#!/usr/bin/env python3
"""
Script para configurar banco de dados
Cria tabelas, índices e dados iniciais
"""
import sys
import os
import logging

# Adicionar diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import engine, Base, check_db_connection
from app.core.config import settings

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def setup_database():
    """Configura banco de dados"""
    logger.info("=" * 60)
    logger.info("CONFIGURAÇÃO DO BANCO DE DADOS")
    logger.info("=" * 60)

    # 1. Verificar conexão
    logger.info("\n1️⃣ Verificando conexão com banco de dados...")
    if not check_db_connection():
        logger.error("❌ Não foi possível conectar ao banco de dados!")
        logger.error(f"   URL: {settings.DATABASE_URL}")
        logger.error("\n💡 Certifique-se de que:")
        logger.error("   - PostgreSQL está rodando")
        logger.error("   - DATABASE_URL está correto no .env")
        logger.error("   - Banco de dados existe")
        return False

    logger.info("✅ Conexão estabelecida com sucesso!")

    # 2. Criar tabelas
    logger.info("\n2️⃣ Criando tabelas...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Tabelas criadas com sucesso!")
    except Exception as e:
        logger.error(f"❌ Erro ao criar tabelas: {e}")
        return False

    # 3. Verificar tabelas criadas
    logger.info("\n3️⃣ Verificando tabelas criadas...")
    try:
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()

        if tables:
            logger.info(f"✅ {len(tables)} tabelas encontradas:")
            for table in sorted(tables):
                logger.info(f"   - {table}")
        else:
            logger.warning("⚠️ Nenhuma tabela encontrada")

    except Exception as e:
        logger.error(f"❌ Erro ao verificar tabelas: {e}")

    logger.info("\n" + "=" * 60)
    logger.info("✅ CONFIGURAÇÃO CONCLUÍDA!")
    logger.info("=" * 60)

    return True


def main():
    """Função principal"""
    logger.info("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   JURISIA PRO - SETUP DO BANCO DE DADOS                 ║
║   Configuração inicial do PostgreSQL                    ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
    """)

    try:
        success = setup_database()

        if success:
            logger.info("\n💡 Próximos passos:")
            logger.info("   1. Execute: python scripts/populate_database.py")
            logger.info("   2. Inicie a API: python -m app.main")
            logger.info("   3. Acesse: http://localhost:8000/docs\n")
            return 0
        else:
            logger.error("\n❌ Setup falhou. Verifique os erros acima.\n")
            return 1

    except KeyboardInterrupt:
        logger.warning("\n⚠️ Setup interrompido pelo usuário\n")
        return 1

    except Exception as e:
        logger.error(f"\n❌ Erro fatal: {e}\n", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
