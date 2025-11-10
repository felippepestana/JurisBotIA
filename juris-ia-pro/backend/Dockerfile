# Backend Dockerfile - Produção otimizado
FROM python:3.11-slim as base

# Metadata
LABEL maintainer="JurisIA Pro <contato@jurisia.pro>"
LABEL description="Backend do JurisIA Pro - Sistema Jurídico Inteligente"

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar apenas requirements primeiro (para cache de layer)
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY app/ ./app/
COPY scripts/ ./scripts/

# Criar usuário não-root para segurança
RUN useradd -m -u 1000 jurisia && \
    chown -R jurisia:jurisia /app

USER jurisia

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expor porta
EXPOSE 8000

# Comando padrão
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
