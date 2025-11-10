#!/bin/bash
# Script de Deploy do JurisIA Pro

set -e

echo "🏛️  JurisIA Pro - Deploy Script"
echo "================================"
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar se está na pasta correta
if [ ! -f "docker-compose.prod.yml" ]; then
    echo -e "${RED}❌ Erro: docker-compose.prod.yml não encontrado!${NC}"
    echo "Execute este script na raiz do projeto."
    exit 1
fi

# Verificar se .env.production existe
if [ ! -f ".env.production" ]; then
    echo -e "${YELLOW}⚠️  Arquivo .env.production não encontrado!${NC}"
    echo "Copiando .env.production.example..."
    cp .env.production.example .env.production
    echo -e "${YELLOW}⚠️  Configure o arquivo .env.production antes de continuar!${NC}"
    echo "Edite o arquivo e execute este script novamente."
    exit 1
fi

# Verificar se Docker está rodando
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker não está rodando!${NC}"
    echo "Inicie o Docker e tente novamente."
    exit 1
fi

# Verificar se docker-compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ docker-compose não encontrado!${NC}"
    echo "Instale docker-compose e tente novamente."
    exit 1
fi

echo -e "${GREEN}✅ Pré-requisitos verificados${NC}"
echo ""

# Menu de opções
echo "Selecione a ação:"
echo "1) Deploy completo (primeira vez)"
echo "2) Rebuild e restart"
echo "3) Parar serviços"
echo "4) Ver logs"
echo "5) Status dos serviços"
echo "6) Backup do banco de dados"
echo "7) Restaurar banco de dados"
echo "0) Sair"
echo ""
read -p "Escolha uma opção: " option

case $option in
    1)
        echo -e "${GREEN}🚀 Iniciando deploy completo...${NC}"
        
        # Pull das imagens
        echo "📥 Baixando imagens Docker..."
        docker-compose -f docker-compose.prod.yml --env-file .env.production pull
        
        # Build das imagens custom
        echo "🔨 Construindo imagens..."
        docker-compose -f docker-compose.prod.yml --env-file .env.production build --no-cache
        
        # Subir serviços
        echo "🚀 Iniciando serviços..."
        docker-compose -f docker-compose.prod.yml --env-file .env.production up -d
        
        # Aguardar serviços ficarem healthy
        echo "⏳ Aguardando serviços ficarem prontos..."
        sleep 10
        
        # Executar migrations/setup
        echo "📊 Configurando banco de dados..."
        docker-compose -f docker-compose.prod.yml --env-file .env.production exec backend python scripts/setup_db.py
        
        # Popular dados iniciais
        echo "📚 Populando dados iniciais..."
        docker-compose -f docker-compose.prod.yml --env-file .env.production exec backend python scripts/populate_database.py
        
        echo -e "${GREEN}✅ Deploy concluído com sucesso!${NC}"
        echo ""
        echo "🌐 Acesse:"
        echo "   Frontend: http://localhost:3000"
        echo "   Backend:  http://localhost:8000"
        echo "   API Docs: http://localhost:8000/docs"
        ;;
        
    2)
        echo -e "${YELLOW}🔄 Rebuild e restart...${NC}"
        docker-compose -f docker-compose.prod.yml --env-file .env.production down
        docker-compose -f docker-compose.prod.yml --env-file .env.production build
        docker-compose -f docker-compose.prod.yml --env-file .env.production up -d
        echo -e "${GREEN}✅ Serviços reiniciados!${NC}"
        ;;
        
    3)
        echo -e "${YELLOW}🛑 Parando serviços...${NC}"
        docker-compose -f docker-compose.prod.yml --env-file .env.production down
        echo -e "${GREEN}✅ Serviços parados!${NC}"
        ;;
        
    4)
        echo -e "${GREEN}📋 Mostrando logs (Ctrl+C para sair)...${NC}"
        docker-compose -f docker-compose.prod.yml --env-file .env.production logs -f
        ;;
        
    5)
        echo -e "${GREEN}📊 Status dos serviços:${NC}"
        docker-compose -f docker-compose.prod.yml --env-file .env.production ps
        echo ""
        echo "Health checks:"
        docker-compose -f docker-compose.prod.yml --env-file .env.production ps | grep -E "(healthy|unhealthy)"
        ;;
        
    6)
        echo -e "${GREEN}💾 Criando backup...${NC}"
        timestamp=$(date +%Y%m%d_%H%M%S)
        docker-compose -f docker-compose.prod.yml --env-file .env.production exec -T postgres pg_dump -U juris_user juris_ia_pro > "backup_${timestamp}.sql"
        echo -e "${GREEN}✅ Backup criado: backup_${timestamp}.sql${NC}"
        ;;
        
    7)
        echo -e "${YELLOW}⚠️  Restaurar banco de dados${NC}"
        read -p "Nome do arquivo de backup: " backup_file
        if [ -f "$backup_file" ]; then
            docker-compose -f docker-compose.prod.yml --env-file .env.production exec -T postgres psql -U juris_user juris_ia_pro < "$backup_file"
            echo -e "${GREEN}✅ Banco restaurado!${NC}"
        else
            echo -e "${RED}❌ Arquivo não encontrado!${NC}"
        fi
        ;;
        
    0)
        echo "Saindo..."
        exit 0
        ;;
        
    *)
        echo -e "${RED}❌ Opção inválida!${NC}"
        exit 1
        ;;
esac

echo ""
echo "✅ Operação concluída!"
