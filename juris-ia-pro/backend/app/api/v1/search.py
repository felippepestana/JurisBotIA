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

router = APIRouter()


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

    # Buscar documentos (usando mock por enquanto)
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

    return SearchResponse(
        query=request.query,
        total=len(filtered_docs),
        results=results,
        time_ms=time_ms,
        filters_applied=filters_applied
    )


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
    # Keywords pré-definidas para MVP
    all_keywords = [
        "CDC", "instituições financeiras", "consumidor", "bancos",
        "tarifa bancária", "venda casada", "superendividamento",
        "dano moral", "responsabilidade civil", "boa-fé",
        "código de defesa do consumidor", "direito bancário",
        "súmula", "jurisprudência", "STJ", "STF", "TJSP"
    ]

    q_lower = q.lower()
    suggestions = [
        kw for kw in all_keywords
        if q_lower in kw.lower()
    ]

    return {
        "query": q,
        "suggestions": suggestions[:10]
    }
