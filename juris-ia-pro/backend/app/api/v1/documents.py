"""
Router para geração de documentos jurídicos
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging

from app.models.schemas import DocumentoGeradoRequest, DocumentoGeradoResponse
from app.services.openai_service import openai_service
from app.core.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/generate", response_model=dict)
async def generate_document(request: DocumentoGeradoRequest):
    """
    Gera documento jurídico com IA.

    Args:
        request: Parâmetros do documento

    Returns:
        Documento gerado

    Raises:
        HTTPException: Se houver erro na geração
    """
    if not settings.ENABLE_DOCUMENT_GENERATION:
        raise HTTPException(
            status_code=503,
            detail="Geração de documentos não está habilitada"
        )

    logger.info(
        f"Gerando documento: {request.tipo_documento} - {request.titulo}"
    )

    # Validar tipo de documento
    valid_types = [
        'peticao', 'contrato', 'parecer', 'recurso',
        'contestacao', 'replica', 'agravo', 'embargos'
    ]

    if request.tipo_documento.lower() not in valid_types:
        raise HTTPException(
            status_code=400,
            detail=f"Tipo de documento inválido. Tipos aceitos: {', '.join(valid_types)}"
        )

    # Validar parâmetros obrigatórios
    if not request.parametros or len(request.parametros) == 0:
        raise HTTPException(
            status_code=400,
            detail="Parâmetros do documento são obrigatórios"
        )

    try:
        # Se OpenAI disponível, gerar com IA
        if openai_service.is_available():
            logger.info("Gerando documento com OpenAI...")

            document_text = openai_service.generate_legal_document(
                document_type=request.tipo_documento,
                parameters=request.parametros
            )

            fontes_citadas = _extract_citations(document_text)

        else:
            # Fallback: gerar mockado
            logger.warning("OpenAI não disponível - usando template mockado")
            document_text = _generate_mock_document(
                request.tipo_documento,
                request.parametros
            )
            fontes_citadas = []

        # Estruturar resposta
        result = {
            "success": True,
            "tipo_documento": request.tipo_documento,
            "titulo": request.titulo,
            "conteudo": document_text,
            "fontes_citadas": fontes_citadas,
            "parametros_utilizados": request.parametros,
            "metadata": {
                "caracteres": len(document_text),
                "palavras": len(document_text.split()),
                "gerado_com": "OpenAI" if openai_service.is_available() else "Template"
            }
        }

        logger.info(
            f"✅ Documento gerado: {len(document_text)} caracteres"
        )

        return result

    except Exception as e:
        logger.error(f"Erro ao gerar documento: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro na geração: {str(e)}"
        )


@router.get("/templates")
async def list_templates():
    """
    Lista templates de documentos disponíveis.

    Returns:
        Lista de templates
    """
    templates = [
        {
            "id": "peticao",
            "nome": "Petição Inicial",
            "descricao": "Petição inicial para ajuizamento de ação",
            "parametros_requeridos": [
                "autor", "reu", "fatos", "pedidos", "valor_causa"
            ]
        },
        {
            "id": "contrato",
            "nome": "Contrato",
            "descricao": "Contrato entre partes",
            "parametros_requeridos": [
                "tipo_contrato", "contratante", "contratado",
                "objeto", "valor", "prazo"
            ]
        },
        {
            "id": "parecer",
            "nome": "Parecer Jurídico",
            "descricao": "Parecer técnico sobre questão jurídica",
            "parametros_requeridos": [
                "consulente", "questao", "fundamentacao"
            ]
        },
        {
            "id": "recurso",
            "nome": "Recurso",
            "descricao": "Recurso de decisão judicial",
            "parametros_requeridos": [
                "tipo_recurso", "recorrente", "decisao_recorrida",
                "fundamentos", "pedidos"
            ]
        },
        {
            "id": "contestacao",
            "nome": "Contestação",
            "descricao": "Contestação em processo judicial",
            "parametros_requeridos": [
                "reu", "autor", "fatos_contestados", "defesa"
            ]
        }
    ]

    return {
        "templates": templates,
        "total": len(templates)
    }


@router.get("/check")
async def check_generation_support():
    """
    Verifica se geração de documentos está disponível.

    Returns:
        Status do serviço
    """
    return {
        "enabled": settings.ENABLE_DOCUMENT_GENERATION,
        "openai_available": openai_service.is_available(),
        "status": "available" if (
            settings.ENABLE_DOCUMENT_GENERATION and
            openai_service.is_available()
        ) else "limited"
    }


def _extract_citations(text: str) -> list:
    """
    Extrai citações de fontes do texto gerado.

    Args:
        text: Texto do documento

    Returns:
        Lista de citações
    """
    import re

    citations = []

    # Padrões de citação
    patterns = [
        r'(Lei\s+\d+\.\d+/\d+)',
        r'(Art\.\s*\d+)',
        r'(Súmula\s+\d+)',
        r'(STJ|STF|TST)\s*-\s*[^\n]+',
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        citations.extend(matches)

    # Remover duplicatas mantendo ordem
    seen = set()
    unique_citations = []
    for citation in citations:
        if citation not in seen:
            seen.add(citation)
            unique_citations.append(citation)

    return unique_citations[:10]  # Limitar a 10


def _generate_mock_document(
    doc_type: str,
    parameters: Dict[str, Any]
) -> str:
    """
    Gera documento mockado quando OpenAI não disponível.

    Args:
        doc_type: Tipo de documento
        parameters: Parâmetros

    Returns:
        Texto do documento
    """
    # Templates simples para cada tipo
    templates = {
        'peticao': """EXCELENTÍSSIMO SENHOR DOUTOR JUIZ DE DIREITO DA {vara} VARA CÍVEL DA COMARCA DE {comarca}

{autor}, {qualificacao_autor}, vem, por seu advogado que esta subscreve, com escritório profissional na {endereco_advogado}, onde recebe intimações, propor a presente

AÇÃO {tipo_acao}

em face de {reu}, {qualificacao_reu}, pelos fatos e fundamentos a seguir aduzidos:

DOS FATOS

{fatos}

DO DIREITO

{fundamentacao_legal}

DOS PEDIDOS

Diante do exposto, requer:

a) {pedidos}

Atribui-se à causa o valor de R$ {valor_causa}.

Termos em que,
Pede deferimento.

{cidade}, {data}

_______________________
{advogado}
OAB/{estado} {oab_numero}
""",

        'contrato': """CONTRATO DE {tipo_contrato}

Pelo presente instrumento particular, de um lado:

CONTRATANTE: {contratante}, {qualificacao_contratante}

E de outro lado:

CONTRATADO: {contratado}, {qualificacao_contratado}

Têm entre si justo e contratado o seguinte:

CLÁUSULA PRIMEIRA - DO OBJETO
{objeto}

CLÁUSULA SEGUNDA - DO VALOR
O valor total do presente contrato é de R$ {valor}.

CLÁUSULA TERCEIRA - DO PRAZO
O prazo de vigência é de {prazo}.

CLÁUSULA QUARTA - DAS OBRIGAÇÕES
{obrigacoes}

CLÁUSULA QUINTA - DO FORO
Fica eleito o foro da Comarca de {foro} para dirimir quaisquer dúvidas.

E por estarem assim justos e contratados, assinam o presente em 2 vias de igual teor.

{cidade}, {data}

_______________________        _______________________
   CONTRATANTE                    CONTRATADO
""",

        'parecer': """PARECER JURÍDICO

CONSULENTE: {consulente}

ASSUNTO: {assunto}

1. DA CONSULTA

{questao}

2. ANÁLISE JURÍDICA

{analise}

3. FUNDAMENTAÇÃO LEGAL

{fundamentacao}

4. CONCLUSÃO

{conclusao}

É o parecer.

{cidade}, {data}

_______________________
{parecerista}
OAB/{estado} {oab_numero}
"""
    }

    template = templates.get(doc_type, "Documento jurídico não disponível em modo mockado.")

    # Substituir placeholders com parâmetros
    try:
        return template.format(**parameters)
    except KeyError as e:
        return f"Documento {doc_type} - Parâmetro faltando: {e}\n\nParâmetros fornecidos:\n" + "\n".join(
            f"- {k}: {v}" for k, v in parameters.items()
        )
