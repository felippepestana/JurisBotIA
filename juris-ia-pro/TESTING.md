# 🧪 Guia de Testes - JurisIA Pro

Este documento descreve como testar todas as funcionalidades do sistema JurisIA Pro.

## 📋 Índice

1. [Setup Rápido](#setup-rápido)
2. [Testes de Serviços](#testes-de-serviços)
3. [Testes de API](#testes-de-api)
4. [Testes de Performance](#testes-de-performance)
5. [Troubleshooting](#troubleshooting)

---

## 🚀 Setup Rápido

### Opção 1: Script Automatizado (Recomendado)

```bash
cd juris-ia-pro/backend
python scripts/run_full_setup.py
```

Este script irá:
- ✅ Verificar status de todos os serviços
- ✅ Configurar o banco de dados PostgreSQL
- ✅ Popular com dados dos scrapers
- ✅ Indexar documentos no Qdrant
- ✅ Executar testes básicos
- ✅ Mostrar relatório completo

### Opção 2: Setup Manual

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com suas configurações

# 3. Setup do banco
python scripts/setup_db.py

# 4. Popular dados
python scripts/populate_database.py

# 5. Iniciar servidor
uvicorn app.main:app --reload
```

---

## 🔍 Testes de Serviços

### 1. Cache Service (Redis)

**Teste de Conexão:**
```bash
python -c "
from app.services.cache_service import cache_service
print('Redis disponível:', cache_service.is_available())
print('Stats:', cache_service.get_stats())
"
```

**Teste de Operações:**
```python
from app.services.cache_service import cache_service

# Set
cache_service.set('test_key', {'data': 'test'}, ttl=60)

# Get
value = cache_service.get('test_key')
print('Valor recuperado:', value)

# Delete
cache_service.delete('test_key')

# Clear por padrão
cache_service.clear_pattern('test:*')
```

**Resultado Esperado:**
- ✅ Redis disponível: True
- ✅ Stats mostram conexões ativas e memória
- ✅ Get retorna valor salvo com set
- ✅ Delete remove a chave

---

### 2. Vector Service (Qdrant)

**Teste de Conexão:**
```bash
python -c "
from app.services.vector_service import vector_service
print('Qdrant disponível:', vector_service.is_available())
print('Collection info:', vector_service.collection_info())
"
```

**Teste de Busca:**
```python
from app.services.vector_service import vector_service

# Busca simples
results = vector_service.search(
    query="CDC instituições financeiras",
    limit=5,
    score_threshold=0.7
)

print(f"Encontrados: {len(results)} documentos")
for doc in results:
    print(f"- {doc['titulo']} (Score: {doc['similarity_score']:.3f})")
```

**Teste de Indexação:**
```python
from app.services.vector_service import vector_service

# Indexar documento único
vector_service.add_document(
    document_id="test_001",
    text="Código de Defesa do Consumidor aplicável aos bancos",
    metadata={
        "tipo_documento": "lei",
        "instancia": "FEDERAL"
    }
)

# Indexar batch
documents = [
    {
        "id": "doc1",
        "titulo": "Lei 8.078",
        "conteudo_completo": "CDC...",
        "tipo_documento": "lei"
    }
]
result = vector_service.add_documents_batch(documents)
print(f"Indexados: {result['indexed']}, Falhados: {result['failed']}")
```

**Resultado Esperado:**
- ✅ Qdrant disponível: True
- ✅ Collection existe com documentos indexados
- ✅ Busca retorna resultados relevantes
- ✅ Scores de similaridade > 0.7

---

### 3. OpenAI Service

**Teste de Embeddings:**
```python
from app.services.openai_service import openai_service

# Gerar embedding
text = "Direito do consumidor"
embedding = openai_service.generate_embedding(text)

print(f"Embedding gerado: {len(embedding)} dimensões")
print(f"Primeiros valores: {embedding[:5]}")
```

**Teste de Chat Jurídico:**
```python
from app.services.openai_service import openai_service

# Gerar resposta
documents = [
    {
        "titulo": "CDC - Lei 8.078/1990",
        "conteudo_completo": "O Código de Defesa do Consumidor...",
        "tipo_documento": "lei"
    }
]

response, confidence = openai_service.generate_legal_response(
    query="O CDC se aplica a bancos?",
    documents=documents
)

print(f"Resposta (confiança: {confidence:.2f}):")
print(response)
```

**Resultado Esperado:**
- ✅ Embedding com 3072 dimensões
- ✅ Resposta jurídica contextualizada
- ✅ Confiança entre 0.0 e 1.0
- ✅ Citações dos documentos fornecidos

---

## 🌐 Testes de API

### Setup
```bash
# Iniciar servidor
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Em outro terminal, testar endpoints
```

### 1. Health Check

```bash
curl http://localhost:8000/health
```

**Resposta esperada:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "services": {
    "database": "available",
    "redis": "available",
    "qdrant": "available",
    "openai": "available"
  }
}
```

---

### 2. Busca de Documentos

**POST /api/v1/search/**

```bash
curl -X POST http://localhost:8000/api/v1/search/ \
  -H "Content-Type: application/json" \
  -d '{
    "query": "CDC instituições financeiras",
    "limit": 5,
    "tipo_documento": "lei"
  }'
```

**Resposta esperada:**
```json
{
  "query": "CDC instituições financeiras",
  "total": 15,
  "results": [
    {
      "id": "lei_cdc_001",
      "titulo": "Lei 8.078/1990 - Código de Defesa do Consumidor",
      "tipo_documento": "lei",
      "ementa": "Dispõe sobre proteção do consumidor...",
      "relevancia_score": 0.95,
      "similarity_score": 0.87,
      "highlight": "...O CDC é aplicável às instituições financeiras..."
    }
  ],
  "time_ms": 45,
  "filters_applied": {
    "tipo_documento": "lei"
  }
}
```

**Teste de Cache:**
```bash
# Primeira requisição (sem cache)
time curl -X POST http://localhost:8000/api/v1/search/ \
  -H "Content-Type: application/json" \
  -d '{"query": "CDC"}' | jq '.time_ms'

# Segunda requisição (com cache) - deve ser mais rápida
time curl -X POST http://localhost:8000/api/v1/search/ \
  -H "Content-Type: application/json" \
  -d '{"query": "CDC"}' | jq '.time_ms'
```

---

### 3. Chat Jurídico

**POST /api/v1/chat/**

```bash
curl -X POST http://localhost:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -d '{
    "query": "O CDC se aplica a bancos?",
    "conversation_id": "test-123"
  }'
```

**Resposta esperada:**
```json
{
  "response": "Sim, conforme a Súmula 297 do STJ, o Código de Defesa do Consumidor é aplicável às instituições financeiras...",
  "confidence_score": 0.92,
  "sources": [
    {
      "id": "sumula_297",
      "titulo": "STJ - Súmula 297",
      "relevance": 0.95
    }
  ],
  "conversation_id": "test-123",
  "time_ms": 1250
}
```

---

### 4. Análise de PDF

**POST /api/v1/analyze/pdf**

```bash
curl -X POST http://localhost:8000/api/v1/analyze/pdf \
  -F "file=@processo.pdf" \
  -F "analysis_type=completa"
```

**Resposta esperada:**
```json
{
  "analysis": {
    "tipo_processo": "Ação de Cobrança",
    "area_direito": "Direito do Consumidor",
    "partes": ["XPTO Ltda", "João da Silva"],
    "valor_causa": "R$ 15.000,00",
    "principais_questoes": [
      "Cobrança indevida de tarifas bancárias"
    ]
  },
  "legal_framework": [
    {
      "documento": "CDC - Art. 51",
      "aplicabilidade": "Alta",
      "fundamento": "Abusividade de cláusulas..."
    }
  ],
  "recommendations": [
    "Alegar violação do CDC artigo 51",
    "Citar Súmula 297 do STJ"
  ],
  "similar_cases": [...],
  "time_ms": 3500
}
```

---

### 5. Autocompletar Busca

**GET /api/v1/search/suggest/keywords**

```bash
curl "http://localhost:8000/api/v1/search/suggest/keywords?q=cdc"
```

**Resposta esperada:**
```json
{
  "query": "cdc",
  "suggestions": [
    "CDC",
    "código de defesa do consumidor",
    "cdc instituições financeiras",
    "cdc bancos"
  ]
}
```

---

## ⚡ Testes de Performance

### 1. Teste de Carga - Busca

```bash
# Instalar Apache Bench
sudo apt-get install apache2-utils

# Teste com 100 requisições, 10 concorrentes
ab -n 100 -c 10 -p search_payload.json -T application/json \
  http://localhost:8000/api/v1/search/
```

**search_payload.json:**
```json
{"query": "CDC", "limit": 10}
```

**Métricas esperadas:**
- Requests per second: > 50 rps
- Time per request: < 200ms (com cache)
- Time per request: < 1000ms (sem cache)
- Failed requests: 0

---

### 2. Teste de Cache Hit Rate

```python
from app.services.cache_service import cache_service
import time

# Fazer múltiplas requisições
queries = ["CDC", "dano moral", "superendividamento"] * 20

start_time = time.time()
for query in queries:
    # Simular busca com cache
    pass
elapsed = time.time() - start_time

# Ver estatísticas
stats = cache_service.get_stats()
print(f"Tempo total: {elapsed:.2f}s")
print(f"Hit rate esperado: > 80%")
```

---

### 3. Benchmark de Embeddings

```python
import time
from app.services.openai_service import openai_service

texts = [
    "Código de Defesa do Consumidor",
    "Direito do trabalho",
    "Responsabilidade civil"
] * 10

start = time.time()
for text in texts:
    openai_service.generate_embedding(text)
elapsed = time.time() - start

print(f"Tempo total: {elapsed:.2f}s")
print(f"Tempo médio por embedding: {elapsed/len(texts)*1000:.0f}ms")
print(f"Taxa esperada: < 500ms por embedding")
```

---

## 🔧 Troubleshooting

### Redis não conecta

**Problema:** `Redis não disponível`

**Solução:**
```bash
# Verificar se Redis está rodando
docker ps | grep redis

# Iniciar Redis
docker-compose up -d redis

# Testar conexão
redis-cli ping
# Deve retornar: PONG
```

---

### Qdrant não conecta

**Problema:** `Qdrant não disponível`

**Solução:**
```bash
# Verificar se Qdrant está rodando
docker ps | grep qdrant

# Iniciar Qdrant
docker-compose up -d qdrant

# Testar API
curl http://localhost:6333/collections
```

---

### OpenAI API Key inválida

**Problema:** `OpenAI não disponível`

**Solução:**
```bash
# Verificar .env
cat .env | grep OPENAI_API_KEY

# Validar chave
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

---

### Banco de dados não inicializa

**Problema:** `Database setup failed`

**Solução:**
```bash
# Verificar conexão
psql -h localhost -U juris_user -d juris_ia_pro

# Recriar banco
python scripts/setup_db.py

# Verificar tabelas
python -c "
from sqlalchemy import inspect, create_engine
from app.core.config import settings
engine = create_engine(settings.DATABASE_URL)
inspector = inspect(engine)
print('Tabelas:', inspector.get_table_names())
"
```

---

### Busca retorna poucos resultados

**Problema:** Busca vetorial retorna 0 ou poucos resultados

**Solução:**
```python
# 1. Verificar se documentos foram indexados
from app.services.vector_service import vector_service
info = vector_service.collection_info()
print(f"Documentos indexados: {info.get('vectors_count', 0)}")

# 2. Reduzir threshold de similaridade
results = vector_service.search(
    query="sua busca",
    limit=10,
    score_threshold=0.5  # Reduzir de 0.7 para 0.5
)

# 3. Re-indexar documentos
from scripts.populate_database import DatabasePopulator
populator = DatabasePopulator()
populator.collect_from_scrapers()
populator.index_to_vector_db()
```

---

## 📊 Métricas de Sucesso

### Funcionalidade
- ✅ Todos os endpoints retornam 200 OK
- ✅ Busca retorna resultados relevantes
- ✅ Cache funciona corretamente
- ✅ Vector search retorna scores > 0.7

### Performance
- ✅ Busca com cache: < 50ms
- ✅ Busca sem cache: < 1000ms
- ✅ Chat response: < 2000ms
- ✅ PDF analysis: < 5000ms

### Qualidade
- ✅ Respostas juridicamente corretas
- ✅ Citações de fontes apropriadas
- ✅ Confiança > 0.7 para respostas
- ✅ Zero erros em produção

---

## 🎯 Próximos Passos

Após validar todos os testes:

1. **Deploy em Produção**
   - Configurar ambiente de produção
   - Setup de monitoring (Prometheus, Grafana)
   - Configurar logs centralizados

2. **Testes Adicionais**
   - Testes de integração end-to-end
   - Testes de segurança
   - Testes de carga em produção

3. **Otimizações**
   - Tuning de cache TTL
   - Otimização de índices Qdrant
   - Batch processing para embeddings

---

## 📞 Suporte

Para problemas ou dúvidas:
- 📧 Email: suporte@jurisia.pro
- 📚 Documentação: ./FEATURES.md
- 🐛 Issues: GitHub Issues
