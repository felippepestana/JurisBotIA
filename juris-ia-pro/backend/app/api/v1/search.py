"""
Router para endpoints de busca jurídica
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List
import time
from datetime import datetime

from app.models.schemas import (
    SearchRequest,
    SearchResponse,
    SearchResult,
    TipoDocumento,
    InstanciaJudicial
)
from app.core.mock_data import search_mock_documents, get_mock_document_by_id
from app.core.config import settings
from app.services.vector_service import vector_service
from app.services.cache_service import cache_service
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/", response_model=SearchResponse)
async def search_documents(request: SearchRequest):
    """
    Busca documentos jurídicos por termos e filtros.

    Args:
        request: Parâmetros de busca

    Returns:
        SearchResponse com resultados encontrados
    """
    start_time = time.time()

    # Validação básica
    if not request.query or len(request.query.strip()) < 3:
        raise HTTPException(
            status_code=400,
            detail="Query deve ter pelo menos 3 caracteres"
        )

    # Tentar buscar do cache primeiro
    cache_key = cache_service._generate_key(
        "search",
        request.query,
        request.limit,
        request.tipo_documento,
        request.instancia
    )

    cached_response = cache_service.get(cache_key)
    if cached_response:
        logger.info("✅ Retornando do cache")
        return SearchResponse(**cached_response)

    # Buscar documentos
    # Tentar busca vetorial primeiro (se disponível)
    if vector_service.is_available():
        logger.info("🔍 Usando busca vetorial (Qdrant)")
        filters_dict = {}
        if request.tipo_documento:
            filters_dict["tipo_documento"] = request.tipo_documento
        if request.instancia:
            filters_dict["instancia"] = request.instancia

        documents = vector_service.search(
            query=request.query,
            limit=request.limit * 2,  # Buscar mais para aplicar outros filtros
            filters=filters_dict,
            score_threshold=settings.RAG_SIMILARITY_THRESHOLD
        )
        logger.info(f"Encontrados {len(documents)} via busca vetorial")
    else:
        # Fallback para busca mockada
        logger.info("📚 Usando busca mockada (fallback)")
        documents = search_mock_documents(request.query, limit=request.limit)

    # Aplicar filtros
    filtered_docs = documents

    if request.tipo_documento:
        filtered_docs = [
            doc for doc in filtered_docs
            if doc.get("tipo_documento") == request.tipo_documento
        ]

    if request.instancia:
        filtered_docs = [
            doc for doc in filtered_docs
            if doc.get("instancia") == request.instancia
        ]

    if request.data_inicio:
        filtered_docs = [
            doc for doc in filtered_docs
            if doc.get("data_publicacao") and doc["data_publicacao"] >= request.data_inicio
        ]

    if request.data_fim:
        filtered_docs = [
            doc for doc in filtered_docs
            if doc.get("data_publicacao") and doc["data_publicacao"] <= request.data_fim
        ]

    # Converter para formato de resposta
    results = []
    for doc in filtered_docs[request.offset:request.offset + request.limit]:
        # Criar highlight (trecho relevante)
        content = doc.get("conteudo_completo", "")
        query_words = request.query.lower().split()
        highlight = None

        for word in query_words:
            if word in content.lower():
                # Encontrar posição e pegar contexto
                pos = content.lower().find(word)
                start = max(0, pos - 50)
                end = min(len(content), pos + 100)
                highlight = "..." + content[start:end] + "..."
                break

        results.append(
            SearchResult(
                id=doc["id"],
                titulo=doc["titulo"],
                tipo_documento=doc["tipo_documento"],
                ementa=doc.get("ementa"),
                orgao_emissor=doc.get("orgao_emissor"),
                data_publicacao=doc.get("data_publicacao"),
                relevancia_score=doc["relevancia_score"],
                similarity_score=doc.get("similarity_score", 0.0),
                citacoes_count=doc["citacoes_count"],
                highlight=highlight
            )
        )

    # Calcular tempo de processamento
    time_ms = int((time.time() - start_time) * 1000)

    # Filtros aplicados
    filters_applied = {}
    if request.tipo_documento:
        filters_applied["tipo_documento"] = request.tipo_documento
    if request.instancia:
        filters_applied["instancia"] = request.instancia
    if request.data_inicio or request.data_fim:
        filters_applied["data_range"] = {
            "inicio": request.data_inicio,
            "fim": request.data_fim
        }

    response = SearchResponse(
        query=request.query,
        total=len(filtered_docs),
        results=results,
        time_ms=time_ms,
        filters_applied=filters_applied
    )

    # Cachear resposta
    cache_service.set(cache_key, response.model_dump(), ttl=settings.CACHE_TTL_SECONDS)

    return response


@router.get("/{document_id}")
async def get_document(document_id: str):
    """
    Busca documento específico por ID.

    Args:
        document_id: ID do documento

    Returns:
        Documento completo

    Raises:
        HTTPException: Se documento não for encontrado
    """
    document = get_mock_document_by_id(document_id)

    if not document:
        raise HTTPException(
            status_code=404,
            detail=f"Documento {document_id} não encontrado"
        )

    return document


@router.get("/suggest/keywords")
async def suggest_keywords(q: str = Query(..., min_length=2)):
    """
    Sugere palavras-chave para autocompletar busca.

    Args:
        q: Texto para sugerir completions

    Returns:
        Lista de sugestões
    """
    # Cache key para sugestões
    cache_key = cache_service._generate_key("suggestions", q.lower())

    # Verificar cache
    if cache_service.is_available():
        cached = cache_service.get(cache_key)
        if cached:
            logger.debug(f"Cache hit para suggestions: {q}")
            return cached

    # Keywords jurídicas pré-definidas (expandidas)
    all_keywords = [
        # CDC e Consumidor
        "CDC", "código de defesa do consumidor", "consumidor", "direito do consumidor",
        "instituições financeiras", "bancos", "relação de consumo",

        # Práticas bancárias
        "tarifa bancária", "tarifa abusiva", "venda casada", "superendividamento",
        "crédito consignado", "empréstimo", "juros abusivos",
        "cobrança indevida", "dívida bancária",

        # Danos e responsabilidade
        "dano moral", "dano material", "responsabilidade civil", "indenização",
        "reparação de danos", "danos morais e materiais",

        # Princípios
        "boa-fé", "boa-fé objetiva", "transparência", "informação adequada",

        # Processuais
        "petição inicial", "contestação", "recurso", "apelação",
        "agravo de instrumento", "embargos de declaração",

        # Fontes
        "súmula", "jurisprudência", "acórdão", "decisão judicial",
        "lei", "decreto", "medida provisória", "constituição",

        # Tribunais
        "STJ", "STF", "TJSP", "TJRJ", "TJMG", "TRF", "TST", "TRT",

        # Outras áreas
        "direito bancário", "direito civil", "direito do trabalho",
        "direito processual civil", "direito tributário",

        # Temas específicos
        "prescrição", "decadência", "vício do produto", "vício do serviço",
        "inversão do ônus da prova", "responsabilidade objetiva",
        "CDC artigo 6º", "CDC artigo 42", "CDC artigo 51"
    ]

    q_lower = q.lower()
    suggestions = [
        kw for kw in all_keywords
        if q_lower in kw.lower()
    ]

    # Ordenar por relevância (exact match primeiro, depois por tamanho)
    suggestions.sort(key=lambda x: (
        not x.lower().startswith(q_lower),  # Começa com query primeiro
        len(x)  # Depois por tamanho
    ))

    result = {
        "query": q,
        "suggestions": suggestions[:10]
    }

    # Cachear resultado (sugestões mudam pouco)
    if cache_service.is_available():
        cache_service.set(cache_key, result, ttl=3600)  # 1 hora

    return result
