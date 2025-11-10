# 🚀 Guia de Deploy - JurisIA Pro

Guia completo para implantação do JurisIA Pro em produção.

## 📋 Índice

1. [Pré-requisitos](#pré-requisitos)
2. [Deploy Local com Docker](#deploy-local-com-docker)
3. [Deploy em Servidor VPS](#deploy-em-servidor-vps)
4. [Deploy em Cloud](#deploy-em-cloud)
5. [Configuração de Domínio e SSL](#configuração-de-domínio-e-ssl)
6. [Monitoramento e Logs](#monitoramento-e-logs)
7. [Backup e Restauração](#backup-e-restauração)
8. [Troubleshooting](#troubleshooting)

---

## 🔧 Pré-requisitos

### Software Necessário

- **Docker** 20.10+
- **Docker Compose** 2.0+
- **Git**
- **OpenAI API Key** (obrigatório)

### Recursos Mínimos

**Para Desenvolvimento:**
- CPU: 2 cores
- RAM: 4GB
- Disco: 20GB
- Conexão: Internet estável

**Para Produção:**
- CPU: 4+ cores
- RAM: 8GB+
- Disco: 50GB+ SSD
- Conexão: Internet rápida e estável

---

## 🐳 Deploy Local com Docker

### 1. Clonar Repositório

```bash
git clone https://github.com/seu-usuario/supabase.git
cd supabase/juris-ia-pro
```

### 2. Configurar Variáveis de Ambiente

```bash
# Copiar arquivo de exemplo
cp .env.production.example .env.production

# Editar configurações
nano .env.production
```

**Variáveis Obrigatórias:**
```env
# OpenAI (OBRIGATÓRIO!)
OPENAI_API_KEY=sk-your-actual-key-here

# Senhas (MUDAR!)
POSTGRES_PASSWORD=seu_password_seguro_aqui
REDIS_PASSWORD=sua_senha_redis_aqui
SECRET_KEY=chave_secreta_aleatoria_muito_longa

# Domínio (se aplicável)
CORS_ORIGINS=https://seudominio.com
NEXT_PUBLIC_API_URL=https://api.seudominio.com
```

### 3. Executar Deploy

```bash
# Tornar script executável
chmod +x deploy.sh

# Executar deploy completo
./deploy.sh
# Selecione opção 1: Deploy completo

# OU executar manualmente:
docker-compose -f docker-compose.prod.yml --env-file .env.production up -d
```

### 4. Verificar Status

```bash
# Ver status dos containers
docker-compose -f docker-compose.prod.yml ps

# Ver logs
docker-compose -f docker-compose.prod.yml logs -f

# Testar health
curl http://localhost:8000/health
curl http://localhost:3000
```

### 5. Acessar Aplicação

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Qdrant UI:** http://localhost:6333/dashboard

---

## 🖥️ Deploy em Servidor VPS

### Opção 1: DigitalOcean / Linode / Vultr

#### 1.1. Criar Droplet/VM

```bash
# Ubuntu 22.04 LTS
# 4GB RAM mínimo
# 2 CPU cores
# 50GB SSD
```

#### 1.2. Conectar via SSH

```bash
ssh root@seu-servidor-ip
```

#### 1.3. Instalar Docker

```bash
# Atualizar sistema
apt update && apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Instalar Docker Compose
apt install docker-compose -y

# Verificar instalação
docker --version
docker-compose --version
```

#### 1.4. Configurar Firewall

```bash
# UFW Firewall
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw enable
```

#### 1.5. Clonar e Deploy

```bash
# Instalar Git
apt install git -y

# Clonar repositório
git clone https://github.com/seu-usuario/supabase.git
cd supabase/juris-ia-pro

# Configurar .env.production
cp .env.production.example .env.production
nano .env.production

# Deploy
./deploy.sh
```

#### 1.6. Configurar Nginx (opcional)

```bash
# Instalar Nginx
apt install nginx -y

# Configurar proxy reverso
nano /etc/nginx/sites-available/jurisia
```

```nginx
server {
    listen 80;
    server_name seudominio.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# Ativar site
ln -s /etc/nginx/sites-available/jurisia /etc/nginx/sites-enabled/
nginx -t
systemctl reload nginx
```

---

## ☁️ Deploy em Cloud

### Opção 1: Railway

1. Criar conta em [railway.app](https://railway.app)
2. Conectar repositório GitHub
3. Railway detecta automaticamente:
   - `backend/Dockerfile`
   - `frontend/Dockerfile`
4. Configurar variáveis de ambiente no painel
5. Deploy automático!

**Custo:** ~$5-20/mês

### Opção 2: Render

1. Criar conta em [render.com](https://render.com)
2. New → Web Service
3. Conectar repositório
4. Configurar:
   - Backend: Dockerfile em `backend/`
   - Frontend: Dockerfile em `frontend/`
5. Adicionar PostgreSQL, Redis (addons)
6. Deploy!

**Custo:** ~$7-25/mês (com banco de dados)

### Opção 3: AWS / Google Cloud / Azure

#### AWS Lightsail (Mais fácil)

```bash
# Criar instância Ubuntu 22.04
# 2GB RAM ($10/mês)

# Seguir passos de VPS acima
```

#### AWS ECS (Mais escalável)

1. Criar cluster ECS
2. Configurar Task Definitions
3. Usar ECR para imagens Docker
4. Configurar Load Balancer
5. Auto-scaling

**Custo:** ~$30-100/mês (dependendo do uso)

---

## 🌐 Configuração de Domínio e SSL

### 1. Apontar Domínio

**Registrar em seu provedor DNS:**

```
Tipo    Nome          Valor
A       @             seu-servidor-ip
A       www           seu-servidor-ip
A       api           seu-servidor-ip
```

### 2. Configurar SSL com Let's Encrypt

```bash
# Instalar Certbot
apt install certbot python3-certbot-nginx -y

# Obter certificado
certbot --nginx -d seudominio.com -d www.seudominio.com -d api.seudominio.com

# Renovação automática
certbot renew --dry-run
```

### 3. Atualizar .env.production

```env
CORS_ORIGINS=https://seudominio.com,https://www.seudominio.com
NEXT_PUBLIC_API_URL=https://api.seudominio.com
```

### 4. Reiniciar Serviços

```bash
./deploy.sh
# Opção 2: Rebuild e restart
```

---

## 📊 Monitoramento e Logs

### Ver Logs em Tempo Real

```bash
# Todos os serviços
docker-compose -f docker-compose.prod.yml logs -f

# Serviço específico
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f frontend

# Últimas 100 linhas
docker-compose -f docker-compose.prod.yml logs --tail=100
```

### Monitorar Recursos

```bash
# Uso de recursos dos containers
docker stats

# Espaço em disco
df -h

# Logs do sistema
journalctl -u docker -f
```

### Ferramentas de Monitoramento (Opcional)

#### Prometheus + Grafana

```bash
# Adicionar ao docker-compose.prod.yml
# Ver exemplo em: monitoring/docker-compose.monitoring.yml
```

#### Sentry (Erros)

```env
# Adicionar ao .env.production
SENTRY_DSN=https://your-sentry-dsn
```

---

## 💾 Backup e Restauração

### Backup Manual

```bash
# Usar script deploy.sh
./deploy.sh
# Opção 6: Backup do banco de dados

# OU manualmente:
docker-compose -f docker-compose.prod.yml exec postgres \
  pg_dump -U juris_user juris_ia_pro > backup_$(date +%Y%m%d).sql
```

### Backup Automático (Cron)

```bash
# Editar crontab
crontab -e

# Adicionar (backup diário às 3h da manhã)
0 3 * * * cd /path/to/juris-ia-pro && docker-compose -f docker-compose.prod.yml exec -T postgres pg_dump -U juris_user juris_ia_pro > backups/backup_$(date +\%Y\%m\%d_\%H\%M).sql
```

### Restauração

```bash
# Usar script deploy.sh
./deploy.sh
# Opção 7: Restaurar banco de dados

# OU manualmente:
docker-compose -f docker-compose.prod.yml exec -T postgres \
  psql -U juris_user juris_ia_pro < backup_20250115.sql
```

---

## 🔍 Troubleshooting

### Problema: Containers não iniciam

```bash
# Ver logs de erro
docker-compose -f docker-compose.prod.yml logs

# Verificar recursos
docker stats
df -h

# Rebuild forçado
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml build --no-cache
docker-compose -f docker-compose.prod.yml up -d
```

### Problema: Erro de conexão com banco

```bash
# Verificar se PostgreSQL está rodando
docker-compose -f docker-compose.prod.yml ps postgres

# Ver logs do PostgreSQL
docker-compose -f docker-compose.prod.yml logs postgres

# Testar conexão
docker-compose -f docker-compose.prod.yml exec postgres \
  psql -U juris_user -d juris_ia_pro -c "SELECT 1"
```

### Problema: OpenAI API Key inválida

```bash
# Verificar .env.production
cat .env.production | grep OPENAI_API_KEY

# Testar key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# Atualizar e reiniciar
nano .env.production
./deploy.sh # Opção 2
```

### Problema: Frontend não conecta no Backend

```bash
# Verificar NEXT_PUBLIC_API_URL
docker-compose -f docker-compose.prod.yml exec frontend \
  printenv | grep NEXT_PUBLIC_API_URL

# Verificar CORS_ORIGINS no backend
docker-compose -f docker-compose.prod.yml exec backend \
  printenv | grep CORS_ORIGINS

# Atualizar e rebuild
./deploy.sh # Opção 2
```

### Problema: Disco cheio

```bash
# Limpar containers antigos
docker system prune -a

# Limpar volumes não usados
docker volume prune

# Limpar logs
truncate -s 0 /var/lib/docker/containers/*/*.log
```

---

## 📋 Checklist Pré-Deploy

- [ ] Servidor configurado (VPS/Cloud)
- [ ] Docker e Docker Compose instalados
- [ ] OpenAI API Key válida
- [ ] Arquivo .env.production configurado
- [ ] Senhas alteradas (PostgreSQL, Redis, SECRET_KEY)
- [ ] Domínio apontado (se aplicável)
- [ ] SSL configurado (se aplicável)
- [ ] Firewall configurado
- [ ] Backup automático configurado
- [ ] Monitoramento configurado

---

## 📋 Checklist Pós-Deploy

- [ ] Frontend acessível
- [ ] Backend respondendo
- [ ] /health retorna 200 OK
- [ ] /docs funcional
- [ ] Busca jurídica funcionando
- [ ] Chat respondendo
- [ ] Análise de PDF funcionando
- [ ] Estatísticas mostrando dados
- [ ] Logs sem erros críticos
- [ ] SSL válido (https)
- [ ] Performance adequada (<1s resposta)

---

## 🆘 Suporte

### Documentação
- [README.md](./README.md)
- [TESTING.md](./TESTING.md)
- [SERVICES.md](./SERVICES.md)
- [STATUS.md](./STATUS.md)

### Comandos Úteis

```bash
# Status completo
./deploy.sh # Opção 5

# Logs
./deploy.sh # Opção 4

# Restart
./deploy.sh # Opção 2

# Parar tudo
./deploy.sh # Opção 3
```

---

## 🎯 Resumo de Custos

| Opção | CPU | RAM | Disco | Custo/mês |
|-------|-----|-----|-------|-----------|
| Railway | Shared | 512MB-1GB | 1GB | $5-10 |
| Render | Shared | 512MB | 1GB | $7-15 |
| DigitalOcean | 2 cores | 4GB | 80GB | $24 |
| AWS Lightsail | 2 cores | 4GB | 80GB | $20 |
| Hetzner | 2 cores | 4GB | 40GB | €4.5 (~$5) |

**+ OpenAI API:** ~$30-50/mês (uso moderado)

**Total estimado:** $35-75/mês

---

**Desenvolvido com ⚖️ para revolucionar o acesso à justiça no Brasil**
