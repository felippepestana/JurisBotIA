"""
Configurações da aplicação usando Pydantic Settings
"""
from typing import List, Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    """Configurações centralizadas da aplicação"""

    # Application
    APP_NAME: str = "JurisIA Pro"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = Field(default="development", env="APP_ENV")
    DEBUG: bool = Field(default=True, env="DEBUG")
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")

    # API
    API_HOST: str = Field(default="0.0.0.0", env="API_HOST")
    API_PORT: int = Field(default=8000, env="API_PORT")
    API_PREFIX: str = "/api/v1"

    # CORS
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://127.0.0.1:3000"],
        env="CORS_ORIGINS"
    )

    # Database
    DATABASE_URL: str = Field(
        default="postgresql://jurisia_user:jurisia_pass_2024@localhost:5432/jurisia_db",
        env="DATABASE_URL"
    )
    DATABASE_POOL_SIZE: int = Field(default=20, env="DATABASE_POOL_SIZE")
    DATABASE_MAX_OVERFLOW: int = Field(default=10, env="DATABASE_MAX_OVERFLOW")

    # Redis
    REDIS_URL: str = Field(
        default="redis://:jurisia_redis_2024@localhost:6379/0",
        env="REDIS_URL"
    )
    REDIS_MAX_CONNECTIONS: int = Field(default=50, env="REDIS_MAX_CONNECTIONS")

    # Qdrant Vector Database
    QDRANT_URL: str = Field(default="http://localhost:6333", env="QDRANT_URL")
    QDRANT_API_KEY: Optional[str] = Field(default=None, env="QDRANT_API_KEY")
    QDRANT_COLLECTION_NAME: str = Field(default="legal_documents", env="QDRANT_COLLECTION_NAME")

    # OpenAI
    OPENAI_API_KEY: str = Field(default="", env="OPENAI_API_KEY")
    OPENAI_MODEL: str = Field(default="gpt-4-turbo-preview", env="OPENAI_MODEL")
    OPENAI_EMBEDDING_MODEL: str = Field(default="text-embedding-3-large", env="OPENAI_EMBEDDING_MODEL")
    OPENAI_MAX_TOKENS: int = Field(default=2000, env="OPENAI_MAX_TOKENS")
    OPENAI_TEMPERATURE: float = Field(default=0.1, env="OPENAI_TEMPERATURE")

    # Embedding Settings
    EMBEDDING_DIMENSION: int = Field(default=3072, env="EMBEDDING_DIMENSION")
    CHUNK_SIZE: int = Field(default=1000, env="CHUNK_SIZE")
    CHUNK_OVERLAP: int = Field(default=200, env="CHUNK_OVERLAP")

    # RAG Configuration
    RAG_TOP_K: int = Field(default=5, env="RAG_TOP_K")
    RAG_SIMILARITY_THRESHOLD: float = Field(default=0.7, env="RAG_SIMILARITY_THRESHOLD")
    RAG_MAX_CONTEXT_LENGTH: int = Field(default=8000, env="RAG_MAX_CONTEXT_LENGTH")

    # Security
    SECRET_KEY: str = Field(
        default="change-this-to-a-random-secret-key-min-32-chars",
        env="SECRET_KEY"
    )
    ALGORITHM: str = Field(default="HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, env="REFRESH_TOKEN_EXPIRE_DAYS")
    BCRYPT_ROUNDS: int = Field(default=12, env="BCRYPT_ROUNDS")

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = Field(default=100, env="RATE_LIMIT_PER_MINUTE")
    RATE_LIMIT_BURST: int = Field(default=20, env="RATE_LIMIT_BURST")

    # File Upload
    MAX_UPLOAD_SIZE_MB: int = Field(default=20, env="MAX_UPLOAD_SIZE_MB")
    ALLOWED_EXTENSIONS: List[str] = Field(
        default=["pdf", "doc", "docx"],
        env="ALLOWED_EXTENSIONS"
    )
    UPLOAD_DIR: str = Field(default="./uploads", env="UPLOAD_DIR")

    # Storage
    STORAGE_TYPE: str = Field(default="local", env="STORAGE_TYPE")
    STORAGE_PATH: str = Field(default="./storage", env="STORAGE_PATH")

    # Monitoring
    ENABLE_METRICS: bool = Field(default=True, env="ENABLE_METRICS")
    METRICS_PORT: int = Field(default=9090, env="METRICS_PORT")

    # Scraping
    SCRAPING_ENABLED: bool = Field(default=True, env="SCRAPING_ENABLED")
    SCRAPING_SCHEDULE_HOURS: int = Field(default=24, env="SCRAPING_SCHEDULE_HOURS")
    SCRAPING_CONCURRENT_REQUESTS: int = Field(default=5, env="SCRAPING_CONCURRENT_REQUESTS")
    SCRAPING_USER_AGENT: str = Field(default="JurisIA-Bot/1.0", env="SCRAPING_USER_AGENT")

    # Feature Flags
    ENABLE_CHAT: bool = Field(default=True, env="ENABLE_CHAT")
    ENABLE_DOCUMENT_GENERATION: bool = Field(default=True, env="ENABLE_DOCUMENT_GENERATION")
    ENABLE_PDF_ANALYSIS: bool = Field(default=True, env="ENABLE_PDF_ANALYSIS")
    ENABLE_LEGAL_ALERTS: bool = Field(default=True, env="ENABLE_LEGAL_ALERTS")

    # Performance
    CACHE_TTL_SECONDS: int = Field(default=3600, env="CACHE_TTL_SECONDS")
    QUERY_TIMEOUT_SECONDS: int = Field(default=30, env="QUERY_TIMEOUT_SECONDS")
    MAX_CONCURRENT_REQUESTS: int = Field(default=100, env="MAX_CONCURRENT_REQUESTS")

    # Development
    DEV_AUTO_RELOAD: bool = Field(default=True, env="DEV_AUTO_RELOAD")
    DEV_MOCK_AI: bool = Field(default=False, env="DEV_MOCK_AI")
    DEV_SAMPLE_DATA: bool = Field(default=True, env="DEV_SAMPLE_DATA")

    @field_validator('CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            # Se for string JSON, parse it
            import json
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                # Se não for JSON, assume que é comma-separated
                return [origin.strip() for origin in v.split(',')]
        return v

    @field_validator('ALLOWED_EXTENSIONS', mode='before')
    @classmethod
    def parse_allowed_extensions(cls, v):
        if isinstance(v, str):
            import json
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return [ext.strip() for ext in v.split(',')]
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Instância global de configurações
settings = Settings()


# Função auxiliar para validar configurações críticas
def validate_critical_settings():
    """Valida configurações críticas antes de iniciar a aplicação"""
    errors = []

    if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "":
        errors.append("OPENAI_API_KEY não configurada")

    if settings.SECRET_KEY == "change-this-to-a-random-secret-key-min-32-chars":
        errors.append("SECRET_KEY padrão detectada - altere para produção!")

    if not settings.DATABASE_URL:
        errors.append("DATABASE_URL não configurada")

    if errors:
        error_msg = "\n".join([f"  - {error}" for error in errors])
        if settings.APP_ENV == "production":
            raise ValueError(f"Configurações críticas faltando:\n{error_msg}")
        else:
            print(f"⚠️  AVISOS DE CONFIGURAÇÃO:\n{error_msg}")

    return len(errors) == 0
