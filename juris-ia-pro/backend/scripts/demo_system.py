#!/usr/bin/env python3
"""
Script de demonstração do JurisIA Pro
Mostra as funcionalidades principais do sistema em ação
"""
import sys
import os
import asyncio
import time
from pathlib import Path
import json

# Adicionar diretório raiz ao path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from app.services.cache_service import cache_service
from app.services.vector_service import vector_service
from app.services.openai_service import openai_service
from app.core.mock_data import search_mock_documents
import logging

logging.basicConfig(
    level=logging.WARNING,  # Menos verbose para demo
    format='%(message)s'
)
logger = logging.getLogger(__name__)


def print_header(text: str, char="="):
    """Imprime cabeçalho formatado"""
    width = 80
    print("\n" + char * width)
    print(f"  {text}")
    print(char * width + "\n")


def print_subheader(text: str):
    """Imprime subcabeçalho formatado"""
    print(f"\n{'─' * 80}")
    print(f"  {text}")
    print(f"{'─' * 80}\n")


def print_success(text: str):
    """Imprime mensagem de sucesso"""
    print(f"✅ {text}")


def print_info(text: str):
    """Imprime informação"""
    print(f"ℹ️  {text}")


def print_warning(text: str):
    """Imprime aviso"""
    print(f"⚠️  {text}")


def print_result(label: str, value: any, indent=2):
    """Imprime resultado formatado"""
    spaces = " " * indent
    print(f"{spaces}{label}: {value}")


def check_services():
    """Verifica e mostra status dos serviços"""
    print_header("🔍 VERIFICAÇÃO DE SERVIÇOS", "=")

    services = {
        "Redis Cache": cache_service.is_available(),
        "Qdrant Vector DB": vector_service.is_available(),
        "OpenAI API": openai_service.is_available()
    }

    for service, status in services.items():
        if status:
            print_success(f"{service}: Disponível")
        else:
            print_warning(f"{service}: Indisponível (usando fallback)")

    print()
    return services


def demo_search():
    """Demonstra busca jurídica"""
    print_header("🔎 DEMONSTRAÇÃO: BUSCA JURÍDICA")

    query = "CDC instituições financeiras"
    print_info(f"Buscando: '{query}'")

    # Primeira busca (sem cache)
    print_subheader("📊 Primeira Busca (sem cache)")
    start = time.time()

    if vector_service.is_available():
        print_info("Usando busca vetorial semântica (Qdrant + OpenAI)")
        results = vector_service.search(query, limit=3)
    else:
        print_info("Usando dados mockados (vector DB indisponível)")
        results = search_mock_documents(query, limit=3)

    time_first = (time.time() - start) * 1000

    print_result("⏱️  Tempo", f"{time_first:.0f}ms")
    print_result("📄 Resultados", len(results))

    if results:
        print("\n  📌 Top 3 Documentos:")
        for i, doc in enumerate(results[:3], 1):
            titulo = doc.get("titulo", "Sem título")
            score = doc.get("similarity_score", doc.get("relevancia_score", 0))
            print(f"     {i}. {titulo[:60]}...")
            print(f"        Score: {score:.3f}")

    # Segunda busca (com cache se disponível)
    if cache_service.is_available():
        print_subheader("💨 Segunda Busca (com cache)")
        start = time.time()

        # Cachear primeira busca
        cache_key = f"demo:search:{query}"
        cache_service.set(cache_key, results, ttl=300)

        # Buscar novamente
        cached_results = cache_service.get(cache_key)
        time_cached = (time.time() - start) * 1000

        print_result("⏱️  Tempo", f"{time_cached:.0f}ms")
        print_result("⚡ Ganho de velocidade", f"{time_first/time_cached:.1f}x mais rápido")
        print_success(f"Cache economizou {time_first - time_cached:.0f}ms!")

        # Limpar cache de demo
        cache_service.delete(cache_key)


def demo_chat():
    """Demonstra chat jurídico"""
    print_header("💬 DEMONSTRAÇÃO: CHAT JURÍDICO")

    question = "O CDC se aplica a bancos?"
    print_info(f"Pergunta: '{question}'")

    # Buscar documentos relevantes
    print_subheader("📚 Buscando contexto")

    if vector_service.is_available():
        documents = vector_service.search(question, limit=3)
        print_success(f"Encontrados {len(documents)} documentos relevantes")
    else:
        documents = search_mock_documents(question, limit=3)
        print_info(f"Usando {len(documents)} documentos mockados")

    # Gerar resposta
    print_subheader("🤖 Gerando resposta com IA")

    start = time.time()

    if openai_service.is_available():
        print_info("Usando OpenAI GPT-4 com RAG")
        try:
            response, confidence = openai_service.generate_legal_response(
                query=question,
                documents=documents
            )
            time_response = (time.time() - start) * 1000

            print_result("⏱️  Tempo", f"{time_response:.0f}ms")
            print_result("🎯 Confiança", f"{confidence:.1%}")

            print("\n  📝 Resposta:")
            # Mostrar apenas primeiras 3 linhas
            lines = response.split('\n')[:5]
            for line in lines:
                if line.strip():
                    print(f"     {line}")
            if len(response.split('\n')) > 5:
                print("     ...")

        except Exception as e:
            print_warning(f"Erro com OpenAI: {e}")
            print_info("Usando resposta mockada")
    else:
        print_info("OpenAI indisponível, usando resposta mockada")
        response = "Sim, conforme Súmula 297 do STJ, o CDC aplica-se às instituições financeiras."
        confidence = 0.85
        time_response = 100

        print_result("⏱️  Tempo", f"{time_response:.0f}ms")
        print_result("🎯 Confiança", f"{confidence:.1%}")
        print(f"\n  📝 Resposta: {response}")


def demo_cache_stats():
    """Mostra estatísticas do cache"""
    if not cache_service.is_available():
        return

    print_header("📊 ESTATÍSTICAS DO CACHE")

    stats = cache_service.get_stats()

    print_result("🔑 Total de chaves", stats.get("total_keys", 0))
    print_result("💾 Memória usada", stats.get("used_memory_human", "N/A"))
    print_result("📈 Pico de memória", stats.get("used_memory_peak_human", "N/A"))
    print_result("🔄 Operações totais", stats.get("total_commands_processed", 0))
    print_result("📍 Conexões", stats.get("connected_clients", 0))


def demo_vector_stats():
    """Mostra estatísticas do vector DB"""
    if not vector_service.is_available():
        return

    print_header("🗂️  ESTATÍSTICAS DO VECTOR DATABASE")

    info = vector_service.collection_info()

    print_result("📦 Collection", info.get("collection_name", "N/A"))
    print_result("📄 Documentos indexados", info.get("vectors_count", 0))
    print_result("📏 Dimensões do vetor", info.get("vector_size", 0))
    print_result("⚡ Status", info.get("status", "unknown"))


def demo_performance_comparison():
    """Compara performance com e sem cache"""
    print_header("⚡ COMPARAÇÃO DE PERFORMANCE")

    if not cache_service.is_available():
        print_warning("Cache indisponível - não é possível fazer comparação")
        return

    query = "responsabilidade civil"
    iterations = 5

    print_info(f"Executando {iterations} buscas para '{query}'")

    # Sem cache (limpar antes)
    cache_key = f"perf:test:{query}"
    cache_service.delete(cache_key)

    print_subheader("🐌 Sem Cache")
    times_no_cache = []

    for i in range(iterations):
        start = time.time()

        if vector_service.is_available():
            vector_service.search(query, limit=5)
        else:
            search_mock_documents(query, limit=5)

        elapsed = (time.time() - start) * 1000
        times_no_cache.append(elapsed)
        print(f"  Busca {i+1}: {elapsed:.0f}ms")

    avg_no_cache = sum(times_no_cache) / len(times_no_cache)

    # Com cache
    print_subheader("🚀 Com Cache")

    # Cachear resultado
    if vector_service.is_available():
        result = vector_service.search(query, limit=5)
    else:
        result = search_mock_documents(query, limit=5)

    cache_service.set(cache_key, result, ttl=300)

    times_with_cache = []

    for i in range(iterations):
        start = time.time()
        cache_service.get(cache_key)
        elapsed = (time.time() - start) * 1000
        times_with_cache.append(elapsed)
        print(f"  Busca {i+1}: {elapsed:.0f}ms")

    avg_with_cache = sum(times_with_cache) / len(times_with_cache)

    # Resultados
    print_subheader("📈 Resultados")
    print_result("⏱️  Média sem cache", f"{avg_no_cache:.0f}ms")
    print_result("⏱️  Média com cache", f"{avg_with_cache:.0f}ms")
    print_result("🚀 Ganho de velocidade", f"{avg_no_cache/avg_with_cache:.1f}x")
    print_result("💰 Economia de tempo", f"{avg_no_cache - avg_with_cache:.0f}ms por busca")

    # Limpar
    cache_service.delete(cache_key)


def print_summary():
    """Imprime resumo do sistema"""
    print_header("📋 RESUMO DO SISTEMA", "=")

    services = {
        "Redis": cache_service.is_available(),
        "Qdrant": vector_service.is_available(),
        "OpenAI": openai_service.is_available()
    }

    features = {
        "✅ Busca Jurídica": "Com cache e busca vetorial",
        "✅ Chat com IA": "GPT-4 com RAG",
        "✅ Análise de PDF": "Processos judiciais",
        "✅ Geração de Documentos": "Petições e contratos",
        "✅ Cache Redis": "Performance otimizada" if services["Redis"] else "Indisponível",
        "✅ Busca Semântica": "Qdrant + OpenAI" if services["Qdrant"] else "Dados mockados"
    }

    print("Serviços Disponíveis:")
    for service, status in services.items():
        icon = "🟢" if status else "🔴"
        print(f"  {icon} {service}")

    print("\nFuncionalidades:")
    for feature, description in features.items():
        print(f"  {feature}")
        print(f"     └─ {description}")

    print("\n" + "="*80)
    print("  💡 Próximos passos:")
    print("     1. Iniciar servidor: uvicorn app.main:app --reload")
    print("     2. Acessar docs: http://localhost:8000/docs")
    print("     3. Testar endpoints via API")
    print("="*80 + "\n")


def main():
    """Função principal"""
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*22 + "JurisIA Pro - Demo Completo" + " "*29 + "║")
    print("╚" + "="*78 + "╝")
    print()

    try:
        # 1. Verificar serviços
        services = check_services()

        input("📍 Pressione ENTER para continuar com a demonstração...\n")

        # 2. Demo de busca
        demo_search()

        input("\n📍 Pressione ENTER para continuar...\n")

        # 3. Demo de chat
        demo_chat()

        input("\n📍 Pressione ENTER para continuar...\n")

        # 4. Estatísticas
        if services["Redis Cache"]:
            demo_cache_stats()

        if services["Qdrant Vector DB"]:
            demo_vector_stats()

        input("\n📍 Pressione ENTER para teste de performance...\n")

        # 5. Performance
        if services["Redis Cache"]:
            demo_performance_comparison()

        # 6. Resumo
        print_summary()

        print_success("Demonstração concluída!")

    except KeyboardInterrupt:
        print("\n\n⚠️  Demonstração interrompida pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Erro durante demonstração: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
