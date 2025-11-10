# ✅ Checklist de Implantação - JurisIA Pro

Use este checklist para garantir que tudo está pronto para deploy em produção.

## 📦 Fase 1: Preparação

### Código e Repositório
- [ ] Todo código commitado no Git
- [ ] Branch de produção criada
- [ ] README.md atualizado
- [ ] Documentação completa
- [ ] .gitignore configurado
- [ ] Sem arquivos sensíveis no repositório

### Ambiente de Desenvolvimento
- [ ] Backend rodando localmente (✅ http://localhost:8000)
- [ ] Frontend rodando localmente (✅ http://localhost:3000)
- [ ] Todos os endpoints funcionando
- [ ] Testes manuais realizados
- [ ] Performance satisfatória

---

## 🔧 Fase 2: Configuração

### Variáveis de Ambiente
- [ ] `.env.production` criado (copiar de `.env.production.example`)
- [ ] **OPENAI_API_KEY** configurada (OBRIGATÓRIO!)
- [ ] **POSTGRES_PASSWORD** alterada (SEGURANÇA!)
- [ ] **REDIS_PASSWORD** alterada (SEGURANÇA!)
- [ ] **SECRET_KEY** gerada (use: `openssl rand -hex 32`)
- [ ] **CORS_ORIGINS** configurado com seu domínio
- [ ] **NEXT_PUBLIC_API_URL** configurado

### Servidor/Infraestrutura
- [ ] Servidor VPS/Cloud provisionado
  - [ ] Mínimo: 4GB RAM, 2 CPU cores, 50GB disco
- [ ] Sistema operacional: Ubuntu 22.04 LTS (recomendado)
- [ ] Acesso SSH configurado
- [ ] Firewall configurado (portas 22, 80, 443)
- [ ] Docker instalado (`docker --version`)
- [ ] Docker Compose instalado (`docker-compose --version`)

### Domínio e DNS (Opcional mas recomendado)
- [ ] Domínio registrado
- [ ] DNS apontando para servidor:
  - [ ] `@` → IP do servidor
  - [ ] `www` → IP do servidor
  - [ ] `api` → IP do servidor
- [ ] SSL/HTTPS configurado (Let's Encrypt)

---

## 🚀 Fase 3: Deploy

### Deploy Inicial
- [ ] Código clonado no servidor
- [ ] `.env.production` configurado no servidor
- [ ] Executar: `./deploy.sh` (opção 1)
- [ ] Aguardar conclusão do build (~5-10 minutos)
- [ ] Verificar containers rodando: `docker ps`

### Verificação de Serviços
- [ ] PostgreSQL iniciado e saudável
- [ ] Redis iniciado e saudável
- [ ] Qdrant iniciado e saudável
- [ ] Backend respondendo em :8000
- [ ] Frontend respondendo em :3000

### Banco de Dados
- [ ] Schema criado (`setup_db.py` executado)
- [ ] Dados iniciais populados (`populate_database.py` executado)
- [ ] ~100 documentos jurídicos indexados
- [ ] Qdrant collection criada

---

## 🧪 Fase 4: Testes em Produção

### Endpoints do Backend
- [ ] `GET /health` retorna 200 OK
- [ ] `GET /docs` acessível
- [ ] `POST /api/v1/search` funcionando
- [ ] `POST /api/v1/chat` respondendo
- [ ] `POST /api/v1/analyze/pdf` processando PDFs
- [ ] `GET /api/v1/stats` retornando métricas

### Frontend
- [ ] Homepage carregando
- [ ] Busca jurídica funcionando
  - [ ] Autocompletar operacional
  - [ ] Filtros aplicando
  - [ ] Resultados exibindo
- [ ] Chat com JUSIA respondendo
  - [ ] Mensagens enviando
  - [ ] Markdown renderizando
  - [ ] Fontes exibindo
- [ ] Análise de PDF funcionando
  - [ ] Upload aceito
  - [ ] Análise processando
  - [ ] Resultados exibindo
- [ ] Dashboard de estatísticas mostrando dados

### Performance
- [ ] Busca respondendo em < 1s
- [ ] Chat respondendo em < 5s
- [ ] Análise PDF em < 10s
- [ ] Cache funcionando (verificar Redis stats)
- [ ] Vector search operacional (verificar Qdrant)

### Segurança
- [ ] HTTPS funcionando (certificado válido)
- [ ] CORS configurado corretamente
- [ ] Senhas fortes em uso
- [ ] Sem informações sensíveis expostas nos logs
- [ ] Rate limiting configurado

---

## 📊 Fase 5: Monitoramento

### Configurar Monitoramento
- [ ] Logs configurados
  - [ ] Backend logs acessíveis
  - [ ] Frontend logs acessíveis
  - [ ] PostgreSQL logs acessíveis
- [ ] Alertas configurados (opcional)
- [ ] Uptime monitoring (opcional)
  - UptimeRobot, Pingdom, etc.

### Backup
- [ ] Backup manual testado
  - [ ] `./deploy.sh` opção 6
- [ ] Backup automático configurado
  - [ ] Cron job criado
  - [ ] Teste de restauração realizado
- [ ] Local de armazenamento de backups definido
  - [ ] AWS S3, Backblaze, etc.

---

## 📱 Fase 6: Pós-Deploy

### Documentação
- [ ] URL de produção documentada
- [ ] Credenciais salvas em local seguro
- [ ] Runbook de operações criado
- [ ] Contatos de emergência definidos

### Comunicação
- [ ] Equipe notificada sobre deploy
- [ ] Usuários informados (se aplicável)
- [ ] Status page atualizado (se houver)

### Otimização (Opcional)
- [ ] CDN configurado (Cloudflare, etc.)
- [ ] Caching otimizado
- [ ] Compressão ativada
- [ ] Analytics configurado (Google Analytics, etc.)
- [ ] Error tracking (Sentry, etc.)

---

## 🆘 Comandos de Emergência

### Ver Status Rápido
```bash
cd /path/to/juris-ia-pro
./deploy.sh  # Opção 5: Status dos serviços
```

### Ver Logs
```bash
./deploy.sh  # Opção 4: Ver logs
```

### Restart Completo
```bash
./deploy.sh  # Opção 2: Rebuild e restart
```

### Rollback (se necessário)
```bash
# Parar serviços atuais
docker-compose -f docker-compose.prod.yml down

# Voltar para commit anterior
git checkout <commit-hash-anterior>

# Rebuild e restart
./deploy.sh  # Opção 1
```

### Restaurar Backup
```bash
./deploy.sh  # Opção 7: Restaurar banco de dados
```

---

## 📈 Métricas de Sucesso

Após deploy, verifique se as seguintes métricas estão sendo atingidas:

### Performance
- ✅ **Busca com cache:** < 100ms
- ✅ **Busca sem cache:** < 1s
- ✅ **Chat response:** < 5s
- ✅ **PDF analysis:** < 10s
- ✅ **Uptime:** > 99%

### Funcionalidade
- ✅ **Documentos indexados:** ~100+
- ✅ **Cache hit rate:** > 60%
- ✅ **API success rate:** > 95%
- ✅ **Zero erros críticos** nos logs

---

## 🎯 Checklist Rápido - Dia do Deploy

### Manhã (Preparação)
- [ ] 08:00 - Backup completo do ambiente atual
- [ ] 08:30 - Verificar servidor de produção
- [ ] 09:00 - Clonar código mais recente
- [ ] 09:30 - Configurar .env.production
- [ ] 10:00 - Build local de teste

### Deploy (Execução)
- [ ] 14:00 - Iniciar deploy em produção
- [ ] 14:10 - Monitorar logs
- [ ] 14:20 - Executar testes manuais
- [ ] 14:30 - Verificar métricas

### Pós-Deploy (Validação)
- [ ] 14:45 - Testar todos os endpoints
- [ ] 15:00 - Verificar performance
- [ ] 15:15 - Monitorar por 30 min
- [ ] 15:45 - Declarar sucesso ou rollback

### Noite (Monitoramento)
- [ ] 20:00 - Check de estabilidade
- [ ] 23:00 - Verificação final
- [ ] Deixar alertas ativos overnight

---

## ✅ Aprovação Final

Antes de considerar o deploy completo, certifique-se de que **TODOS** os itens abaixo estão ✅:

- [ ] **Todos os serviços estão rodando** (4/4 healthy)
- [ ] **Todos os endpoints estão funcionais** (100% sucesso)
- [ ] **Performance está adequada** (< 1s para buscas)
- [ ] **Sem erros críticos nos logs**
- [ ] **Backup configurado e testado**
- [ ] **Monitoramento ativo**
- [ ] **Documentação atualizada**
- [ ] **Equipe treinada** (se houver)

---

## 🎉 Deploy Concluído!

Parabéns! Se todos os itens acima estão ✅, seu sistema JurisIA Pro está oficialmente em produção!

### Próximos Passos
1. Monitorar por 24-48h
2. Coletar feedback de usuários
3. Planejar melhorias
4. Adicionar mais features
5. Escalar conforme necessário

---

**Data do Deploy:** ___/___/______

**Responsável:** _________________________

**Status Final:** [ ] ✅ Sucesso  [ ] ⚠️ Com ressalvas  [ ] ❌ Falha

**Observações:**
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

---

**Desenvolvido com ⚖️ para revolucionar o acesso à justiça no Brasil**
