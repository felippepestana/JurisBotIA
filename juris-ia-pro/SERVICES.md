# 🔧 Serviços do JurisIA Pro

Documentação completa dos serviços implementados no backend.

## 📋 Índice

1. [Cache Service (Redis)](#cache-service)
2. [Vector Service (Qdrant)](#vector-service)
3. [OpenAI Service](#openai-service)
4. [PDF Service](#pdf-service)
5. [Scrapers](#scrapers)

---

## 🗄️ Cache Service

**Arquivo:** `backend/app/services/cache_service.py`

### Visão Geral
Sistema de cache baseado em Redis para otimizar performance e reduzir custos de API.

### Recursos
- ✅ Cache key-value com TTL customizado
- ✅ Decorador `@cached` para funções
- ✅ Limpeza por padrões (wildcards)
- ✅ Estatísticas de uso
- ✅ Fallback gracioso quando Redis indisponível

### API

#### Verificar Disponibilidade
```python
from app.services.cache_service import cache_service

if cache_service.is_available():
    print("Redis disponível!")
```

#### Set/Get/Delete
```python
# Set com TTL
cache_service.set("user:123", {"name": "João"}, ttl=3600)

# Get
data = cache_service.get("user:123")

# Delete
cache_service.delete("user:123")
```

#### Decorador @cached
```python
from app.services.cache_service import cached

@cached(prefix="search", ttl=300)
async def search_documents(query: str, limit: int):
    # A função só executa se não houver cache
    results = expensive_search(query, limit)
    return results

# Primeira chamada: executa e cacheia
results1 = await search_documents("CDC", 10)

# Segunda chamada: retorna do cache (rápido!)
results2 = await search_documents("CDC", 10)
```

#### Limpar Padrões
```python
# Limpar todas as chaves que começam com "search:"
cache_service.clear_pattern("search:*")

# Limpar tudo do usuário 123
cache_service.clear_pattern("user:123:*")
```

#### Estatísticas
```python
stats = cache_service.get_stats()
print(f"Total de chaves: {stats['total_keys']}")
print(f"Memória usada: {stats['used_memory_human']}")
print(f"Hit rate: {stats.get('hit_rate', 'N/A')}")
```

### Configuração

**Variáveis de Ambiente (.env):**
```env
REDIS_URL=redis://localhost:6379/0
CACHE_TTL_SECONDS=300
```

### Métricas
- **Tempo de resposta com cache:** ~5-10ms
- **Redução de custos OpenAI:** ~80% (menos chamadas de embedding)
- **Hit rate esperado:** >75% em produção

---

## 🔍 Vector Service

**Arquivo:** `backend/app/services/vector_service.py`

### Visão Geral
Busca semântica usando Qdrant e embeddings da OpenAI para encontrar documentos juridicamente relevantes.

### Recursos
- ✅ Busca vetorial semântica
- ✅ Indexação individual e em batch
- ✅ Filtros por metadados (tipo_documento, instância)
- ✅ Score threshold configurável
- ✅ Operações CRUD completas

### API

#### Verificar Disponibilidade
```python
from app.services.vector_service import vector_service

if vector_service.is_available():
    info = vector_service.collection_info()
    print(f"Documentos indexados: {info['vectors_count']}")
```

#### Busca Semântica
```python
# Busca básica
results = vector_service.search(
    query="CDC aplicável aos bancos",
    limit=10,
    score_threshold=0.7
)

for doc in results:
    print(f"{doc['titulo']} - Score: {doc['similarity_score']:.3f}")
```

#### Busca com Filtros
```python
# Filtrar por tipo e instância
results = vector_service.search(
    query="dano moral",
    limit=5,
    filters={
        "tipo_documento": "acordao",
        "instancia": "STJ"
    },
    score_threshold=0.75
)
```

#### Indexar Documento Único
```python
vector_service.add_document(
    document_id="lei_cdc_001",
    text="O Código de Defesa do Consumidor é aplicável...",
    metadata={
        "titulo": "CDC - Lei 8.078/1990",
        "tipo_documento": "lei",
        "instancia": "FEDERAL",
        "data_publicacao": "1990-09-11"
    }
)
```

#### Indexar em Batch (Recomendado)
```python
documents = [
    {
        "id": "doc1",
        "titulo": "Lei 8.078",
        "conteudo_completo": "CDC...",
        "tipo_documento": "lei"
    },
    {
        "id": "doc2",
        "titulo": "Súmula 297",
        "conteudo_completo": "...",
        "tipo_documento": "sumula"
    }
]

result = vector_service.add_documents_batch(documents)
print(f"Indexados: {result['indexed']}")
print(f"Falhados: {result['failed']}")
```

#### Atualizar Documento
```python
vector_service.update_document(
    document_id="lei_cdc_001",
    text="Novo conteúdo atualizado...",
    metadata={...}
)
```

#### Deletar Documentos
```python
# Deletar um
vector_service.delete_document("lei_cdc_001")

# Deletar múltiplos
vector_service.delete_documents(["doc1", "doc2", "doc3"])
```

### Configuração

**Variáveis de Ambiente (.env):**
```env
QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION=juris_documents
VECTOR_DIMENSION=3072
RAG_SIMILARITY_THRESHOLD=0.7
```

### Métricas
- **Dimensões do embedding:** 3072 (text-embedding-3-large)
- **Tempo de busca:** ~300-800ms (incluindo embedding)
- **Precisão:** Alta para queries jurídicas
- **Capacidade:** Milhões de documentos (escalável)

### Como Funciona

1. **Indexação:**
   - Documento → OpenAI Embedding (3072 dims) → Qdrant

2. **Busca:**
   - Query → OpenAI Embedding → Qdrant Search → Top K resultados

3. **Filtros:**
   - Aplicados no Qdrant antes do ranking
   - Suporta filtros exatos e ranges

---

## 🤖 OpenAI Service

**Arquivo:** `backend/app/services/openai_service.py`

### Visão Geral
Integração completa com OpenAI para embeddings, chat e análise jurídica.

### Recursos
- ✅ Geração de embeddings (text-embedding-3-large)
- ✅ Chat jurídico com RAG
- ✅ Análise de documentos legais
- ✅ Geração de documentos (petições, contratos)
- ✅ Retry automático com exponential backoff
- ✅ Estimativa de custos

### API

#### Gerar Embeddings
```python
from app.services.openai_service import openai_service

text = "Código de Defesa do Consumidor"
embedding = openai_service.generate_embedding(text)

print(f"Dimensões: {len(embedding)}")  # 3072
```

#### Chat Jurídico com RAG
```python
# Documentos relevantes (vindos da busca vetorial)
documents = [
    {
        "titulo": "Súmula 297 STJ",
        "conteudo_completo": "O CDC é aplicável...",
        "tipo_documento": "sumula"
    }
]

response, confidence = openai_service.generate_legal_response(
    query="O CDC se aplica a bancos?",
    documents=documents,
    max_tokens=500
)

print(f"Resposta (conf: {confidence:.2f}):")
print(response)
```

#### Analisar Documento Legal
```python
document_text = """
AÇÃO DE COBRANÇA
Autor: João da Silva
Réu: Banco XYZ
Valor: R$ 10.000,00
...
"""

analysis = openai_service.analyze_legal_document(
    document_text=document_text,
    analysis_type="completa",  # ou "rapida", "identificacao", "riscos"
    focus_areas=["CDC", "consumidor"]
)

print("Tipo:", analysis["document_type"])
print("Área:", analysis["legal_area"])
print("Questões:", analysis["key_issues"])
print("Framework:", analysis["applicable_framework"])
```

#### Gerar Documento Jurídico
```python
# Gerar petição inicial
parameters = {
    "autor": "Maria Santos",
    "reu": "Empresa XYZ Ltda",
    "facts": "Cobrança indevida de tarifa bancária...",
    "pedidos": ["Restituição em dobro", "Danos morais"],
    "valor_causa": "R$ 15.000,00"
}

document = openai_service.generate_legal_document(
    document_type="inicial",
    parameters=parameters,
    template="consumidor"  # opcional
)

print(document)  # Petição inicial formatada
```

### Tipos de Análise

#### 1. Análise Rápida
- Identificação básica do tipo de documento
- Partes envolvidas
- Área do direito
- ~500 tokens

#### 2. Análise Completa (padrão)
- Tudo da análise rápida +
- Questões jurídicas detalhadas
- Framework legal aplicável
- Possíveis argumentos
- ~1500 tokens

#### 3. Identificação de Riscos
- Foco em riscos e vulnerabilidades
- Pontos fracos da argumentação
- Precedentes desfavoráveis
- ~1000 tokens

### Tipos de Documentos Geráveis

1. **Petição Inicial** (`inicial`)
2. **Contestação** (`contestacao`)
3. **Recurso** (`recurso`)
4. **Memoriais** (`memoriais`)
5. **Contrato** (`contrato`)
6. **Parecer Jurídico** (`parecer`)

### Configuração

**Variáveis de Ambiente (.env):**
```env
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4-turbo-preview
OPENAI_EMBEDDING_MODEL=text-embedding-3-large
OPENAI_MAX_TOKENS=2000
OPENAI_TEMPERATURE=0.3
```

### Custos Estimados (por 1000 requisições)

| Operação | Tokens | Custo USD |
|----------|--------|-----------|
| Embedding | ~500 | $0.10 |
| Chat simples | ~1000 | $0.30 |
| Análise completa | ~2500 | $0.75 |
| Geração documento | ~3000 | $0.90 |

**Otimização:** Com cache Redis, redução de ~80% nos custos de embedding.

---

## 📄 PDF Service

**Arquivo:** `backend/app/services/pdf_service.py`

### Visão Geral
Extração e análise de PDFs jurídicos (processos, petições, decisões).

### Recursos
- ✅ Validação de PDF (tamanho, páginas, formato)
- ✅ Extração de texto (PyPDF2 + pdfplumber)
- ✅ Análise estruturada de processos
- ✅ Identificação automática de partes e valores
- ✅ Suporte a PDFs grandes (até 20MB, 100 páginas)

### API

#### Validar PDF
```python
from app.services.pdf_service import pdf_service

is_valid, message = pdf_service.validate_pdf(
    file_content=pdf_bytes,
    filename="processo.pdf",
    max_size_mb=20
)

if not is_valid:
    print(f"Erro: {message}")
```

#### Extrair Texto
```python
# Método 1: PyPDF2 (mais rápido)
text = pdf_service.extract_text_pypdf(pdf_bytes)

# Método 2: pdfplumber (mais preciso)
text = pdf_service.extract_text_pdfplumber(pdf_bytes)

# Método automático (tenta pdfplumber, fallback PyPDF2)
text = pdf_service.extract_text(pdf_bytes, filename="processo.pdf")
```

#### Analisar Processo Judicial
```python
analysis = pdf_service.analyze_legal_pdf(
    pdf_content=pdf_bytes,
    filename="processo_12345.pdf",
    analysis_type="completa"
)

print("Status:", analysis["status"])
print("Texto extraído:", len(analysis["extracted_text"]), "caracteres")
print("Páginas:", analysis["metadata"]["pages"])
print("Análise:", analysis["analysis"])
```

### Estrutura da Análise

```python
{
    "status": "success",
    "filename": "processo.pdf",
    "extracted_text": "AÇÃO DE COBRANÇA...",
    "metadata": {
        "pages": 15,
        "file_size": "2.5 MB",
        "extraction_method": "pdfplumber"
    },
    "analysis": {
        "document_type": "Petição Inicial",
        "legal_area": "Direito do Consumidor",
        "parties": ["João Silva", "Banco XYZ"],
        "key_issues": ["Tarifa bancária abusiva"],
        "applicable_framework": [
            {"lei": "CDC Art. 51", "aplicabilidade": "Alta"}
        ],
        "recommendations": ["Citar Súmula 297"],
        "confidence_score": 0.87
    }
}
```

### Limites e Restrições

- **Tamanho máximo:** 20 MB (configurável)
- **Páginas máximas:** 100 páginas
- **Formatos suportados:** PDF 1.4+
- **Timeout:** 30 segundos por PDF

### Configuração

**Variáveis de Ambiente (.env):**
```env
PDF_MAX_SIZE_MB=20
PDF_MAX_PAGES=100
PDF_EXTRACTION_TIMEOUT=30
```

---

## 🕷️ Scrapers

**Arquivos:**
- `backend/app/scrapers/base_scraper.py`
- `backend/app/scrapers/planalto_scraper.py`
- `backend/app/scrapers/stj_scraper.py`

### Visão Geral
Sistema de coleta automatizada de dados jurídicos de fontes oficiais.

### Base Scraper

Classe abstrata com funcionalidades comuns:
- ✅ Retry automático (3 tentativas)
- ✅ Rate limiting
- ✅ Parse HTML com BeautifulSoup
- ✅ Normalização de datas
- ✅ Progress logging

```python
from app.scrapers.base_scraper import BaseScraper

class MeuScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            source_name="MinhaFonte",
            base_url="https://exemplo.com"
        )

    def scrape(self, **kwargs):
        # Implementar lógica específica
        html = self.fetch_page(url)
        soup = self.parse_html(html)
        # ...
        self.save_document(document_dict)
        return self.get_documents()
```

### Planalto Scraper

**Coleta:** Legislação federal (leis, decretos, MPs)

**Uso:**
```python
from app.scrapers.planalto_scraper import PlanaltoScraper

scraper = PlanaltoScraper()

# Scraping de leis importantes pré-definidas
documents = scraper.scrape(scrape_mode="important")
# Retorna 7 leis: CDC, CPC, CC, ECA, etc.
```

**Leis Coletadas:**
1. Lei 8.078/1990 - Código de Defesa do Consumidor
2. Lei 13.105/2015 - Código de Processo Civil
3. Lei 10.406/2002 - Código Civil
4. Lei 8.069/1990 - ECA
5. Lei 9.099/1995 - Juizados Especiais
6. Lei 4.737/1965 - Código Eleitoral
7. E outras...

### STJ Scraper

**Coleta:** Súmulas e jurisprudência do STJ

**Uso:**
```python
from app.scrapers.stj_scraper import STJScraper

scraper = STJScraper()

# Súmulas importantes
documents = scraper.scrape(scrape_mode="sumulas", limit=8)

# Jurisprudência relevante
documents = scraper.scrape(scrape_mode="jurisprudencia", limit=10)
```

**Súmulas Coletadas:**
- Súmula 297: CDC aplicável a instituições financeiras
- Súmula 385: Dano moral e cadastro de crédito
- Súmula 37: Cumulação de danos
- E outras...

### Estrutura de Documento Retornado

```python
{
    "id": "lei_cdc_001",
    "titulo": "Lei 8.078/1990 - Código de Defesa do Consumidor",
    "tipo_documento": "lei",  # lei, sumula, acordao, decreto
    "numero_processo": "Lei 8.078/1990",
    "conteudo_completo": "Texto completo da lei...",
    "ementa": "Dispõe sobre proteção do consumidor...",
    "orgao_emissor": "Presidência da República",
    "instancia": "FEDERAL",  # FEDERAL, STJ, STF, OUTRA
    "data_publicacao": datetime(1990, 9, 11),
    "palavras_chave": ["consumidor", "direito", "código"],
    "assuntos": ["Direito do Consumidor"],
    "metadados": {
        "artigos_principais": ["Art. 1º...", "Art. 2º..."],
        "tipo_legislacao": "lei_federal"
    },
    "relevancia_score": 0.95,
    "citacoes_count": 1247,
    "fonte_original": "Planalto - Presidência da República",
    "url_fonte": "https://www.planalto.gov.br/...",
    "scraped_at": datetime.utcnow(),
    "source": "Planalto"
}
```

### Rate Limiting

Todos os scrapers implementam rate limiting para respeitar servidores:

```python
# Aguarda entre requisições
scraper.rate_limit(seconds=0.5)  # Aguarda 500ms
```

---

## 🔄 Integração entre Serviços

### Fluxo de Busca Completo

```
1. User Query
   ↓
2. Cache Service (check)
   ↓ (miss)
3. Vector Service (search)
   ↓
4. OpenAI Service (embedding)
   ↓
5. Qdrant (similarity search)
   ↓
6. Cache Service (store)
   ↓
7. Return Results
```

### Fluxo de Indexação

```
1. Scrapers (collect)
   ↓
2. Data Processing
   ↓
3. OpenAI Service (embeddings batch)
   ↓
4. Vector Service (index)
   ↓
5. Qdrant (store vectors)
   ↓
6. PostgreSQL (store metadata)
```

### Fluxo de Chat RAG

```
1. User Question
   ↓
2. Vector Service (find relevant docs)
   ↓
3. OpenAI Service (generate response with context)
   ↓
4. Return Response + Sources
```

---

## 🚀 Quick Start Integrado

```python
# 1. Setup inicial
from app.services.cache_service import cache_service
from app.services.vector_service import vector_service
from app.services.openai_service import openai_service

# 2. Coletar dados
from app.scrapers.planalto_scraper import PlanaltoScraper
scraper = PlanaltoScraper()
docs = scraper.scrape(scrape_mode="important")

# 3. Indexar no Qdrant
result = vector_service.add_documents_batch(docs)
print(f"Indexados: {result['indexed']}")

# 4. Buscar
results = vector_service.search("CDC bancos", limit=5)

# 5. Chat com RAG
response, conf = openai_service.generate_legal_response(
    query="O CDC se aplica a bancos?",
    documents=results
)
print(response)
```

---

## 📊 Monitoramento

### Métricas Recomendadas

**Cache:**
- Hit rate (%)
- Tempo médio de resposta
- Memória usada

**Vector Search:**
- Tempo de busca
- Número de resultados
- Score médio

**OpenAI:**
- Tokens consumidos
- Custo estimado
- Taxa de erro

**Scrapers:**
- Documentos coletados
- Taxa de sucesso
- Tempo de execução

---

## 🆘 Troubleshooting

Consulte **[TESTING.md](./TESTING.md)** para:
- Testes de cada serviço
- Resolução de problemas comuns
- Validação de configuração
- Benchmarks de performance

---

## 📚 Documentação Adicional

- **[README.md](./README.md)** - Visão geral do projeto
- **[TESTING.md](./TESTING.md)** - Guia completo de testes
- **[FEATURES.md](./FEATURES.md)** - Funcionalidades detalhadas (se existir)

---

**Desenvolvido com ⚖️ para revolucionar o acesso à justiça no Brasil**
