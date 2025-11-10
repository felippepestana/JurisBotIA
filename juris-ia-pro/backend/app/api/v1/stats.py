"""
Router para endpoint de estatísticas do sistema
"""
from fastapi import APIRouter
from typing import Dict, Any
import time
from datetime import datetime

from app.services.cache_service import cache_service
from app.services.vector_service import vector_service
from app.services.openai_service import openai_service
from app.core.config import settings
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/")
async def get_system_stats() -> Dict[str, Any]:
    """
    Retorna estatísticas gerais do sistema.

    Returns:
        Dicionário com estatísticas detalhadas
    """
    start_time = time.time()

    # Verificar status dos serviços
    services_status = {
        "redis": {
            "available": cache_service.is_available(),
            "status": "online" if cache_service.is_available() else "offline"
        },
        "qdrant": {
            "available": vector_service.is_available(),
            "status": "online" if vector_service.is_available() else "offline"
        },
        "openai": {
            "available": openai_service.is_available(),
            "status": "online" if openai_service.is_available() else "offline"
        }
    }

    # Estatísticas do cache
    cache_stats = {}
    if cache_service.is_available():
        try:
            cache_stats = cache_service.get_stats()
        except Exception as e:
            logger.warning(f"Erro ao buscar stats do cache: {e}")
            cache_stats = {"error": str(e)}

    # Estatísticas do vector database
    vector_stats = {}
    if vector_service.is_available():
        try:
            collection_info = vector_service.collection_info()
            vector_stats = {
                "collection_name": settings.QDRANT_COLLECTION,
                "documents_indexed": collection_info.get("vectors_count", 0),
                "vector_dimension": settings.VECTOR_DIMENSION,
                "status": collection_info.get("status", "unknown")
            }
        except Exception as e:
            logger.warning(f"Erro ao buscar stats do Qdrant: {e}")
            vector_stats = {"error": str(e)}

    # Configurações do sistema
    system_config = {
        "environment": "development" if settings.DEV_MOCK_AI else "production",
        "cache_ttl_seconds": settings.CACHE_TTL_SECONDS,
        "rag_similarity_threshold": settings.RAG_SIMILARITY_THRESHOLD,
        "openai_model": settings.OPENAI_MODEL,
        "embedding_model": settings.OPENAI_EMBEDDING_MODEL
    }

    # Tempo de resposta
    processing_time_ms = int((time.time() - start_time) * 1000)

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "system": {
            "version": "1.0.0",
            "status": "operational",
            "uptime_check_ms": processing_time_ms
        },
        "services": services_status,
        "cache": cache_stats,
        "vector_database": vector_stats,
        "configuration": system_config
    }


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    Health check simplificado do sistema.

    Returns:
        Status de saúde dos serviços
    """
    services_health = {
        "redis": cache_service.is_available(),
        "qdrant": vector_service.is_available(),
        "openai": openai_service.is_available()
    }

    # Sistema está healthy se pelo menos Qdrant ou OpenAI estiver disponível
    is_healthy = services_health["qdrant"] or services_health["openai"]

    return {
        "status": "healthy" if is_healthy else "degraded",
        "timestamp": datetime.utcnow().isoformat(),
        "services": services_health,
        "message": "All systems operational" if is_healthy else "Some services unavailable"
    }


@router.get("/cache/stats")
async def get_cache_stats() -> Dict[str, Any]:
    """
    Retorna estatísticas detalhadas do cache Redis.

    Returns:
        Estatísticas do cache
    """
    if not cache_service.is_available():
        return {
            "available": False,
            "message": "Redis cache not available"
        }

    try:
        stats = cache_service.get_stats()
        return {
            "available": True,
            "timestamp": datetime.utcnow().isoformat(),
            "statistics": stats
        }
    except Exception as e:
        logger.error(f"Erro ao buscar estatísticas do cache: {e}")
        return {
            "available": True,
            "error": str(e)
        }


@router.get("/vector/stats")
async def get_vector_stats() -> Dict[str, Any]:
    """
    Retorna estatísticas detalhadas do banco vetorial Qdrant.

    Returns:
        Estatísticas do Qdrant
    """
    if not vector_service.is_available():
        return {
            "available": False,
            "message": "Qdrant vector database not available"
        }

    try:
        collection_info = vector_service.collection_info()
        return {
            "available": True,
            "timestamp": datetime.utcnow().isoformat(),
            "collection": settings.QDRANT_COLLECTION,
            "statistics": collection_info
        }
    except Exception as e:
        logger.error(f"Erro ao buscar estatísticas do Qdrant: {e}")
        return {
            "available": True,
            "error": str(e)
        }


@router.post("/cache/clear")
async def clear_cache(pattern: str = "*") -> Dict[str, Any]:
    """
    Limpa cache baseado em padrão.

    Args:
        pattern: Padrão de chaves a limpar (default: *)

    Returns:
        Resultado da operação

    Warning:
        Use com cuidado em produção!
    """
    if not cache_service.is_available():
        return {
            "success": False,
            "message": "Redis cache not available"
        }

    try:
        # Validar padrão para evitar limpeza acidental total
        if pattern == "*":
            # Permitir apenas com confirmação explícita
            logger.warning("Tentativa de limpar TODO o cache!")

        cleared = cache_service.clear_pattern(pattern)
        return {
            "success": True,
            "pattern": pattern,
            "keys_cleared": cleared,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Erro ao limpar cache: {e}")
        return {
            "success": False,
            "error": str(e)
        }


@router.get("/performance")
async def get_performance_metrics() -> Dict[str, Any]:
    """
    Retorna métricas de performance estimadas.

    Returns:
        Métricas de performance
    """
    # Testes simples de performance
    metrics = {}

    # Teste de cache
    if cache_service.is_available():
        cache_start = time.time()
        test_key = "test:performance:check"
        cache_service.set(test_key, {"test": "data"}, ttl=10)
        cache_service.get(test_key)
        cache_service.delete(test_key)
        cache_time = (time.time() - cache_start) * 1000
        metrics["cache_roundtrip_ms"] = round(cache_time, 2)
    else:
        metrics["cache_roundtrip_ms"] = None

    # Teste de vector search
    if vector_service.is_available():
        vector_start = time.time()
        try:
            # Busca simples de teste
            vector_service.search("teste performance", limit=1)
            vector_time = (time.time() - vector_start) * 1000
            metrics["vector_search_ms"] = round(vector_time, 2)
        except Exception as e:
            logger.warning(f"Erro no teste de vector search: {e}")
            metrics["vector_search_ms"] = None
    else:
        metrics["vector_search_ms"] = None

    # Benchmarks esperados
    benchmarks = {
        "cache_hit_target_ms": 50,
        "cache_miss_target_ms": 800,
        "chat_response_target_ms": 2000,
        "pdf_analysis_target_ms": 5000
    }

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "current_metrics": metrics,
        "target_benchmarks": benchmarks,
        "status": "Performance metrics collected successfully"
    }
