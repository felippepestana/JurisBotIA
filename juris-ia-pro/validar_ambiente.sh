#!/bin/bash

# ============================================
# JURISIA PRO - Script de Validação
# ============================================
# Este script verifica se seu ambiente está
# pronto para o deploy
# ============================================

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Contadores
CHECKS_PASSED=0
CHECKS_FAILED=0
WARNINGS=0

echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}🏛️  JurisIA Pro - Validação de Ambiente${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""

# Função para check bem-sucedido
check_ok() {
    echo -e "${GREEN}✓${NC} $1"
    ((CHECKS_PASSED++))
}

# Função para check falhou
check_fail() {
    echo -e "${RED}✗${NC} $1"
    ((CHECKS_FAILED++))
}

# Função para aviso
check_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
    ((WARNINGS++))
}

echo -e "${BLUE}1. Verificando Sistema Operacional...${NC}"
OS=$(uname -s)
case "$OS" in
    Linux*)     check_ok "Linux detectado";;
    Darwin*)    check_ok "macOS detectado";;
    MINGW*|MSYS*|CYGWIN*)    check_ok "Windows detectado";;
    *)          check_warn "SO desconhecido: $OS";;
esac
echo ""

echo -e "${BLUE}2. Verificando Docker...${NC}"
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version)
    check_ok "Docker instalado: $DOCKER_VERSION"

    # Verificar se Docker está rodando
    if docker info &> /dev/null; then
        check_ok "Docker daemon está rodando"
    else
        check_fail "Docker daemon não está rodando! Inicie o Docker Desktop ou execute 'sudo systemctl start docker'"
    fi
else
    check_fail "Docker não está instalado! Instale em: https://www.docker.com/products/docker-desktop"
fi
echo ""

echo -e "${BLUE}3. Verificando Docker Compose...${NC}"
if command -v docker-compose &> /dev/null; then
    COMPOSE_VERSION=$(docker-compose --version)
    check_ok "Docker Compose instalado: $COMPOSE_VERSION"
elif docker compose version &> /dev/null; then
    COMPOSE_VERSION=$(docker compose version)
    check_ok "Docker Compose (plugin) instalado: $COMPOSE_VERSION"
else
    check_fail "Docker Compose não está instalado!"
fi
echo ""

echo -e "${BLUE}4. Verificando Git...${NC}"
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version)
    check_ok "Git instalado: $GIT_VERSION"
else
    check_warn "Git não instalado (opcional, mas recomendado)"
fi
echo ""

echo -e "${BLUE}5. Verificando Espaço em Disco...${NC}"
if command -v df &> /dev/null; then
    AVAILABLE=$(df -h . | awk 'NR==2 {print $4}')
    check_ok "Espaço disponível: $AVAILABLE"

    # Verificar se tem pelo menos 5GB (aproximado)
    AVAILABLE_GB=$(df -BG . | awk 'NR==2 {print $4}' | sed 's/G//')
    if [ "$AVAILABLE_GB" -ge 5 ]; then
        check_ok "Espaço suficiente (>= 5 GB)"
    else
        check_warn "Espaço pode ser insuficiente. Recomendado: >= 10 GB"
    fi
else
    check_warn "Não foi possível verificar espaço em disco"
fi
echo ""

echo -e "${BLUE}6. Verificando Portas Disponíveis...${NC}"

# Verificar porta 3000
if command -v lsof &> /dev/null; then
    if lsof -i:3000 &> /dev/null; then
        check_warn "Porta 3000 está em uso. Será necessário liberar antes do deploy"
    else
        check_ok "Porta 3000 disponível (Frontend)"
    fi

    # Verificar porta 8000
    if lsof -i:8000 &> /dev/null; then
        check_warn "Porta 8000 está em uso. Será necessário liberar antes do deploy"
    else
        check_ok "Porta 8000 disponível (Backend)"
    fi
elif command -v netstat &> /dev/null; then
    if netstat -tuln | grep ":3000 " &> /dev/null; then
        check_warn "Porta 3000 pode estar em uso"
    else
        check_ok "Porta 3000 provavelmente disponível"
    fi

    if netstat -tuln | grep ":8000 " &> /dev/null; then
        check_warn "Porta 8000 pode estar em uso"
    else
        check_ok "Porta 8000 provavelmente disponível"
    fi
else
    check_warn "Não foi possível verificar portas (lsof/netstat não disponível)"
fi
echo ""

echo -e "${BLUE}7. Verificando Arquivos do Projeto...${NC}"

# Verificar arquivos essenciais
if [ -f "docker-compose.prod.yml" ]; then
    check_ok "docker-compose.prod.yml encontrado"
else
    check_fail "docker-compose.prod.yml NÃO encontrado! Você está na pasta correta?"
fi

if [ -f "deploy.sh" ]; then
    check_ok "deploy.sh encontrado"

    # Verificar se é executável
    if [ -x "deploy.sh" ]; then
        check_ok "deploy.sh é executável"
    else
        check_warn "deploy.sh não é executável. Execute: chmod +x deploy.sh"
    fi
else
    check_fail "deploy.sh NÃO encontrado!"
fi

if [ -d "backend" ]; then
    check_ok "Pasta backend/ encontrada"
else
    check_fail "Pasta backend/ NÃO encontrada!"
fi

if [ -d "frontend" ]; then
    check_ok "Pasta frontend/ encontrada"
else
    check_fail "Pasta frontend/ NÃO encontrada!"
fi

if [ -d "database" ]; then
    check_ok "Pasta database/ encontrada"
else
    check_warn "Pasta database/ NÃO encontrada"
fi
echo ""

echo -e "${BLUE}8. Verificando Configurações...${NC}"

if [ -f ".env.production" ]; then
    check_ok "Arquivo .env.production encontrado"

    # Verificar se a chave OpenAI foi configurada
    if grep -q "sk-COLE_SUA_CHAVE_OPENAI_AQUI" .env.production; then
        check_fail "OPENAI_API_KEY ainda não foi configurada no .env.production!"
        echo -e "${YELLOW}   Edite o arquivo e adicione sua chave OpenAI${NC}"
    elif grep -q "sk-proj-" .env.production || grep -q "sk-" .env.production; then
        # Verificar se não é o placeholder
        if ! grep -q "sk-your-openai-api-key-here" .env.production; then
            check_ok "OPENAI_API_KEY parece estar configurada"
        else
            check_fail "OPENAI_API_KEY ainda é o valor de exemplo!"
        fi
    else
        check_warn "OPENAI_API_KEY pode não estar configurada corretamente"
    fi

    # Verificar se as senhas foram alteradas
    if grep -q "CHANGE_THIS" .env.production; then
        check_warn "Algumas senhas ainda estão como CHANGE_THIS. Recomendado alterar."
    else
        check_ok "Senhas foram alteradas"
    fi

elif [ -f ".env.production.READY" ]; then
    check_warn "Arquivo .env.production.READY encontrado, mas .env.production NÃO"
    echo -e "${YELLOW}   Execute: mv .env.production.READY .env.production${NC}"
else
    check_fail "Arquivo .env.production NÃO encontrado!"
    if [ -f ".env.production.example" ]; then
        echo -e "${YELLOW}   Execute: cp .env.production.example .env.production${NC}"
    fi
fi
echo ""

echo -e "${BLUE}9. Verificando Conectividade...${NC}"

# Verificar conexão com internet
if ping -c 1 google.com &> /dev/null || ping -c 1 8.8.8.8 &> /dev/null; then
    check_ok "Conexão com internet disponível"
else
    check_warn "Não foi possível verificar conexão com internet"
fi

# Verificar acesso ao Docker Hub
if curl -s --connect-timeout 5 https://hub.docker.com &> /dev/null; then
    check_ok "Acesso ao Docker Hub disponível"
else
    check_warn "Não foi possível verificar acesso ao Docker Hub"
fi
echo ""

# ============================================
# RESUMO
# ============================================

echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}📊 RESUMO DA VALIDAÇÃO${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""

echo -e "${GREEN}✓ Checks bem-sucedidos:${NC} $CHECKS_PASSED"
echo -e "${RED}✗ Checks falharam:${NC} $CHECKS_FAILED"
echo -e "${YELLOW}⚠ Avisos:${NC} $WARNINGS"
echo ""

if [ $CHECKS_FAILED -eq 0 ]; then
    echo -e "${GREEN}============================================${NC}"
    echo -e "${GREEN}✓ AMBIENTE PRONTO PARA DEPLOY!${NC}"
    echo -e "${GREEN}============================================${NC}"
    echo ""
    echo -e "Próximo passo:"
    echo -e "  ${BLUE}./deploy.sh${NC}"
    echo -e "  Escolha opção 1: Deploy completo"
    echo ""

    if [ $WARNINGS -gt 0 ]; then
        echo -e "${YELLOW}⚠ Alguns avisos foram encontrados.${NC}"
        echo -e "${YELLOW}  O deploy deve funcionar, mas revise os avisos acima.${NC}"
        echo ""
    fi
else
    echo -e "${RED}============================================${NC}"
    echo -e "${RED}✗ AMBIENTE NÃO ESTÁ PRONTO${NC}"
    echo -e "${RED}============================================${NC}"
    echo ""
    echo -e "${RED}Corrija os problemas acima antes de continuar.${NC}"
    echo ""
    echo -e "Problemas críticos encontrados: ${RED}$CHECKS_FAILED${NC}"
    echo ""
    echo -e "Para ajuda, consulte:"
    echo -e "  ${BLUE}cat EXECUTE_AGORA.md${NC}"
    echo -e "  ${BLUE}cat GUIA_PASSO_A_PASSO.md${NC}"
    echo ""
    exit 1
fi

# ============================================
# VERIFICAÇÃO ADICIONAL: OpenAI API Key
# ============================================

if [ -f ".env.production" ]; then
    echo -e "${BLUE}============================================${NC}"
    echo -e "${BLUE}🔑 VERIFICAÇÃO DA CHAVE OPENAI${NC}"
    echo -e "${BLUE}============================================${NC}"
    echo ""

    OPENAI_KEY=$(grep "^OPENAI_API_KEY=" .env.production | cut -d'=' -f2)

    if [ -n "$OPENAI_KEY" ] && [ "$OPENAI_KEY" != "sk-your-openai-api-key-here" ] && [ "$OPENAI_KEY" != "sk-COLE_SUA_CHAVE_OPENAI_AQUI" ]; then
        KEY_LENGTH=${#OPENAI_KEY}
        if [ $KEY_LENGTH -gt 40 ]; then
            echo -e "${GREEN}✓ Chave OpenAI configurada (${KEY_LENGTH} caracteres)${NC}"
            echo -e "${YELLOW}⚠ Não validamos se a chave é válida. Isso será verificado no deploy.${NC}"
        else
            echo -e "${YELLOW}⚠ Chave OpenAI parece muito curta (${KEY_LENGTH} caracteres)${NC}"
            echo -e "${YELLOW}  Verifique se copiou a chave completa${NC}"
        fi
    else
        echo -e "${RED}✗ Chave OpenAI não configurada!${NC}"
        echo -e ""
        echo -e "Como obter a chave:"
        echo -e "  1. Acesse: ${BLUE}https://platform.openai.com/api-keys${NC}"
        echo -e "  2. Faça login"
        echo -e "  3. Clique em 'Create new secret key'"
        echo -e "  4. Copie a chave (começa com sk-)"
        echo -e "  5. Edite .env.production e cole a chave"
        echo ""
    fi
    echo ""
fi

echo -e "${BLUE}============================================${NC}"
echo -e "${GREEN}Validação concluída!${NC}"
echo -e "${BLUE}============================================${NC}"
