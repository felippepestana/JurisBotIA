"""
🏛️ JurisIA Pro - Servidor Demo Simplificado

Este é um servidor de DEMONSTRAÇÃO que funciona SEM:
- Docker
- PostgreSQL
- Redis
- Qdrant
- OpenAI API

Usa dados MOCK para demonstrar as funcionalidades.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import time

# ========================================
# Configuração do FastAPI
# ========================================

app = FastAPI(
    title="JurisIA Pro - Demo",
    description="Sistema de IA Jurídica - Versão Demonstração",
    version="1.0.0-demo"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========================================
# Modelos Pydantic
# ========================================

class SearchRequest(BaseModel):
    query: str
    limit: Optional[int] = 5
    tipo: Optional[str] = None

class ChatRequest(BaseModel):
    query: str
    conversa_id: Optional[str] = None

class DocumentoJuridico(BaseModel):
    id: int
    titulo: str
    tipo: str
    conteudo: str
    relevancia: float
    fonte: str
    data_publicacao: str

class SearchResponse(BaseModel):
    results: List[DocumentoJuridico]
    total: int
    tempo_ms: int

class ChatResponse(BaseModel):
    resposta: str
    fontes: List[Dict[str, Any]]
    tempo_ms: int
    conversa_id: str

# ========================================
# Dados MOCK
# ========================================

DOCUMENTOS_MOCK = [
    {
        "id": 1,
        "titulo": "CDC - Código de Defesa do Consumidor (Lei 8.078/1990)",
        "tipo": "lei",
        "conteudo": "O Código de Defesa do Consumidor estabelece normas de proteção e defesa do consumidor, de ordem pública e interesse social. Aplica-se a instituições financeiras conforme Súmula 297 do STJ.",
        "fonte": "Planalto",
        "data_publicacao": "1990-09-11"
    },
    {
        "id": 2,
        "titulo": "Súmula 297 STJ - CDC e Instituições Financeiras",
        "tipo": "sumula",
        "conteudo": "O Código de Defesa do Consumidor é aplicável às instituições financeiras.",
        "fonte": "STJ",
        "data_publicacao": "2004-09-22"
    },
    {
        "id": 3,
        "titulo": "CPC - Código de Processo Civil (Lei 13.105/2015)",
        "tipo": "lei",
        "conteudo": "O Código de Processo Civil estabelece normas processuais civis. Trata da jurisdição, ação, partes, processos, recursos e procedimentos especiais.",
        "fonte": "Planalto",
        "data_publicacao": "2015-03-16"
    },
    {
        "id": 4,
        "titulo": "Código Civil (Lei 10.406/2002)",
        "tipo": "lei",
        "conteudo": "Institui o Código Civil brasileiro. Regula direitos e obrigações de ordem privada concernentes às pessoas, aos bens e às relações jurídicas.",
        "fonte": "Planalto",
        "data_publicacao": "2002-01-10"
    },
    {
        "id": 5,
        "titulo": "Súmula 381 STJ - Juros em Contrato de Mútuo",
        "tipo": "sumula",
        "conteudo": "Nos contratos bancários, é vedado ao julgador conhecer, de ofício, da abusividade das cláusulas.",
        "fonte": "STJ",
        "data_publicacao": "2009-04-22"
    }
]

RESPOSTAS_CHAT_MOCK = {
    "cdc": "Sim, o Código de Defesa do Consumidor (CDC) se aplica a instituições financeiras! Esta posição está consolidada na Súmula 297 do Superior Tribunal de Justiça (STJ), que estabelece: 'O Código de Defesa do Consumidor é aplicável às instituições financeiras'. Isso significa que bancos, financeiras e outras instituições do sistema financeiro devem respeitar os direitos dos consumidores estabelecidos no CDC, como informação clara, proteção contra cláusulas abusivas e direito de arrependimento em determinadas situações.",

    "default": "Como assistente jurídica JUSIA, posso ajudar com informações sobre legislação brasileira, jurisprudência e doutrina. Esta é uma versão de demonstração com dados limitados. Para respostas completas com inteligência artificial real, é necessário configurar a chave da OpenAI API. Os dados mostrados são exemplificativos e servem para demonstrar as funcionalidades do sistema."
}

# ========================================
# Rotas da API
# ========================================

@app.get("/")
async def root():
    """Homepage da API"""
    return {
        "message": "🏛️ JurisIA Pro API - Versão Demo",
        "status": "online",
        "version": "1.0.0-demo",
        "docs": "/docs",
        "modo": "DEMONSTRAÇÃO",
        "limitacoes": [
            "Dados mock (não conecta a bancos reais)",
            "Sem OpenAI (respostas pré-programadas)",
            "Sem cache Redis",
            "Sem busca vetorial Qdrant"
        ],
        "funcionalidades": [
            "GET /health - Health check",
            "POST /api/v1/search/ - Busca jurídica",
            "POST /api/v1/chat/ - Chat com JUSIA",
            "GET /api/v1/stats/ - Estatísticas"
        ]
    }

@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0-demo",
        "services": {
            "api": "online",
            "database": "mock",
            "cache": "mock",
            "vector_db": "mock",
            "openai": "mock"
        }
    }

@app.post("/api/v1/search/", response_model=SearchResponse)
async def search(request: SearchRequest):
    """Busca jurídica com dados mock"""

    inicio = time.time()

    # Simular busca nos documentos mock
    query_lower = request.query.lower()

    resultados = []
    for doc in DOCUMENTOS_MOCK:
        # Busca simples por palavras-chave
        if (query_lower in doc["titulo"].lower() or
            query_lower in doc["conteudo"].lower()):

            # Calcular relevância mock
            relevancia = 0.85 if query_lower in doc["titulo"].lower() else 0.70

            resultados.append(DocumentoJuridico(
                id=doc["id"],
                titulo=doc["titulo"],
                tipo=doc["tipo"],
                conteudo=doc["conteudo"][:200] + "...",
                relevancia=relevancia,
                fonte=doc["fonte"],
                data_publicacao=doc["data_publicacao"]
            ))

    # Limitar resultados
    resultados = resultados[:request.limit]

    # Se não encontrou nada, retornar todos
    if not resultados:
        resultados = [
            DocumentoJuridico(
                id=doc["id"],
                titulo=doc["titulo"],
                tipo=doc["tipo"],
                conteudo=doc["conteudo"][:200] + "...",
                relevancia=0.50,
                fonte=doc["fonte"],
                data_publicacao=doc["data_publicacao"]
            )
            for doc in DOCUMENTOS_MOCK[:request.limit]
        ]

    tempo_ms = int((time.time() - inicio) * 1000)

    return SearchResponse(
        results=resultados,
        total=len(resultados),
        tempo_ms=tempo_ms
    )

@app.post("/api/v1/chat/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat com JUSIA (versão mock)"""

    inicio = time.time()

    # Detectar tipo de pergunta
    query_lower = request.query.lower()

    if "cdc" in query_lower or "consumidor" in query_lower or "banco" in query_lower:
        resposta = RESPOSTAS_CHAT_MOCK["cdc"]
        fontes = [
            {
                "titulo": "Súmula 297 STJ",
                "tipo": "sumula",
                "relevancia": 0.95
            },
            {
                "titulo": "CDC - Lei 8.078/1990",
                "tipo": "lei",
                "relevancia": 0.90
            }
        ]
    else:
        resposta = RESPOSTAS_CHAT_MOCK["default"]
        fontes = [
            {
                "titulo": "Base de Conhecimento Mock",
                "tipo": "info",
                "relevancia": 0.70
            }
        ]

    tempo_ms = int((time.time() - inicio) * 1000)

    return ChatResponse(
        resposta=resposta,
        fontes=fontes,
        tempo_ms=tempo_ms,
        conversa_id=request.conversa_id or f"conv_{int(time.time())}"
    )

@app.get("/api/v1/stats/")
async def stats():
    """Estatísticas do sistema (mock)"""
    return {
        "status": "online",
        "modo": "demonstração",
        "servicos": {
            "api": {
                "status": "online",
                "uptime_seconds": 0,
                "requests_total": 0
            },
            "database": {
                "status": "mock",
                "tipo": "dados_mock",
                "documentos": len(DOCUMENTOS_MOCK)
            },
            "cache": {
                "status": "mock",
                "tipo": "sem_cache"
            },
            "vector_db": {
                "status": "mock",
                "documentos_indexados": len(DOCUMENTOS_MOCK)
            },
            "openai": {
                "status": "mock",
                "modelo": "respostas_pre_programadas"
            }
        },
        "performance": {
            "busca_media_ms": 10,
            "chat_media_ms": 15
        },
        "observacoes": [
            "Esta é uma versão de DEMONSTRAÇÃO",
            "Usa dados mock, não conecta a serviços reais",
            "Para versão completa, siga DEPLOY.md no repositório"
        ]
    }

@app.get("/api/v1/search/suggest/keywords")
async def suggest_keywords(q: Optional[str] = ""):
    """Sugestões de palavras-chave (mock)"""

    keywords = [
        "CDC", "CPC", "Código Civil", "Direito do Consumidor",
        "Súmulas STJ", "Jurisprudência", "Processo Civil",
        "Contratos", "Responsabilidade Civil", "Direito Bancário"
    ]

    if q:
        keywords = [k for k in keywords if q.lower() in k.lower()]

    return {
        "suggestions": keywords[:10],
        "total": len(keywords)
    }

# ========================================
# Inicialização
# ========================================

if __name__ == "__main__":
    import uvicorn

    print("=" * 60)
    print("🏛️  JurisIA Pro - Servidor Demo")
    print("=" * 60)
    print()
    print("⚠️  MODO DEMONSTRAÇÃO")
    print("   - Usa dados MOCK")
    print("   - Não conecta a serviços externos")
    print("   - Sem OpenAI, PostgreSQL, Redis, Qdrant")
    print()
    print("📊 Funcionalidades disponíveis:")
    print("   ✓ GET /health - Health check")
    print("   ✓ POST /api/v1/search/ - Busca jurídica mock")
    print("   ✓ POST /api/v1/chat/ - Chat JUSIA mock")
    print("   ✓ GET /api/v1/stats/ - Estatísticas")
    print()
    print("🌐 Servidor rodando em:")
    print("   http://localhost:8000")
    print("   http://localhost:8000/docs (Swagger UI)")
    print()
    print("=" * 60)
    print()

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
