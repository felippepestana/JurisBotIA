#!/usr/bin/env python3
"""
Script de configuração completa do JurisIA Pro
Executa setup do banco, população de dados e testes básicos
"""
import sys
import os
import asyncio
import time
from pathlib import Path

# Adicionar diretório raiz ao path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from app.core.config import settings
from scripts.setup_db import setup_database
from scripts.populate_database import DatabasePopulator
from app.services.cache_service import cache_service
from app.services.vector_service import vector_service
from app.services.openai_service import openai_service
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def print_section(title: str):
    """Imprime seção formatada"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")


def check_services():
    """Verifica status dos serviços"""
    print_section("🔍 VERIFICAÇÃO DE SERVIÇOS")

    services_status = {
        "PostgreSQL": False,
        "Redis": cache_service.is_available(),
        "Qdrant": vector_service.is_available(),
        "OpenAI": openai_service.is_available()
    }

    # Verificar PostgreSQL
    try:
        from sqlalchemy import create_engine
        engine = create_engine(settings.DATABASE_URL)
        with engine.connect():
            services_status["PostgreSQL"] = True
    except Exception as e:
        logger.warning(f"PostgreSQL não disponível: {e}")

    print("Status dos Serviços:")
    for service, status in services_status.items():
        icon = "✅" if status else "❌"
        print(f"  {icon} {service}: {'Disponível' if status else 'Indisponível'}")

    return services_status


def run_database_setup():
    """Configura banco de dados"""
    print_section("🗄️  CONFIGURAÇÃO DO BANCO DE DADOS")

    try:
        setup_database()
        print("✅ Banco de dados configurado com sucesso!")
        return True
    except Exception as e:
        logger.error(f"❌ Erro ao configurar banco: {e}")
        return False


def run_data_population():
    """Popula banco com dados"""
    print_section("📚 POPULAÇÃO DE DADOS")

    try:
        populator = DatabasePopulator()

        # Coletar de scrapers
        documents = populator.collect_from_scrapers()
        print(f"✅ Coletados {len(documents)} documentos dos scrapers")

        # Indexar no Qdrant (se disponível)
        if vector_service.is_available():
            result = populator.index_to_vector_db()
            print(f"✅ Indexados {result['indexed']} documentos no Qdrant")
            if result['failed'] > 0:
                print(f"⚠️  {result['failed']} documentos falharam na indexação")
        else:
            print("⚠️  Qdrant não disponível - pulando indexação vetorial")

        # Salvar no PostgreSQL (futuro)
        print("ℹ️  Salvamento no PostgreSQL será implementado em breve")

        return True
    except Exception as e:
        logger.error(f"❌ Erro ao popular dados: {e}")
        return False


def test_search():
    """Testa funcionalidade de busca"""
    print_section("🔎 TESTE DE BUSCA")

    try:
        test_queries = [
            "CDC instituições financeiras",
            "dano moral",
            "superendividamento"
        ]

        for query in test_queries:
            print(f"\n📝 Buscando: '{query}'")

            # Se vector service disponível, testar busca vetorial
            if vector_service.is_available():
                start = time.time()
                results = vector_service.search(query, limit=3)
                elapsed = (time.time() - start) * 1000

                print(f"   ⏱️  Tempo: {elapsed:.0f}ms")
                print(f"   📊 Resultados: {len(results)}")

                if results:
                    for i, doc in enumerate(results[:2], 1):
                        print(f"   {i}. {doc.get('titulo', 'Sem título')[:60]}...")
                        print(f"      Score: {doc.get('similarity_score', 0):.3f}")
            else:
                print("   ⚠️  Busca vetorial indisponível - usando mock")

        print("\n✅ Testes de busca concluídos")
        return True

    except Exception as e:
        logger.error(f"❌ Erro ao testar busca: {e}")
        return False


def test_cache():
    """Testa funcionalidade de cache"""
    print_section("💾 TESTE DE CACHE")

    if not cache_service.is_available():
        print("⚠️  Redis não disponível - pulando testes de cache")
        return True

    try:
        # Teste básico de get/set
        test_key = "test:juris-ia:startup"
        test_value = {"message": "Cache funcionando!", "timestamp": time.time()}

        cache_service.set(test_key, test_value, ttl=60)
        retrieved = cache_service.get(test_key)

        if retrieved and retrieved.get("message") == test_value["message"]:
            print("✅ Cache set/get funcionando")
        else:
            print("❌ Erro no cache set/get")
            return False

        # Limpar teste
        cache_service.delete(test_key)

        # Mostrar estatísticas
        stats = cache_service.get_stats()
        print(f"\n📊 Estatísticas do Cache:")
        print(f"   Total de chaves: {stats.get('total_keys', 0)}")
        print(f"   Memória usada: {stats.get('used_memory_human', 'N/A')}")

        return True

    except Exception as e:
        logger.error(f"❌ Erro ao testar cache: {e}")
        return False


def test_openai():
    """Testa integração OpenAI"""
    print_section("🤖 TESTE DE INTEGRAÇÃO OPENAI")

    if not openai_service.is_available():
        print("⚠️  OpenAI não disponível - configure OPENAI_API_KEY")
        return True

    try:
        # Teste de embedding
        print("Testando geração de embeddings...")
        test_text = "Código de Defesa do Consumidor"
        embedding = openai_service.generate_embedding(test_text)

        if embedding and len(embedding) == 3072:
            print(f"✅ Embedding gerado: {len(embedding)} dimensões")
        else:
            print("❌ Erro ao gerar embedding")
            return False

        print("\n✅ Integração OpenAI funcionando")
        return True

    except Exception as e:
        logger.error(f"❌ Erro ao testar OpenAI: {e}")
        return False


def print_summary(results: dict):
    """Imprime resumo dos testes"""
    print_section("📋 RESUMO")

    total = len(results)
    passed = sum(1 for r in results.values() if r)
    failed = total - passed

    print("Resultados dos Testes:")
    for test_name, result in results.items():
        icon = "✅" if result else "❌"
        print(f"  {icon} {test_name}")

    print(f"\n{'='*80}")
    print(f"Total: {passed}/{total} testes passaram")

    if failed == 0:
        print("🎉 Sistema configurado com sucesso!")
        print("\n💡 Próximos passos:")
        print("   1. Inicie o servidor: uvicorn app.main:app --reload")
        print("   2. Acesse a documentação: http://localhost:8000/docs")
        print("   3. Teste os endpoints via API")
    else:
        print(f"⚠️  {failed} teste(s) falharam - verifique os logs acima")


def main():
    """Função principal"""
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*20 + "JurisIA Pro - Setup Completo" + " "*30 + "║")
    print("╚" + "="*78 + "╝")

    results = {}

    # 1. Verificar serviços
    services = check_services()

    # 2. Setup do banco (se PostgreSQL disponível)
    if services["PostgreSQL"]:
        results["Database Setup"] = run_database_setup()
    else:
        print("\n⚠️  PostgreSQL indisponível - pulando setup do banco")
        results["Database Setup"] = False

    # 3. Popular dados
    results["Data Population"] = run_data_population()

    # 4. Testes
    results["Cache Test"] = test_cache()
    results["Search Test"] = test_search()
    results["OpenAI Test"] = test_openai()

    # 5. Resumo
    print_summary(results)

    # Status de saída
    sys.exit(0 if all(results.values()) else 1)


if __name__ == "__main__":
    main()
