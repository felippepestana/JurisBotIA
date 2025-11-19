# 🚀 EXECUTE AGORA - Guia Ultra-Simples

## ✅ TUDO JÁ ESTÁ PRONTO!

Preparei **TUDO** para você. Só faltam **3 passos simples**!

---

## 📋 PRÉ-REQUISITOS

Antes de começar, você precisa ter:

### 1. Docker Instalado

**Verificar se tem:**
```bash
docker --version
```

**Se aparecer erro, instale:**
- **Windows/Mac:** https://www.docker.com/products/docker-desktop
- **Linux:** `sudo apt install docker.io docker-compose`

### 2. Chave OpenAI

**Como obter (2 minutos):**
1. Acesse: https://platform.openai.com/api-keys
2. Faça login ou crie conta
3. Clique em "Create new secret key"
4. Copie a chave (começa com `sk-...`)
5. **GUARDE** em local seguro!

---

## 🎯 OS 3 PASSOS

### Passo 1: Configurar a Chave OpenAI (30 segundos)

```bash
# Entre na pasta do projeto
cd juris-ia-pro

# Renomeie o arquivo pré-configurado
mv .env.production.READY .env.production

# Edite o arquivo
nano .env.production
# ou
code .env.production
# ou
notepad .env.production
```

**Encontre a linha 50:**
```env
OPENAI_API_KEY=sk-COLE_SUA_CHAVE_OPENAI_AQUI
```

**Substitua por sua chave:**
```env
OPENAI_API_KEY=sk-proj-abc123def456...sua-chave-aqui
```

**Salve o arquivo:**
- Nano: `Ctrl+O` → Enter → `Ctrl+X`
- VS Code / Notepad: `Ctrl+S`

✅ **Pronto!** Senhas e configurações já estão prontas!

### Passo 2: Executar o Deploy (15-20 minutos)

```bash
# Certifique-se de estar na pasta correta
cd juris-ia-pro

# Dar permissão ao script
chmod +x deploy.sh

# Executar deploy
./deploy.sh
```

**No menu que aparecer:**
```
Escolha uma opção:
1) Deploy completo (primeira vez)   ← Digite 1 e pressione ENTER
...
```

**O que vai acontecer:**
```
✓ Verificando .env.production...
✓ Baixando imagens Docker... (2-5 min)
✓ Compilando backend... (3-5 min)
✓ Compilando frontend... (5-8 min)
✓ Iniciando serviços... (1-2 min)
✓ Deploy completo!
```

**Tempo total: 10-20 minutos**

⏳ **Aguarde!** Tome um café enquanto o sistema é construído.

### Passo 3: Acessar o Sistema (10 segundos)

**Quando terminar, você verá:**
```
✓ Deploy completo executado com sucesso!

Acesse:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs
```

**Abra seu navegador:**
```
http://localhost:3000
```

🎉 **PRONTO! Sistema funcionando!**

---

## 🧪 TESTES RÁPIDOS

### Teste 1: Homepage

1. Abra: http://localhost:3000
2. Você deve ver o logo "JurisIA Pro"

### Teste 2: Busca

1. Clique em "Buscar Jurisprudência"
2. Digite: `CDC bancos`
3. Clique em "Buscar"
4. Você deve ver resultados!

### Teste 3: Chat

1. Clique em "Chat JUSIA"
2. Digite: `O que é o CDC?`
3. Pressione Enter
4. Aguarde 3-5 segundos
5. JUSIA vai responder!

---

## ❓ PROBLEMAS COMUNS

### "Docker não encontrado"

**Solução:**
```bash
# Verificar se Docker está rodando (Mac/Windows)
# Abra Docker Desktop e aguarde o ícone ficar verde

# Linux: Iniciar Docker
sudo systemctl start docker

# Adicionar seu usuário ao grupo docker (Linux)
sudo usermod -aG docker $USER
# Depois: Fazer logout e login novamente
```

### "Porta já está em uso"

**Solução:**
```bash
# Parar o que estiver usando a porta 3000
# Linux/Mac:
lsof -ti:3000 | xargs kill -9

# Windows PowerShell:
Get-Process -Id (Get-NetTCPConnection -LocalPort 3000).OwningProcess | Stop-Process
```

### "OpenAI API Key inválida"

**Solução:**
1. Verifique se copiou a chave completa
2. A chave deve começar com `sk-proj-` ou `sk-`
3. Edite novamente o `.env.production`
4. Reinicie: `./deploy.sh` → Opção 2 (Rebuild)

### "Build falhou"

**Solução:**
```bash
# Limpar cache do Docker
docker system prune -a
# Digite 'y' para confirmar

# Tentar novamente
./deploy.sh
# Opção 1
```

---

## 📊 COMANDOS ÚTEIS

```bash
# Ver status dos serviços
docker-compose -f docker-compose.prod.yml ps

# Ver logs
docker-compose -f docker-compose.prod.yml logs -f

# Parar tudo
docker-compose -f docker-compose.prod.yml down

# Reiniciar
docker-compose -f docker-compose.prod.yml restart

# Ou use o script:
./deploy.sh
```

---

## 🎓 PRÓXIMOS PASSOS

Depois que o sistema estiver rodando:

### 1. Popular Mais Dados

```bash
# Executar dentro do container backend
docker-compose -f docker-compose.prod.yml exec backend python scripts/populate_database.py
```

### 2. Criar Backup

```bash
./deploy.sh
# Escolha opção 6: Backup do banco de dados
```

### 3. Explorar a API

Acesse: http://localhost:8000/docs

Você verá toda a documentação interativa da API!

### 4. Deploy em Produção

Quando quiser colocar online:
- Leia: `DEPLOY.md` (instruções para VPS, Railway, Render, AWS)

---

## 📞 AJUDA

**Se tiver qualquer problema:**

1. Verifique os logs:
   ```bash
   docker-compose -f docker-compose.prod.yml logs backend
   docker-compose -f docker-compose.prod.yml logs frontend
   ```

2. Leia o troubleshooting completo:
   ```bash
   cat GUIA_PASSO_A_PASSO.md
   # Vá para seção 7: Solução de Problemas
   ```

3. Reinicie tudo:
   ```bash
   docker-compose -f docker-compose.prod.yml down
   docker-compose -f docker-compose.prod.yml up -d
   ```

---

## ✅ CHECKLIST RÁPIDO

Antes de executar, confirme:

- [ ] Docker instalado e rodando
- [ ] Chave OpenAI obtida
- [ ] Arquivo `.env.production` criado e editado
- [ ] Chave OpenAI colada no `.env.production`
- [ ] Pelo menos 10 GB de espaço livre em disco
- [ ] Portas 3000 e 8000 livres

**Se marcou todos, execute!**

---

## 🎯 RESUMO DOS 3 PASSOS

```bash
# 1. Configurar OpenAI
mv .env.production.READY .env.production
nano .env.production  # Cole sua chave na linha 50

# 2. Deploy
chmod +x deploy.sh
./deploy.sh  # Opção 1

# 3. Acessar
# Abra: http://localhost:3000
```

**É isso! Só 3 passos!** 🚀

---

## 📦 O QUE JÁ ESTÁ CONFIGURADO

✅ **Senhas seguras geradas automaticamente:**
- PostgreSQL: `be558f126e906bcf3f99246a87b1b413`
- Redis: `44d927641580ca2d0c6e24aece113dd6`
- Secret Key: `8e0d385d42e3e3deb91a93aeaa7a53cee1251753b908d70dd29f84cdb1ee516e`

✅ **Configurações otimizadas:**
- Cache TTL: 5 minutos
- RAG threshold: 0.7
- Max tokens: 4000
- Rate limit: 60/min

✅ **URLs configuradas:**
- CORS: localhost:3000, localhost:8000
- API URL: http://localhost:8000

✅ **Tudo pronto!** Você só precisa da chave OpenAI!

---

**🏛️ JurisIA Pro - Pronto para revolucionar o acesso à justiça! ⚖️**

**Qualquer dúvida, consulte:**
- `GUIA_PASSO_A_PASSO.md` - Tutorial detalhado
- `DEPLOY.md` - Deploy avançado
- `TROUBLESHOOTING.md` - Solução de problemas
