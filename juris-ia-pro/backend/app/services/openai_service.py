"""
Serviço de integração com OpenAI para geração de respostas jurídicas
"""
from typing import List, Dict, Any, Tuple
import openai
from openai import OpenAI
import logging
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import settings

logger = logging.getLogger(__name__)


class OpenAIService:
    """Serviço para interação com OpenAI API"""

    def __init__(self):
        """Inicializa o cliente OpenAI"""
        if not settings.OPENAI_API_KEY:
            logger.warning("OPENAI_API_KEY não configurada - usando modo mock")
            self.client = None
        else:
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def is_available(self) -> bool:
        """Verifica se o serviço está disponível"""
        return self.client is not None

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def generate_embedding(self, text: str) -> List[float]:
        """
        Gera embedding vetorial para um texto.

        Args:
            text: Texto para gerar embedding

        Returns:
            Lista de floats representando o embedding

        Raises:
            Exception: Se houver erro na API
        """
        if not self.is_available():
            raise Exception("OpenAI API não configurada")

        try:
            response = self.client.embeddings.create(
                model=settings.OPENAI_EMBEDDING_MODEL,
                input=text,
                encoding_format="float"
            )

            embedding = response.data[0].embedding
            logger.info(f"Embedding gerado: {len(embedding)} dimensões")

            return embedding

        except Exception as e:
            logger.error(f"Erro ao gerar embedding: {e}")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def generate_legal_response(
        self,
        query: str,
        documents: List[Dict[str, Any]],
        system_prompt: str = None
    ) -> Tuple[str, float]:
        """
        Gera resposta jurídica baseada em documentos.

        Args:
            query: Pergunta do usuário
            documents: Lista de documentos jurídicos relevantes
            system_prompt: Prompt customizado do sistema (opcional)

        Returns:
            Tuple[str, float]: (resposta, confidence score)

        Raises:
            Exception: Se houver erro na API
        """
        if not self.is_available():
            raise Exception("OpenAI API não configurada")

        # Montar contexto dos documentos
        context = self._build_context(documents)

        # System prompt padrão
        if not system_prompt:
            system_prompt = """Você é um assistente jurídico especializado em direito brasileiro.

REGRAS OBRIGATÓRIAS:
1. Responda APENAS com base nos documentos fornecidos no contexto
2. Cite SEMPRE as fontes específicas (tribunal, número, data)
3. Use linguagem jurídica apropriada mas acessível
4. Se não houver informação suficiente, diga claramente
5. NUNCA invente decisões, súmulas ou jurisprudência
6. Indique divergências jurisprudenciais quando houver
7. Estruture a resposta de forma clara e profissional

FORMATO DE RESPOSTA:
**POSIÇÃO JURÍDICA:**
[Resposta direta à pergunta]

**FUNDAMENTAÇÃO LEGAL:**
[Base legal e jurisprudencial com citações precisas]

**FONTES CONSULTADAS:**
[Liste as fontes utilizadas]"""

        # User prompt com contexto
        user_prompt = f"""CONTEXTO JURÍDICO:
{context}

PERGUNTA DO USUÁRIO:
{query}

Responda de forma fundamentada e cite as fontes consultadas."""

        try:
            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=settings.OPENAI_MAX_TOKENS,
                temperature=settings.OPENAI_TEMPERATURE,
                presence_penalty=0.1,
                frequency_penalty=0.1
            )

            answer = response.choices[0].message.content

            # Calcular confidence baseado em finish_reason e uso de tokens
            finish_reason = response.choices[0].finish_reason
            tokens_used = response.usage.total_tokens
            max_tokens = settings.OPENAI_MAX_TOKENS

            # Confidence score
            if finish_reason == "stop" and tokens_used < max_tokens * 0.9:
                confidence = 0.85
            elif finish_reason == "stop":
                confidence = 0.75
            else:
                confidence = 0.65

            logger.info(
                f"Resposta gerada: {len(answer)} chars, "
                f"{tokens_used} tokens, "
                f"confidence: {confidence}"
            )

            return answer, confidence

        except Exception as e:
            logger.error(f"Erro ao gerar resposta legal: {e}")
            raise

    def _build_context(self, documents: List[Dict[str, Any]]) -> str:
        """
        Constrói contexto formatado dos documentos.

        Args:
            documents: Lista de documentos jurídicos

        Returns:
            String com contexto formatado
        """
        context_parts = []

        for i, doc in enumerate(documents, 1):
            doc_context = f"""
═══════════════════════════════════════
DOCUMENTO {i}
═══════════════════════════════════════
FONTE: {doc.get('orgao_emissor', 'N/A')}
TIPO: {doc.get('tipo_documento', 'N/A').upper()}
TÍTULO: {doc.get('titulo', 'N/A')}
DATA: {doc.get('data_publicacao', 'N/A')}
NÚMERO: {doc.get('numero_processo', 'N/A')}

EMENTA:
{doc.get('ementa', 'N/A')}

CONTEÚDO:
{doc.get('conteudo_completo', 'N/A')[:1500]}...

RELEVÂNCIA: {doc.get('relevancia_score', 0):.2f}
CITAÇÕES: {doc.get('citacoes_count', 0)}
"""
            context_parts.append(doc_context)

        return "\n".join(context_parts)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def analyze_legal_document(
        self,
        document_text: str,
        analysis_type: str = "completa"
    ) -> Dict[str, Any]:
        """
        Analisa um documento jurídico (ex: processo PDF).

        Args:
            document_text: Texto do documento
            analysis_type: Tipo de análise (completa, sumaria, especifica)

        Returns:
            Dict com análise estruturada

        Raises:
            Exception: Se houver erro na API
        """
        if not self.is_available():
            raise Exception("OpenAI API não configurada")

        system_prompt = """Você é um especialista em análise de documentos jurídicos brasileiros.

Analise o documento fornecido e extraia:
1. TESE PRINCIPAL - Qual a questão jurídica central
2. PARTES ENVOLVIDAS - Quem são os atores
3. ÁREA DO DIREITO - Classificação jurídica
4. PEDIDOS - O que está sendo solicitado
5. FUNDAMENTAÇÃO - Base legal e jurisprudencial citada
6. PALAVRAS-CHAVE - Termos jurídicos relevantes
7. SUGESTÕES - Próximos passos ou decisões aplicáveis

Seja objetivo e profissional."""

        user_prompt = f"""Analise o seguinte documento jurídico:

{document_text[:4000]}

Forneça uma análise {analysis_type} estruturada."""

        try:
            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=1500,
                temperature=0.2
            )

            analysis = response.choices[0].message.content

            # Estruturar análise
            result = {
                "analise_completa": analysis,
                "tipo_analise": analysis_type,
                "tokens_utilizados": response.usage.total_tokens,
                "modelo": settings.OPENAI_MODEL
            }

            logger.info(f"Análise de documento concluída: {len(analysis)} chars")

            return result

        except Exception as e:
            logger.error(f"Erro ao analisar documento: {e}")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def generate_legal_document(
        self,
        document_type: str,
        parameters: Dict[str, Any]
    ) -> str:
        """
        Gera documento jurídico (petição, contrato, etc).

        Args:
            document_type: Tipo de documento (peticao, contrato, parecer, etc)
            parameters: Parâmetros necessários para geração

        Returns:
            Texto do documento gerado

        Raises:
            Exception: Se houver erro na API
        """
        if not self.is_available():
            raise Exception("OpenAI API não configurada")

        # Templates por tipo
        templates = {
            "peticao": """Gere uma petição inicial profissional seguindo a estrutura:
1. EXCELENTÍSSIMO SENHOR DOUTOR JUIZ
2. Identificação das partes
3. DOS FATOS
4. DO DIREITO
5. DA JURISPRUDÊNCIA
6. DOS PEDIDOS

Use linguagem jurídica formal e brasileira.""",

            "contrato": """Gere um contrato formal seguindo a estrutura:
1. CONTRATO DE [TIPO]
2. Identificação das partes
3. CLÁUSULAS (numeradas)
4. Disposições finais
5. Foro e assinaturas

Use linguagem contratual formal.""",

            "parecer": """Gere um parecer jurídico seguindo a estrutura:
1. CONSULENTE
2. CONSULTA
3. PARECER
4. FUNDAMENTAÇÃO
5. CONCLUSÃO

Use linguagem técnica e fundamentada."""
        }

        system_prompt = templates.get(
            document_type,
            "Gere um documento jurídico profissional e bem estruturado."
        )

        user_prompt = f"""Gere o documento com os seguintes parâmetros:

{self._format_parameters(parameters)}

O documento deve ser completo, profissional e pronto para uso."""

        try:
            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=2000,
                temperature=0.3
            )

            document = response.choices[0].message.content

            logger.info(
                f"Documento {document_type} gerado: "
                f"{len(document)} chars"
            )

            return document

        except Exception as e:
            logger.error(f"Erro ao gerar documento: {e}")
            raise

    def _format_parameters(self, parameters: Dict[str, Any]) -> str:
        """Formata parâmetros para o prompt"""
        formatted = []
        for key, value in parameters.items():
            formatted.append(f"- {key.upper()}: {value}")
        return "\n".join(formatted)


# Instância global do serviço
openai_service = OpenAIService()
