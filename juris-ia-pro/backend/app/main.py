"""
JurisIA Pro - API Principal
Sistema Jurídico Inteligente com IA
"""
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
import time
import logging
from datetime import datetime

from app.core.config import settings, validate_critical_settings
from app.core.database import check_db_connection
from app.models.schemas import HealthResponse, ErrorResponse

# Configurar logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Lifespan context manager para startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia o ciclo de vida da aplicação.
    Executado no startup e shutdown.
    """
    # STARTUP
    logger.info(f"🚀 Iniciando {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"   Ambiente: {settings.APP_ENV}")
    logger.info(f"   Debug: {settings.DEBUG}")

    # Validar configurações críticas
    try:
        validate_critical_settings()
    except ValueError as e:
        logger.error(f"❌ Erro nas configurações: {e}")
        if settings.APP_ENV == "production":
            raise

    # Verificar conexão com banco (apenas em produção)
    if settings.APP_ENV == "production":
        if not check_db_connection():
            logger.error("❌ Falha ao conectar no banco de dados")
            raise Exception("Database connection failed")
    else:
        logger.info("⚠️  Modo desenvolvimento: usando dados mockados (banco não requerido)")

    logger.info("✅ Aplicação iniciada com sucesso!")

    yield  # Aplicação roda aqui

    # SHUTDOWN
    logger.info("🛑 Encerrando aplicação...")


# Criar aplicação FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    description="Sistema Jurídico Inteligente com IA - Busca, análise e geração de documentos legais",
    version=settings.APP_VERSION,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan,
)


# ============================================
# MIDDLEWARES
# ============================================

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Process-Time"]
)

# GZip Compression
app.add_middleware(GZipMiddleware, minimum_size=1000)


# Middleware para medir tempo de processamento
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.4f}"

    # Log de requests lentos
    if process_time > 1.0:
        logger.warning(
            f"Slow request: {request.method} {request.url.path} "
            f"took {process_time:.2f}s"
        )

    return response


# Middleware para logging de requisições
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"{request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code}"
    )
    return response


# ============================================
# EXCEPTION HANDLERS
# ============================================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handler para erros de validação"""
    logger.warning(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(
            detail="Erro de validação nos dados enviados",
            error_code="VALIDATION_ERROR"
        ).model_dump()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handler para exceções gerais"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            detail="Erro interno do servidor",
            error_code="INTERNAL_ERROR"
        ).model_dump()
    )


# ============================================
# ROTAS BÁSICAS
# ============================================

@app.get("/", tags=["Root"])
async def root():
    """Rota raiz da API"""
    return {
        "message": f"🏛️ {settings.APP_NAME} API",
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV,
        "docs": "/docs" if settings.DEBUG else "disabled",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Verifica o status de saúde da aplicação e suas dependências.

    Returns:
        HealthResponse: Status de todos os serviços
    """
    # Verificar database (apenas em produção)
    if settings.APP_ENV == "production":
        db_status = "healthy" if check_db_connection() else "unhealthy"
    else:
        db_status = "mocked"  # Usando dados mockados em dev

    # TODO: Verificar Redis
    redis_status = "not_checked"

    # TODO: Verificar Qdrant
    qdrant_status = "not_checked"

    # TODO: Verificar OpenAI
    openai_status = "configured" if settings.OPENAI_API_KEY else "not_configured"

    # Status geral
    if settings.APP_ENV == "development":
        overall_status = "healthy"  # Dev sempre saudável com mocks
    else:
        overall_status = "healthy" if db_status == "healthy" else "degraded"

    return HealthResponse(
        status=overall_status,
        version=settings.APP_VERSION,
        timestamp=datetime.utcnow(),
        database=db_status,
        redis=redis_status,
        qdrant=qdrant_status,
        openai=openai_status
    )


@app.get("/api/v1/info", tags=["Info"])
async def api_info():
    """
    Informações sobre a API e recursos disponíveis.

    Returns:
        dict: Informações da API
    """
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "features": {
            "chat": settings.ENABLE_CHAT,
            "document_generation": settings.ENABLE_DOCUMENT_GENERATION,
            "pdf_analysis": settings.ENABLE_PDF_ANALYSIS,
            "legal_alerts": settings.ENABLE_LEGAL_ALERTS
        },
        "limits": {
            "max_upload_mb": settings.MAX_UPLOAD_SIZE_MB,
            "rate_limit_per_minute": settings.RATE_LIMIT_PER_MINUTE
        },
        "endpoints": {
            "search": f"{settings.API_PREFIX}/search",
            "chat": f"{settings.API_PREFIX}/chat",
            "documents": f"{settings.API_PREFIX}/documents",
            "analyze": f"{settings.API_PREFIX}/analyze",
            "docs": "/docs" if settings.DEBUG else None
        }
    }


# ============================================
# IMPORT E REGISTER DE ROTAS
# ============================================

from app.api.v1 import search, chat, documents, analyze

app.include_router(
    search.router,
    prefix=f"{settings.API_PREFIX}/search",
    tags=["Search"]
)

app.include_router(
    chat.router,
    prefix=f"{settings.API_PREFIX}/chat",
    tags=["Chat"]
)

app.include_router(
    documents.router,
    prefix=f"{settings.API_PREFIX}/documents",
    tags=["Documents"]
)

app.include_router(
    analyze.router,
    prefix=f"{settings.API_PREFIX}/analyze",
    tags=["Analysis"]
)

# TODO: Implementar router de autenticação
# from app.api.v1 import auth
#
# app.include_router(
#     auth.router,
#     prefix=f"{settings.API_PREFIX}/auth",
#     tags=["Authentication"]
# )


# ============================================
# ROTAS TEMPORÁRIAS PARA MVP
# ============================================

@app.get(f"{settings.API_PREFIX}/stats", tags=["Stats"])
async def get_stats():
    """
    Estatísticas básicas do sistema.

    Returns:
        dict: Estatísticas do sistema
    """
    from app.core.mock_data import get_mock_stats

    stats = get_mock_stats()
    stats["version"] = settings.APP_VERSION
    stats["last_update"] = "2024-01-15T00:00:00Z"

    return stats


# ============================================
# MAIN (para execução direta)
# ============================================

if __name__ == "__main__":
    import uvicorn

    logger.info(f"Iniciando servidor em {settings.API_HOST}:{settings.API_PORT}")

    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEV_AUTO_RELOAD and settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
        access_log=settings.DEBUG
    )
