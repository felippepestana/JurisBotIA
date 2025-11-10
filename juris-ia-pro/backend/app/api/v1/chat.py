"""
Router para endpoints de chat jurídico com IA
"""
from fastapi import APIRouter, HTTPException
import time
from datetime import datetime
import uuid
import hashlib

from app.models.schemas import (
    ChatMessage,
    ChatResponse,
    SourceReference
)
from app.core.mock_data import search_mock_documents
from app.core.config import settings
from app.services.openai_service import openai_service
from app.services.cache_service import cache_service
from app.services.vector_service import vector_service
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


def generate_mock_legal_response(query: str, documents: list) -> str:
    """
    Gera resposta jurídica mockada (sem chamar OpenAI para desenvolvimento).

    Args:
        query: Pergunta do usuário
        documents: Documentos encontrados

    Returns:
        Resposta formatada
    """
    query_lower = query.lower()

    # Respostas pré-definidas baseadas em palavras-chave
    if "cdc" in query_lower and "banco" in query_lower or "financeira" in query_lower:
        return """Com base na jurisprudência consultada, podemos afirmar que:

**POSIÇÃO CONSOLIDADA:**
O Código de Defesa do Consumidor (CDC) **aplica-se plenamente** às instituições financeiras, conforme estabelecido pela Súmula 297 do Superior Tribunal de Justiça (STJ).

**FUNDAMENTAÇÃO LEGAL:**
- **Súmula 297 do STJ**: "O Código de Defesa do Consumidor é aplicável às instituições financeiras"
- **Lei 8.078/90, Art. 3º, § 2º**: Define expressamente que serviço inclui atividades de natureza bancária e financeira
- **Constituição Federal, Art. 5º, XXXII**: Estabelece que o Estado promoverá a defesa do consumidor

**IMPLICAÇÕES PRÁTICAS:**
- Bancos devem observar os princípios da boa-fé, transparência e razoabilidade
- Práticas abusivas, como venda casada, são vedadas
- Consumidor tem direito à informação clara sobre produtos e tarifas"""

    elif "tarifa" in query_lower:
        return """Sobre tarifas bancárias, a jurisprudência estabelece:

**POSIÇÃO DO STF:**
É **inconstitucional** a cobrança de tarifa de abertura de conta corrente, conforme decidido no RE 591.054, por caracterizar venda casada vedada pelo CDC.

**PRINCÍPIOS APLICÁVEIS:**
- Tarifas devem ser **razoáveis e proporcionais**
- É necessária **transparência prévia** na informação
- Cobranças abusivas permitem restituição em dobro (Art. 42, parágrafo único, do CDC)

**JURISPRUDÊNCIA RELEVANTE:**
- STF - RE 591.054: Inconstitucionalidade da tarifa de abertura de conta
- TJSP: Casos recentes reconhecem direito à restituição de tarifas abusivas"""

    elif "superendividamento" in query_lower:
        return """Sobre superendividamento, a jurisprudência reconhece:

**PROTEÇÃO AO CONSUMIDOR:**
A concessão **irresponsável de crédito** configura prática abusiva passível de reparação, conforme REsp 1.255.573/RS do STJ.

**RESPONSABILIDADE DA INSTITUIÇÃO:**
- Dever de avaliar capacidade de pagamento
- Vedação ao estímulo ao consumo irresponsável
- Possibilidade de dano moral coletivo

**BASE LEGAL:**
- CDC - Princípio da boa-fé objetiva
- Prevenção ao superendividamento
- Jurisprudência consolidada no STJ"""

    else:
        # Resposta genérica
        return f"""Com base nos {len(documents)} documentos consultados na base jurídica:

**ANÁLISE:**
A questão levantada possui relevância jurídica e deve ser analisada à luz da legislação e jurisprudência brasileira.

**RECOMENDAÇÕES:**
1. Consulte os documentos específicos citados nas fontes
2. Verifique a aplicabilidade ao caso concreto
3. Considere consultar um advogado especializado

**OBSERVAÇÃO:**
Esta resposta é baseada em informações gerais. Para análise específica do seu caso, recomendamos consulta jurídica individualizada."""


@router.post("/", response_model=ChatResponse)
async def legal_chat(message: ChatMessage):
    """
    Chat jurídico com IA.

    Args:
        message: Mensagem do usuário

    Returns:
        Resposta da IA com fontes citadas

    Raises:
        HTTPException: Se houver erro no processamento
    """
    start_time = time.time()

    # Validação
    if not message.message or len(message.message.strip()) < 3:
        raise HTTPException(
            status_code=400,
            detail="Mensagem deve ter pelo menos 3 caracteres"
        )

    # Gerar cache key baseado na mensagem
    # Nota: não incluímos conversation_id no cache pois queremos reusar respostas para mesma pergunta
    cache_key = cache_service._generate_key(
        "chat",
        message.message.lower().strip()
    )

    # Verificar cache
    if cache_service.is_available():
        cached_response = cache_service.get(cache_key)
        if cached_response:
            logger.info(f"Cache hit para chat: {message.message[:50]}")
            # Atualizar conversation_id se fornecido
            if message.conversation_id:
                cached_response["conversation_id"] = message.conversation_id
            return ChatResponse(**cached_response)

    # Buscar documentos relevantes com vector search
    if vector_service.is_available():
        logger.info("Buscando documentos com vector search")
        documents = vector_service.search(
            query=message.message,
            limit=5,
            score_threshold=0.65  # Threshold mais baixo para chat (mais documentos)
        )
    else:
        logger.info("Vector search indisponível, usando mock")
        documents = search_mock_documents(message.message, limit=5)

    if not documents:
        return ChatResponse(
            response="Não encontrei informações jurídicas relevantes para sua pergunta na base de dados atual. Por favor, reformule sua consulta ou seja mais específico sobre o tema jurídico que deseja consultar.",
            sources=[],
            confidence=0.0,
            conversation_id=message.conversation_id or str(uuid.uuid4()),
            processing_time_ms=int((time.time() - start_time) * 1000)
        )

    # Gerar resposta
    if settings.DEV_MOCK_AI or not openai_service.is_available():
        # Modo mock (desenvolvimento ou sem API key)
        logger.info("Usando resposta mockada (OpenAI não disponível)")
        ai_response = generate_mock_legal_response(message.message, documents)
        confidence = 0.85
    else:
        # Usar OpenAI real
        try:
            logger.info("Gerando resposta com OpenAI API")
            ai_response, confidence = openai_service.generate_legal_response(
                query=message.message,
                documents=documents
            )
        except Exception as e:
            logger.error(f"Erro ao usar OpenAI, fallback para mock: {e}")
            ai_response = generate_mock_legal_response(message.message, documents)
            confidence = 0.85

    # Preparar fontes
    sources = []
    for doc in documents[:3]:  # Top 3 mais relevantes
        # Extrair trecho relevante
        content = doc.get("conteudo_completo", "")
        excerpt = content[:200] + "..." if len(content) > 200 else content

        sources.append(
            SourceReference(
                documento_id=doc["id"],
                titulo=doc["titulo"],
                orgao=doc.get("orgao_emissor"),
                data=doc.get("data_publicacao"),
                trecho_relevante=excerpt,
                confianca=doc.get("similarity_score", doc["relevancia_score"])
            )
        )

    # Calcular tempo de processamento
    processing_time_ms = int((time.time() - start_time) * 1000)

    # ID da conversa
    conversation_id = message.conversation_id or str(uuid.uuid4())

    # Criar resposta
    response = ChatResponse(
        response=ai_response,
        sources=sources,
        confidence=confidence,
        conversation_id=conversation_id,
        processing_time_ms=processing_time_ms
    )

    # Cachear resposta (se cache disponível e confiança boa)
    if cache_service.is_available() and confidence >= 0.7:
        try:
            cache_service.set(
                cache_key,
                response.model_dump(),
                ttl=600  # 10 minutos para chat (pode mudar mais que busca)
            )
            logger.debug(f"Resposta de chat cacheada: {message.message[:50]}")
        except Exception as e:
            logger.warning(f"Erro ao cachear resposta de chat: {e}")

    return response


@router.get("/history")
async def get_chat_history(conversation_id: str):
    """
    Busca histórico de uma conversa.

    Args:
        conversation_id: ID da conversa

    Returns:
        Histórico de mensagens

    Note:
        Implementação mockada para MVP
    """
    # TODO: Implementar busca real no banco de dados
    return {
        "conversation_id": conversation_id,
        "messages": [],
        "created_at": datetime.utcnow().isoformat(),
        "note": "Histórico de conversas será implementado na próxima versão"
    }
