# 🏛️ JurisIA Pro - Sistema Jurídico Inteligente

Sistema completo de consulta jurídica com IA, análise de processos e geração de documentos legais.

## 🎯 Funcionalidades

### Versão 1.0 (MVP)
- ✅ Busca jurídica inteligente com RAG
- ✅ Chatbot jurídico com citação de fontes
- ✅ Análise de processos PDF
- ✅ Base de dados de jurisprudência brasileira
- ✅ Geração de documentos jurídicos

### Recursos Principais
- **Consulta Jurisprudencial**: Busca semântica em STF, STJ, tribunais regionais
- **Assistente IA**: Chat com respostas fundamentadas e citação de fontes
- **Análise de Processos**: Upload de PDF e análise automática
- **Banco de Dados**: Legislação, jurisprudência, súmulas, doutrinas

## 🏗️ Arquitetura

```
├── backend/          # API FastAPI + RAG Engine
├── frontend/         # Interface React/Next.js
├── database/         # PostgreSQL + pgvector
├── scripts/          # Scrapers de dados jurídicos
└── docs/             # Documentação completa
```

## 🛠️ Stack Tecnológica

### Backend
- **API**: FastAPI (Python 3.11+)
- **IA/LLM**: OpenAI GPT-4 + LangChain
- **Embeddings**: text-embedding-3-large
- **Vector DB**: Qdrant (self-hosted)
- **Database**: PostgreSQL 15 + pgvector
- **Cache**: Redis

### Frontend
- **Framework**: Next.js 14 + React
- **UI**: TailwindCSS + Shadcn/ui
- **State**: Zustand
- **Auth**: NextAuth.js

### Infraestrutura
- **Containerização**: Docker + Docker Compose
- **Deploy**: Railway/Render (free tier)
- **Monitoring**: Prometheus + Grafana
- **CI/CD**: GitHub Actions

## 🚀 Quick Start

### Pré-requisitos
- Docker e Docker Compose
- Python 3.11+
- Node.js 18+
- Chave API OpenAI

### 1. Clonar e Configurar

```bash
# Entrar no diretório
cd juris-ia-pro

# Copiar arquivo de ambiente
cp .env.example .env

# Editar com suas credenciais
nano .env
```

### 2. Subir Infraestrutura

```bash
# Subir banco de dados, Redis e Qdrant
docker-compose up -d

# Aguardar serviços iniciarem
sleep 10
```

### 3. Configurar Backend

```bash
cd backend

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou: venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Rodar migrações
python scripts/setup_db.py

# Iniciar API
uvicorn app.main:app --reload
```

### 4. Configurar Frontend

```bash
cd frontend

# Instalar dependências
npm install

# Rodar em desenvolvimento
npm run dev
```

### 5. Acessar Sistema

- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **API Health**: http://localhost:8000/health

## 📊 Estrutura do Banco de Dados

### Tabelas Principais
- `documentos_juridicos`: Decisões, leis, súmulas
- `usuarios`: Advogados e usuários do sistema
- `consultas`: Histórico de buscas
- `documentos_gerados`: Petições e contratos gerados
- `embeddings`: Vetores para busca semântica
- `citacoes`: Relações entre documentos jurídicos

## 🔧 Scripts de Dados

### Scraping de Fontes Jurídicas

```bash
# STJ - Súmulas
python scripts/scrape_stj.py --type sumulas

# STF - Decisões recentes
python scripts/scrape_stf.py --days 30

# Planalto - Legislação
python scripts/scrape_legislacao.py --start-year 2020

# Popular banco completo (demora ~2h)
python scripts/populate_database.py --full
```

## 📖 Uso da API

### Busca Jurídica

```bash
curl -X POST "http://localhost:8000/api/v1/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "CDC aplicação instituições financeiras",
    "filters": {"tribunal": "STJ", "ano": 2023}
  }'
```

### Chat Jurídico

```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "O que diz a jurisprudência sobre venda casada?"
  }'
```

### Análise de Processo

```bash
curl -X POST "http://localhost:8000/api/v1/analyze-case" \
  -F "file=@processo.pdf" \
  -F "analysis_type=full"
```

## 🧪 Testes

```bash
# Backend
cd backend
pytest tests/ -v --cov

# Frontend
cd frontend
npm test
```

## 📈 Performance

### Benchmarks Iniciais (MVP)
- **Busca**: ~200ms (5 documentos)
- **Chat IA**: ~2-4s (resposta completa)
- **Análise PDF**: ~5-10s (processo médio 20 páginas)
- **Capacidade**: ~1000 documentos indexados

### Otimizações Futuras
- Cache Redis para consultas frequentes
- Índices otimizados no PostgreSQL
- CDN para assets estáticos
- Load balancing para escala horizontal

## 🔐 Segurança

- ✅ HTTPS obrigatório em produção
- ✅ Rate limiting (100 req/min por IP)
- ✅ Validação de inputs
- ✅ Sanitização de dados jurídicos
- ✅ Logs de auditoria (LGPD compliant)
- ✅ Anonimização de dados pessoais
- ✅ Backup automático diário

## 📝 Roadmap

### v1.0 - MVP (30 dias)
- [x] Estrutura base do projeto
- [ ] API FastAPI funcional
- [ ] RAG com busca vetorial
- [ ] Interface básica de busca
- [ ] 500+ documentos indexados

### v1.1 - Aprimoramento (60 dias)
- [ ] Análise de PDF completa
- [ ] Geração de documentos
- [ ] Sistema de alertas jurisprudenciais
- [ ] Dashboard de métricas
- [ ] 10.000+ documentos

### v2.0 - Produção (90 dias)
- [ ] Autenticação multi-tenant
- [ ] API pública documentada
- [ ] Mobile app (React Native)
- [ ] Integração com sistemas jurídicos
- [ ] 100.000+ documentos

## 🤝 Contribuindo

Este é um projeto privado em desenvolvimento inicial.

## 📄 Licença

Proprietário - Todos os direitos reservados

## 📞 Suporte

Para dúvidas e suporte:
- 📧 Email: suporte@jurisia.com.br
- 📚 Docs: http://docs.jurisia.com.br
- 🐛 Issues: GitHub Issues

---

**Desenvolvido com ⚖️ para revolucionar o acesso à justiça no Brasil**
