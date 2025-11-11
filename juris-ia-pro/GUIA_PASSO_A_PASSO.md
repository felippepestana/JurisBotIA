# 🎯 Guia Passo a Passo DETALHADO - JurisIA Pro

## 📋 Índice

1. [Acessar os Arquivos do Projeto](#1-acessar-os-arquivos-do-projeto)
2. [Entender o Projeto](#2-entender-o-projeto)
3. [Preparar o Ambiente](#3-preparar-o-ambiente)
4. [Configurar o Sistema](#4-configurar-o-sistema)
5. [Fazer o Deploy](#5-fazer-o-deploy)
6. [Testar o Sistema](#6-testar-o-sistema)
7. [Solução de Problemas](#7-solução-de-problemas)

---

# 1. Acessar os Arquivos do Projeto

## Opção A: Acessar via GitHub (Navegador Web)

### Passo 1.1: Abrir o GitHub

1. Abra seu navegador (Chrome, Firefox, Edge, Safari)
2. Digite na barra de endereço:
   ```
   https://github.com/felippepestana/supabase
   ```
3. Pressione ENTER

### Passo 1.2: Navegar para o Branch Correto

1. Na página do GitHub, procure o botão de **branch** (geralmente mostra "main" ou "master")
2. Clique nesse botão
3. Na caixa de busca que aparecer, digite:
   ```
   claude/jusbrasil-web-chatbot-011CUfRi9oNUUVEuxfS4fz1N
   ```
4. Clique no branch que aparecer na lista

### Passo 1.3: Entrar na Pasta do Projeto

1. Você verá uma lista de pastas e arquivos
2. Procure a pasta chamada **`juris-ia-pro`**
3. **Clique** nessa pasta

### Passo 1.4: Visualizar os Documentos

Agora você verá todos os arquivos do projeto. Para ler qualquer documento:

1. **Clique** no nome do arquivo (ex: `DEPLOY.md`)
2. O GitHub vai mostrar o conteúdo formatado
3. Para voltar, clique no botão "voltar" do navegador

**Documentos disponíveis:**
- `INDEX.md` - Índice completo
- `FINAL_SUMMARY.md` - Resumo executivo
- `DEPLOY.md` - Guia de deployment
- `CHECKLIST.md` - Checklist
- `README.md` - Visão geral
- E mais 5 documentos técnicos

---

## Opção B: Acessar Localmente (Seu Computador)

### Passo 1.1: Verificar se Tem Git Instalado

**No Windows:**
1. Pressione `Windows + R`
2. Digite `cmd` e pressione ENTER
3. Digite: `git --version`
4. Pressione ENTER

**No Mac/Linux:**
1. Abra o Terminal
2. Digite: `git --version`
3. Pressione ENTER

**Resultado esperado:**
- ✅ Se aparecer algo como "git version 2.x.x" → Git está instalado
- ❌ Se aparecer erro → Precisa instalar o Git

**Como instalar Git (se necessário):**
- Windows: Baixe em https://git-scm.com/download/win
- Mac: Digite no terminal: `brew install git` (ou baixe em https://git-scm.com/download/mac)
- Linux: `sudo apt install git` (Ubuntu/Debian) ou `sudo yum install git` (RedHat/CentOS)

### Passo 1.2: Clonar o Repositório

**IMPORTANTE:** Escolha onde salvar o projeto. Vou usar a pasta "Documentos" como exemplo.

**No Windows:**
```cmd
# Abra o CMD (Prompt de Comando)
# Pressione Windows + R, digite "cmd", pressione ENTER

# Navegue para a pasta Documentos
cd %USERPROFILE%\Documents

# Clone o repositório
git clone https://github.com/felippepestana/supabase.git

# Aguarde o download (pode demorar 1-2 minutos)
```

**No Mac/Linux:**
```bash
# Abra o Terminal

# Navegue para a pasta Documentos
cd ~/Documents

# Clone o repositório
git clone https://github.com/felippepestana/supabase.git

# Aguarde o download
```

### Passo 1.3: Trocar para o Branch Correto

```bash
# Entre na pasta que foi baixada
cd supabase

# Mude para o branch do projeto
git checkout claude/jusbrasil-web-chatbot-011CUfRi9oNUUVEuxfS4fz1N

# Você verá uma mensagem confirmando a troca
```

### Passo 1.4: Entrar na Pasta do Projeto

```bash
# Entre na pasta do JurisIA Pro
cd juris-ia-pro

# Liste os arquivos disponíveis
ls
```

**Você verá:**
```
CHECKLIST.md
DEPLOY.md
FEATURES.md
FINAL_SUMMARY.md
INDEX.md
QUICKSTART.md
README.md
SERVICES.md
STATUS.md
TESTING.md
backend/
database/
frontend/
deploy.sh
docker-compose.prod.yml
...
```

### Passo 1.5: Ler os Documentos

**Opção 1: Abrir com Editor de Texto**

**No Windows:**
```cmd
# Abrir com Notepad
notepad FINAL_SUMMARY.md

# Ou com seu editor preferido
code FINAL_SUMMARY.md    (VS Code)
```

**No Mac:**
```bash
# Abrir com TextEdit
open -a TextEdit FINAL_SUMMARY.md

# Ou com VS Code
code FINAL_SUMMARY.md
```

**No Linux:**
```bash
# Abrir com editor padrão
xdg-open FINAL_SUMMARY.md

# Ou com VS Code
code FINAL_SUMMARY.md

# Ou com Gedit
gedit FINAL_SUMMARY.md
```

**Opção 2: Ler no Terminal**

```bash
# Visualizar no terminal (mais simples)
cat FINAL_SUMMARY.md

# Visualizar com paginação (pode rolar com setas)
less FINAL_SUMMARY.md
# Pressione 'q' para sair

# Visualizar o começo do arquivo
head -50 FINAL_SUMMARY.md

# Visualizar o fim do arquivo
tail -50 FINAL_SUMMARY.md
```

---

# 2. Entender o Projeto

## Passo 2.1: Ler o Resumo Executivo

**Tempo estimado: 10 minutos**

```bash
# Certifique-se de estar na pasta correta
cd ~/Documents/supabase/juris-ia-pro

# Leia o resumo executivo
cat FINAL_SUMMARY.md | less
# Use as setas ↑↓ para navegar
# Pressione 'q' para sair
```

**O que você vai aprender:**
- ✅ O que é o JurisIA Pro
- ✅ Quais funcionalidades tem
- ✅ Quanto código foi desenvolvido
- ✅ Como fazer deployment

## Passo 2.2: Ver o Índice Completo

```bash
# Abra o índice
cat INDEX.md | less
```

**O que você vai encontrar:**
- 📋 Lista de todos os documentos
- 🗂️ Estrutura de pastas do projeto
- 🔍 Guia de navegação rápida

## Passo 2.3: Entender a Estrutura

```bash
# Ver estrutura de pastas
tree -L 2
# Se não tiver o comando 'tree', use:
ls -R | head -100
```

**Estrutura esperada:**
```
juris-ia-pro/
├── backend/           → Código do backend (API)
├── frontend/          → Código do frontend (Interface)
├── database/          → Schema do banco de dados
├── DEPLOY.md          → Como fazer deploy
├── CHECKLIST.md       → Checklist de deploy
└── ... (outros arquivos)
```

---

# 3. Preparar o Ambiente

## Passo 3.1: Verificar Requisitos do Sistema

### Requisito 1: Docker

**Verificar se Docker está instalado:**

```bash
docker --version
```

**Resultado esperado:**
- ✅ `Docker version 20.x.x` ou superior → Docker instalado
- ❌ Erro → Precisa instalar Docker

**Instalar Docker (se necessário):**

**Windows:**
1. Baixe Docker Desktop: https://www.docker.com/products/docker-desktop
2. Execute o instalador
3. Reinicie o computador
4. Abra Docker Desktop
5. Aguarde iniciar (ícone de baleia na bandeja)

**Mac:**
1. Baixe Docker Desktop: https://www.docker.com/products/docker-desktop
2. Arraste para Applications
3. Abra Docker Desktop
4. Aguarde iniciar

**Linux (Ubuntu/Debian):**
```bash
# Atualizar sistema
sudo apt update

# Instalar Docker
sudo apt install -y docker.io docker-compose

# Iniciar serviço Docker
sudo systemctl start docker
sudo systemctl enable docker

# Adicionar seu usuário ao grupo docker
sudo usermod -aG docker $USER

# IMPORTANTE: Faça logout e login novamente para aplicar
```

**Verificar Docker Compose:**

```bash
docker-compose --version
```

**Resultado esperado:**
- ✅ `docker-compose version 1.29.x` ou `Docker Compose version 2.x.x`

### Requisito 2: Chave OpenAI API

**Você PRECISA de uma chave da OpenAI para o sistema funcionar.**

**Como obter:**

1. Acesse: https://platform.openai.com/
2. Faça login ou crie uma conta
3. Clique em **API Keys** (no menu lateral)
4. Clique em **Create new secret key**
5. Dê um nome (ex: "JurisIA Pro")
6. Clique em **Create secret key**
7. **COPIE a chave** (começa com `sk-...`)
8. **SALVE em local seguro** (você não verá novamente!)

**Exemplo de chave:**
```
sk-proj-abc123def456ghi789jkl012mno345pqr678stu901vwx234yzA
```

**Custos estimados:**
- Desenvolvimento/Testes: $5-10/mês
- Produção (uso moderado): $30-50/mês

### Requisito 3: Espaço em Disco

**Verificar espaço disponível:**

```bash
# Linux/Mac
df -h ~

# Windows (no PowerShell)
Get-PSDrive C
```

**Necessário:**
- Mínimo: 5 GB livres
- Recomendado: 10 GB livres

---

# 4. Configurar o Sistema

## Passo 4.1: Navegar para o Projeto

```bash
# Navegue para a pasta do projeto
cd ~/Documents/supabase/juris-ia-pro

# Confirme que está no lugar certo
pwd
# Deve mostrar: /Users/seu-usuario/Documents/supabase/juris-ia-pro
# ou C:\Users\seu-usuario\Documents\supabase\juris-ia-pro (Windows)
```

## Passo 4.2: Copiar Template de Configuração

```bash
# Copie o arquivo de exemplo
cp .env.production.example .env.production

# Verifique que foi criado
ls -la .env.production
```

## Passo 4.3: Editar Configurações

**IMPORTANTE:** Aqui você vai configurar senhas e chaves.

### Opção 1: Editar com Nano (Terminal)

```bash
nano .env.production
```

**Como usar o Nano:**
- Use as setas ↑↓←→ para navegar
- Digite para editar
- `Ctrl + O` para salvar
- `Enter` para confirmar
- `Ctrl + X` para sair

### Opção 2: Editar com VS Code

```bash
code .env.production
```

### Opção 3: Editar com Bloco de Notas (Windows)

```cmd
notepad .env.production
```

## Passo 4.4: Configurar Variáveis OBRIGATÓRIAS

**Você verá um arquivo assim:**

```env
# ========================================
# CONFIGURAÇÕES DO BANCO DE DADOS
# ========================================
POSTGRES_USER=juris_user
POSTGRES_PASSWORD=CHANGE_THIS_SECURE_PASSWORD_123
POSTGRES_DB=juris_ia_pro
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# ========================================
# REDIS (CACHE)
# ========================================
REDIS_PASSWORD=CHANGE_THIS_REDIS_PASSWORD_456
REDIS_HOST=redis
REDIS_PORT=6379

# ========================================
# QDRANT (VECTOR DATABASE)
# ========================================
QDRANT_URL=http://qdrant:6333

# ========================================
# OPENAI API
# ========================================
OPENAI_API_KEY=sk-your-openai-api-key-here

# ========================================
# SEGURANÇA
# ========================================
SECRET_KEY=CHANGE_THIS_TO_RANDOM_SECURE_STRING_789

# ========================================
# CORS (DOMÍNIOS PERMITIDOS)
# ========================================
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# ========================================
# FRONTEND
# ========================================
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Configure CADA variável:

#### 1. POSTGRES_PASSWORD

**O que é:** Senha do banco de dados PostgreSQL

**Como configurar:**
1. Encontre a linha: `POSTGRES_PASSWORD=CHANGE_THIS_SECURE_PASSWORD_123`
2. Troque por uma senha forte (ex: `POSTGRES_PASSWORD=MinhaSenha@2025!Segura`)
3. **ANOTE essa senha!**

**Exemplo:**
```env
POSTGRES_PASSWORD=JurisDB@2025!Segura#123
```

#### 2. REDIS_PASSWORD

**O que é:** Senha do cache Redis

**Como configurar:**
1. Encontre a linha: `REDIS_PASSWORD=CHANGE_THIS_REDIS_PASSWORD_456`
2. Troque por outra senha forte (diferente da anterior)

**Exemplo:**
```env
REDIS_PASSWORD=RedisCache@2025!Forte#456
```

#### 3. OPENAI_API_KEY

**O que é:** Sua chave da OpenAI (obtida no Passo 3.1)

**Como configurar:**
1. Encontre a linha: `OPENAI_API_KEY=sk-your-openai-api-key-here`
2. Cole sua chave da OpenAI (a que começa com `sk-...`)

**Exemplo:**
```env
OPENAI_API_KEY=sk-proj-abc123def456ghi789jkl012mno345pqr678stu901vwx234yzA
```

#### 4. SECRET_KEY

**O que é:** Chave secreta para segurança da aplicação

**Como gerar uma chave aleatória:**

```bash
# No terminal (Mac/Linux)
openssl rand -hex 32

# Ou use este site (confiável):
# https://www.random.org/strings/?num=1&len=64&digits=on&upperalpha=on&loweralpha=on&unique=on&format=html&rnd=new
```

**Como configurar:**
1. Copie a chave gerada
2. Cole na linha `SECRET_KEY=...`

**Exemplo:**
```env
SECRET_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6
```

#### 5. CORS_ORIGINS (opcional - para produção)

**O que é:** Domínios permitidos para acessar a API

**Para desenvolvimento local:** Deixe como está
```env
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

**Para produção (se tiver domínio):**
```env
CORS_ORIGINS=https://seudominio.com,https://www.seudominio.com
```

#### 6. NEXT_PUBLIC_API_URL (opcional - para produção)

**O que é:** URL do backend que o frontend vai usar

**Para desenvolvimento local:** Deixe como está
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Para produção (se tiver domínio):**
```env
NEXT_PUBLIC_API_URL=https://api.seudominio.com
```

## Passo 4.5: Salvar o Arquivo

**No Nano:**
- `Ctrl + O` → Enter → `Ctrl + X`

**No VS Code ou Notepad:**
- `Ctrl + S` (ou Cmd + S no Mac)
- Feche o editor

## Passo 4.6: Verificar Configuração

```bash
# Verificar se o arquivo existe e tem conteúdo
cat .env.production | grep -E "OPENAI_API_KEY|POSTGRES_PASSWORD|REDIS_PASSWORD|SECRET_KEY"
```

**Resultado esperado:**
```
POSTGRES_PASSWORD=JurisDB@2025!Segura#123
REDIS_PASSWORD=RedisCache@2025!Forte#456
OPENAI_API_KEY=sk-proj-abc123...
SECRET_KEY=a1b2c3d4e5f6g7h8...
```

**⚠️ Se alguma ainda estiver como "CHANGE_THIS":**
- Volte ao Passo 4.4 e configure corretamente

---

# 5. Fazer o Deploy

## Passo 5.1: Dar Permissão ao Script de Deploy

```bash
# Certifique-se de estar na pasta correta
cd ~/Documents/supabase/juris-ia-pro

# Tornar o script executável
chmod +x deploy.sh

# Verificar
ls -la deploy.sh
# Deve mostrar: -rwxr-xr-x (o 'x' indica executável)
```

## Passo 5.2: Executar o Deploy

```bash
# Execute o script
./deploy.sh
```

**Você verá um menu:**

```
🏛️  JurisIA Pro - Deploy Script

Escolha uma opção:
1) Deploy completo (primeira vez)
2) Rebuild e restart
3) Parar serviços
4) Ver logs
5) Status dos serviços
6) Backup do banco de dados
7) Restaurar banco de dados
8) Sair

Opção:
```

## Passo 5.3: Escolher "Deploy Completo"

1. Digite `1` e pressione ENTER
2. Aguarde a confirmação

**Você verá:**
```
Iniciando deploy completo...
Verificando .env.production...
✓ Arquivo de configuração encontrado
```

## Passo 5.4: Aguardar o Build

**O que vai acontecer:**

1. **Download de imagens Docker** (2-5 minutos)
   ```
   Pulling postgres (postgres:15-alpine)...
   Pulling redis (redis:7-alpine)...
   Pulling qdrant (qdrant/qdrant:latest)...
   ```

2. **Build do backend** (3-5 minutos)
   ```
   Building backend...
   Step 1/12 : FROM python:3.11-slim as base
   Step 2/12 : ENV PYTHONUNBUFFERED=1
   ...
   Successfully built abc123def456
   ```

3. **Build do frontend** (5-8 minutos)
   ```
   Building frontend...
   Step 1/15 : FROM node:18-alpine AS base
   ...
   Creating optimized production build...
   Successfully built ghi789jkl012
   ```

4. **Iniciar serviços** (1-2 minutos)
   ```
   Creating network "juris-ia-pro_default"...
   Creating volume "postgres_data"...
   Creating volume "redis_data"...
   Creating volume "qdrant_data"...

   Starting postgres...
   Starting redis...
   Starting qdrant...
   Starting backend...
   Starting frontend...
   ```

**Tempo total estimado: 10-20 minutos**

**⚠️ IMPORTANTE:** Não feche o terminal durante o processo!

## Passo 5.5: Aguardar Mensagem de Sucesso

**Quando tudo estiver pronto, você verá:**

```
✓ Todos os serviços estão rodando!

Deploy completo executado com sucesso!

Acesse:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

Para ver logs: ./deploy.sh (opção 4)
```

## Passo 5.6: Setup Inicial do Banco de Dados

**Após o deploy, configure o banco:**

```bash
# Em uma NOVA aba do terminal (mantenha a anterior aberta)
cd ~/Documents/supabase/juris-ia-pro

# Execute o setup do banco
docker-compose -f docker-compose.prod.yml exec backend python scripts/setup_db.py
```

**Você verá:**
```
🏛️ JurisIA Pro - Database Setup

Conectando ao banco de dados...
✓ Conexão estabelecida

Criando extensões...
✓ Extensão uuid-ossp criada
✓ Extensão pgvector criada

Criando tabelas...
✓ Tabela usuarios criada
✓ Tabela documentos_juridicos criada
✓ Tabela embeddings criada
... (mais 7 tabelas)

✓ Database setup completo!
```

## Passo 5.7: Popular Dados Iniciais

```bash
# Popule o banco com dados iniciais
docker-compose -f docker-compose.prod.yml exec backend python scripts/populate_database.py
```

**Você verá:**
```
🏛️ JurisIA Pro - Database Population

Iniciando scrapers...

[Planalto Scraper]
✓ CDC - Lei 8.078/1990 coletada
✓ CPC - Lei 13.105/2015 coletada
✓ CC - Lei 10.406/2002 coletada
... (mais 4 leis)

[STJ Scraper]
✓ Súmula 297 coletada
✓ Súmula 381 coletada
... (mais súmulas)

Indexando no Qdrant...
✓ 15 documentos indexados no Qdrant

Salvando no PostgreSQL...
✓ 15 documentos salvos no banco

✓ Population completa!
Total: 15 documentos jurídicos indexados
```

**Tempo: 2-5 minutos**

---

# 6. Testar o Sistema

## Passo 6.1: Verificar Status dos Serviços

```bash
# Verificar se tudo está rodando
docker-compose -f docker-compose.prod.yml ps
```

**Resultado esperado:**
```
       Name                      Command               State           Ports
----------------------------------------------------------------------------------
juris-ia-pro_backend_1    uvicorn app.main:app ...     Up      0.0.0.0:8000->8000/tcp
juris-ia-pro_frontend_1   node server.js               Up      0.0.0.0:3000->3000/tcp
juris-ia-pro_postgres_1   docker-entrypoint.sh ...     Up      5432/tcp
juris-ia-pro_qdrant_1     ./entrypoint.sh              Up      6333/tcp
juris-ia-pro_redis_1      docker-entrypoint.sh ...     Up      6379/tcp
```

**✅ Todos devem mostrar "Up"**

## Passo 6.2: Testar Backend (API)

### Teste 1: Health Check

```bash
# Testar se a API está respondendo
curl http://localhost:8000/health
```

**Resultado esperado:**
```json
{
  "status": "ok",
  "version": "1.0.0",
  "services": {
    "database": "connected",
    "cache": "connected",
    "vector_db": "connected"
  }
}
```

### Teste 2: Busca Jurídica

```bash
# Fazer uma busca
curl -X POST http://localhost:8000/api/v1/search/ \
  -H "Content-Type: application/json" \
  -d '{"query": "CDC bancos", "limit": 3}'
```

**Resultado esperado:**
```json
{
  "results": [
    {
      "titulo": "CDC - Código de Defesa do Consumidor",
      "tipo": "lei",
      "relevancia": 0.95,
      ...
    }
  ],
  "total": 3,
  "tempo_ms": 50
}
```

### Teste 3: Chat com JUSIA

```bash
# Fazer uma pergunta
curl -X POST http://localhost:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -d '{"query": "O CDC se aplica a bancos?"}'
```

**Resultado esperado:**
```json
{
  "resposta": "Sim, o CDC se aplica a instituições financeiras...",
  "fontes": [
    {
      "titulo": "Súmula 297 STJ",
      ...
    }
  ],
  "tempo_ms": 2500
}
```

## Passo 6.3: Testar Frontend (Interface)

### Teste 1: Abrir Homepage

1. Abra seu navegador
2. Digite na barra de endereço: `http://localhost:3000`
3. Pressione ENTER

**Você deve ver:**
- 🏛️ Logo "JurisIA Pro"
- Texto de apresentação
- Botões de navegação

### Teste 2: Testar Busca

1. Na homepage, clique em **"Buscar Jurisprudência"**
2. Ou acesse diretamente: `http://localhost:3000/search`

3. Na caixa de busca, digite: `CDC bancos`
4. Pressione ENTER ou clique em "Buscar"

**Você deve ver:**
- Lista de resultados
- Destaques da busca
- Filtros laterais

### Teste 3: Testar Chat

1. Clique em **"Chat JUSIA"** no menu
2. Ou acesse: `http://localhost:3000/chat`

3. Digite uma pergunta: `O que é o CDC?`
4. Pressione ENTER

**Você deve ver:**
- Sua mensagem aparecendo
- Resposta da JUSIA (aguarde 3-5 segundos)
- Fontes citadas

### Teste 4: Testar Análise de PDF

1. Clique em **"Analisar PDF"** no menu
2. Ou acesse: `http://localhost:3000/analyze`

3. Arraste um PDF para a área de upload
4. Ou clique e selecione um arquivo

5. Escolha o tipo de análise: "Completa"
6. Clique em "Analisar"

**Você deve ver:**
- Barra de progresso
- Análise completa após 10-15 segundos
- Resultados estruturados

### Teste 5: Verificar Dashboard

1. Clique em **"Estatísticas"** no menu
2. Ou acesse: `http://localhost:3000/stats`

**Você deve ver:**
- Status dos serviços (todos "Online")
- Métricas de performance
- Estatísticas do cache
- Informações do Qdrant

## Passo 6.4: Ver Logs (Se Necessário)

```bash
# Ver logs de todos os serviços
docker-compose -f docker-compose.prod.yml logs

# Ver logs apenas do backend
docker-compose -f docker-compose.prod.yml logs backend

# Ver logs apenas do frontend
docker-compose -f docker-compose.prod.yml logs frontend

# Seguir logs em tempo real
docker-compose -f docker-compose.prod.yml logs -f
# Pressione Ctrl+C para parar
```

---

# 7. Solução de Problemas

## Problema 1: "Serviço não está acessível"

### Sintoma:
- Ao acessar `http://localhost:3000`, aparece "Site inacessível"

### Solução:

```bash
# 1. Verificar se os containers estão rodando
docker-compose -f docker-compose.prod.yml ps

# 2. Se algum estiver "Exit" ou "Restarting", reinicie:
docker-compose -f docker-compose.prod.yml restart

# 3. Ver os logs para identificar erro
docker-compose -f docker-compose.prod.yml logs frontend
```

## Problema 2: "OpenAI API Key inválida"

### Sintoma:
- Chat e busca não funcionam
- Erro no log: "Invalid API key"

### Solução:

```bash
# 1. Verificar se a chave está configurada
docker-compose -f docker-compose.prod.yml exec backend env | grep OPENAI

# 2. Se estiver errada, edite .env.production
nano .env.production
# Corrija a linha OPENAI_API_KEY

# 3. Reinicie os serviços
docker-compose -f docker-compose.prod.yml restart backend
```

## Problema 3: "Banco de dados não conecta"

### Sintoma:
- Erro: "Database connection failed"

### Solução:

```bash
# 1. Verificar se PostgreSQL está rodando
docker-compose -f docker-compose.prod.yml ps postgres

# 2. Ver logs do PostgreSQL
docker-compose -f docker-compose.prod.yml logs postgres

# 3. Se necessário, recriar container
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d postgres

# 4. Aguardar 30 segundos e reiniciar backend
docker-compose -f docker-compose.prod.yml restart backend
```

## Problema 4: "Docker não encontrado"

### Sintoma:
- Erro: "docker: command not found"

### Solução:

**Verifique se Docker está instalado:**
```bash
which docker
```

**Se não estiver:**
- Volte ao Passo 3.1 e instale o Docker

**Se estiver mas não funciona (Linux):**
```bash
# Iniciar serviço Docker
sudo systemctl start docker

# Adicionar seu usuário ao grupo
sudo usermod -aG docker $USER

# Fazer logout e login novamente
```

## Problema 5: "Porta já está em uso"

### Sintoma:
- Erro: "port 3000 is already allocated"

### Solução:

**Opção 1: Parar o processo que está usando a porta**
```bash
# Linux/Mac - Encontrar processo na porta 3000
lsof -ti:3000

# Matar o processo
kill -9 $(lsof -ti:3000)

# Windows (PowerShell)
Get-Process -Id (Get-NetTCPConnection -LocalPort 3000).OwningProcess | Stop-Process
```

**Opção 2: Mudar a porta do JurisIA Pro**
```bash
# Edite docker-compose.prod.yml
nano docker-compose.prod.yml

# Encontre a linha do frontend:
# ports:
#   - "3000:3000"
#
# Mude para outra porta (ex: 3001):
# ports:
#   - "3001:3000"

# Salve e reinicie
docker-compose -f docker-compose.prod.yml up -d
```

## Problema 6: "Build falhou"

### Sintoma:
- Erro durante `docker-compose build`

### Solução:

```bash
# 1. Limpar cache do Docker
docker system prune -a
# Digite 'y' para confirmar

# 2. Tentar build novamente
docker-compose -f docker-compose.prod.yml build --no-cache

# 3. Se ainda falhar, verifique espaço em disco
df -h
```

## Problema 7: "Resposta muito lenta"

### Sintoma:
- Chat demora mais de 10 segundos
- Busca lenta

### Solução:

```bash
# 1. Verificar cache Redis
curl http://localhost:8000/api/v1/stats/cache/stats

# 2. Se cache estiver inativo, verificar logs
docker-compose -f docker-compose.prod.yml logs redis

# 3. Limpar cache e reiniciar
curl -X POST http://localhost:8000/api/v1/stats/cache/clear
docker-compose -f docker-compose.prod.yml restart redis backend
```

## Obter Ajuda Adicional

### Ver logs detalhados:
```bash
docker-compose -f docker-compose.prod.yml logs -f --tail=100
```

### Entrar dentro de um container:
```bash
# Entrar no backend
docker-compose -f docker-compose.prod.yml exec backend bash

# Entrar no frontend
docker-compose -f docker-compose.prod.yml exec frontend sh
```

### Reiniciar tudo do zero:
```bash
# CUIDADO: Isso apaga todos os dados!
docker-compose -f docker-compose.prod.yml down -v
docker-compose -f docker-compose.prod.yml up -d
```

---

# 8. Comandos Úteis de Referência

## Gerenciamento de Serviços

```bash
# Iniciar todos os serviços
docker-compose -f docker-compose.prod.yml up -d

# Parar todos os serviços
docker-compose -f docker-compose.prod.yml down

# Reiniciar todos
docker-compose -f docker-compose.prod.yml restart

# Reiniciar apenas um serviço
docker-compose -f docker-compose.prod.yml restart backend

# Ver status
docker-compose -f docker-compose.prod.yml ps

# Ver logs
docker-compose -f docker-compose.prod.yml logs -f
```

## Backup e Restore

```bash
# Fazer backup do banco
./deploy.sh  # Opção 6

# Ou manualmente:
docker-compose -f docker-compose.prod.yml exec postgres pg_dump -U juris_user juris_ia_pro > backup.sql

# Restaurar backup
docker-compose -f docker-compose.prod.yml exec -T postgres psql -U juris_user juris_ia_pro < backup.sql
```

## Limpeza

```bash
# Parar e remover tudo (CUIDADO!)
docker-compose -f docker-compose.prod.yml down -v

# Limpar imagens não usadas
docker image prune -a

# Limpar tudo do Docker
docker system prune -a --volumes
```

---

# 🎉 Conclusão

Se você seguiu todos os passos até aqui, seu sistema JurisIA Pro deve estar:

✅ **Instalado** e configurado
✅ **Rodando** em http://localhost:3000
✅ **Funcional** com busca, chat e análise de PDF
✅ **Pronto** para uso!

---

## Próximos Passos

1. **Usar o sistema** - Teste todas as funcionalidades
2. **Adicionar mais dados** - Expanda a base de documentos
3. **Deploy em produção** - Siga o guia em DEPLOY.md
4. **Configurar domínio** - Para acesso público

---

## Ajuda Rápida

| Preciso... | Comando |
|-----------|---------|
| Iniciar sistema | `docker-compose -f docker-compose.prod.yml up -d` |
| Parar sistema | `docker-compose -f docker-compose.prod.yml down` |
| Ver status | `docker-compose -f docker-compose.prod.yml ps` |
| Ver logs | `docker-compose -f docker-compose.prod.yml logs -f` |
| Reiniciar | `docker-compose -f docker-compose.prod.yml restart` |
| Backup | `./deploy.sh` → opção 6 |
| Abrir frontend | http://localhost:3000 |
| Abrir API docs | http://localhost:8000/docs |

---

**🏛️ JurisIA Pro - Sistema pronto! Bom uso! ⚖️**
