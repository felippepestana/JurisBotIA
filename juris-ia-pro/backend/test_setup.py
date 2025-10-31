#!/usr/bin/env python3
"""
Script de teste para validar o setup do backend
"""
import sys
import os

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_imports():
    """Testa se todos os imports necessários funcionam"""
    print("🧪 Testando imports...")

    try:
        from app.core.config import settings
        print("✅ app.core.config")
    except Exception as e:
        print(f"❌ app.core.config: {e}")
        return False

    try:
        from app.core.database import engine, SessionLocal
        print("✅ app.core.database")
    except Exception as e:
        print(f"❌ app.core.database: {e}")
        return False

    try:
        from app.models.schemas import SearchRequest, ChatMessage
        print("✅ app.models.schemas")
    except Exception as e:
        print(f"❌ app.models.schemas: {e}")
        return False

    try:
        from app.main import app
        print("✅ app.main")
    except Exception as e:
        print(f"❌ app.main: {e}")
        return False

    return True


def test_config():
    """Testa as configurações"""
    print("\n🧪 Testando configurações...")

    try:
        from app.core.config import settings, validate_critical_settings

        print(f"   APP_NAME: {settings.APP_NAME}")
        print(f"   APP_VERSION: {settings.APP_VERSION}")
        print(f"   APP_ENV: {settings.APP_ENV}")
        print(f"   DATABASE_URL: {settings.DATABASE_URL[:30]}...")
        print(f"   OPENAI_API_KEY: {'✅ Configurada' if settings.OPENAI_API_KEY else '❌ NÃO configurada'}")

        validate_critical_settings()
        print("✅ Configurações validadas")
        return True

    except Exception as e:
        print(f"⚠️  Aviso de configuração: {e}")
        return True  # Não falhar no dev


def test_database_connection():
    """Testa conexão com banco"""
    print("\n🧪 Testando conexão com banco de dados...")

    try:
        from app.core.database import check_db_connection, get_db_stats

        if check_db_connection():
            print("✅ Conexão com banco estabelecida")
            stats = get_db_stats()
            print(f"   Pool size: {stats['size']}")
            print(f"   Checked out: {stats['checked_out']}")
            return True
        else:
            print("❌ Falha ao conectar no banco")
            print("   → Execute: docker-compose up -d")
            return False

    except Exception as e:
        print(f"❌ Erro ao testar banco: {e}")
        print("   → Execute: docker-compose up -d")
        return False


def test_fastapi_app():
    """Testa se a aplicação FastAPI pode ser iniciada"""
    print("\n🧪 Testando aplicação FastAPI...")

    try:
        from app.main import app
        from fastapi.testclient import TestClient

        client = TestClient(app)

        # Test root endpoint
        response = client.get("/")
        if response.status_code == 200:
            print("✅ Root endpoint funcionando")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Root endpoint retornou {response.status_code}")
            return False

        # Test health endpoint
        response = client.get("/health")
        if response.status_code == 200:
            print("✅ Health endpoint funcionando")
            health_data = response.json()
            print(f"   Status: {health_data['status']}")
            print(f"   Database: {health_data['database']}")
        else:
            print(f"❌ Health endpoint retornou {response.status_code}")
            return False

        return True

    except Exception as e:
        print(f"❌ Erro ao testar FastAPI: {e}")
        return False


def main():
    """Função principal"""
    print("=" * 60)
    print("🚀 TESTE DE SETUP - JURISIA PRO BACKEND")
    print("=" * 60)

    results = []

    # Teste 1: Imports
    results.append(("Imports", test_imports()))

    # Teste 2: Configurações
    results.append(("Configurações", test_config()))

    # Teste 3: Database
    results.append(("Database", test_database_connection()))

    # Teste 4: FastAPI
    results.append(("FastAPI App", test_fastapi_app()))

    # Resumo
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)

    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{test_name:.<40} {status}")

    total_passed = sum(1 for _, result in results if result)
    total_tests = len(results)

    print(f"\nTotal: {total_passed}/{total_tests} testes passaram")

    if total_passed == total_tests:
        print("\n🎉 Todos os testes passaram! Sistema pronto para usar.")
        print("\n💡 Próximos passos:")
        print("   1. Configure OPENAI_API_KEY no arquivo .env")
        print("   2. Execute: python -m app.main")
        print("   3. Acesse: http://localhost:8000/docs")
        return 0
    else:
        print("\n⚠️  Alguns testes falharam. Verifique os erros acima.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
