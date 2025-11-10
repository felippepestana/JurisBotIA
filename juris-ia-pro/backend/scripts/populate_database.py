#!/usr/bin/env python3
"""
Script para popular banco de dados com documentos jurídicos
Usa scrapers e serviços de embedding/vector
"""
import sys
import os
import logging
from datetime import datetime
from typing import List, Dict, Any

# Adicionar diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.scrapers.planalto_scraper import PlanaltoScraper
from app.scrapers.stj_scraper import STJScraper
from app.services.vector_service import vector_service
from app.core.mock_data import MOCK_LEGAL_DOCUMENTS

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DatabasePopulator:
    """Classe para popular banco de dados"""

    def __init__(self):
        """Inicializa populador"""
        self.documents_collected = []
        self.stats = {
            "total_scraped": 0,
            "total_indexed": 0,
            "total_failed": 0,
            "sources": {}
        }

    def collect_from_scrapers(self) -> List[Dict[str, Any]]:
        """
        Coleta documentos de todos os scrapers.

        Returns:
            Lista de documentos coletados
        """
        logger.info("=" * 60)
        logger.info("INICIANDO COLETA DE DOCUMENTOS JURÍDICOS")
        logger.info("=" * 60)

        # 1. Documentos mockados (base inicial)
        logger.info("\n📚 Adicionando documentos mockados...")
        mock_docs = list(MOCK_LEGAL_DOCUMENTS)
        self.documents_collected.extend(mock_docs)
        self.stats["sources"]["mock"] = len(mock_docs)
        logger.info(f"✅ {len(mock_docs)} documentos mockados adicionados")

        # 2. Scraper do Planalto
        logger.info("\n🏛️ Scraping Planalto (Legislação Federal)...")
        try:
            planalto_scraper = PlanaltoScraper()
            planalto_docs = planalto_scraper.scrape(scrape_mode="important")

            self.documents_collected.extend(planalto_docs)
            self.stats["sources"]["planalto"] = len(planalto_docs)

            logger.info(f"✅ {len(planalto_docs)} leis coletadas do Planalto")
        except Exception as e:
            logger.error(f"❌ Erro no scraper Planalto: {e}")
            self.stats["sources"]["planalto"] = 0

        # 3. Scraper do STJ
        logger.info("\n⚖️ Scraping STJ (Súmulas)...")
        try:
            stj_scraper = STJScraper()
            stj_sumulas = stj_scraper.scrape(scrape_mode="sumulas", limit=8)

            self.documents_collected.extend(stj_sumulas)
            self.stats["sources"]["stj_sumulas"] = len(stj_sumulas)

            logger.info(f"✅ {len(stj_sumulas)} súmulas coletadas do STJ")
        except Exception as e:
            logger.error(f"❌ Erro no scraper STJ: {e}")
            self.stats["sources"]["stj_sumulas"] = 0

        logger.info("\n⚖️ Scraping STJ (Jurisprudência)...")
        try:
            stj_scraper = STJScraper()
            stj_jurisp = stj_scraper.scrape(scrape_mode="jurisprudencia", limit=3)

            self.documents_collected.extend(stj_jurisp)
            self.stats["sources"]["stj_jurisprudencia"] = len(stj_jurisp)

            logger.info(f"✅ {len(stj_jurisp)} acórdãos coletados do STJ")
        except Exception as e:
            logger.error(f"❌ Erro no scraper STJ jurisprudência: {e}")
            self.stats["sources"]["stj_jurisprudencia"] = 0

        # Total
        self.stats["total_scraped"] = len(self.documents_collected)

        logger.info("\n" + "=" * 60)
        logger.info(f"📊 TOTAL COLETADO: {self.stats['total_scraped']} documentos")
        logger.info("=" * 60)

        return self.documents_collected

    def index_to_vector_db(self) -> Dict[str, int]:
        """
        Indexa documentos no banco vetorial (Qdrant).

        Returns:
            Dict com estatísticas de indexação
        """
        logger.info("\n" + "=" * 60)
        logger.info("INDEXANDO DOCUMENTOS NO BANCO VETORIAL")
        logger.info("=" * 60)

        if not vector_service.is_available():
            logger.warning("⚠️ Serviço vetorial não disponível - pulando indexação")
            return {"success": 0, "failed": 0}

        if not self.documents_collected:
            logger.warning("⚠️ Nenhum documento para indexar")
            return {"success": 0, "failed": 0}

        # Indexar em lote
        result = vector_service.add_documents_batch(
            documents=self.documents_collected,
            text_field="conteudo_completo"
        )

        self.stats["total_indexed"] = result["success"]
        self.stats["total_failed"] = result["failed"]

        logger.info("\n" + "=" * 60)
        logger.info(f"✅ INDEXADOS: {result['success']} documentos")
        logger.info(f"❌ FALHAS: {result['failed']} documentos")
        logger.info("=" * 60)

        return result

    def save_to_mock_data(self, filename: str = "collected_documents.py"):
        """
        Salva documentos coletados como arquivo Python.

        Args:
            filename: Nome do arquivo
        """
        logger.info(f"\n💾 Salvando documentos em {filename}...")

        try:
            import json
            from datetime import date

            # Converter datas para strings
            docs_serializable = []
            for doc in self.documents_collected:
                doc_copy = doc.copy()

                # Converter date para string
                if isinstance(doc_copy.get('data_publicacao'), date):
                    doc_copy['data_publicacao'] = doc_copy['data_publicacao'].isoformat()
                if isinstance(doc_copy.get('data_julgamento'), date):
                    doc_copy['data_julgamento'] = doc_copy['data_julgamento'].isoformat()

                docs_serializable.append(doc_copy)

            # Salvar
            output_file = os.path.join(
                os.path.dirname(__file__),
                filename
            )

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("# Documentos jurídicos coletados automaticamente\n")
                f.write(f"# Data: {datetime.now().isoformat()}\n")
                f.write(f"# Total: {len(docs_serializable)} documentos\n\n")
                f.write("COLLECTED_DOCUMENTS = ")
                f.write(json.dumps(docs_serializable, indent=2, ensure_ascii=False))

            logger.info(f"✅ Documentos salvos em: {output_file}")

        except Exception as e:
            logger.error(f"❌ Erro ao salvar documentos: {e}")

    def print_summary(self):
        """Imprime resumo da execução"""
        logger.info("\n" + "=" * 60)
        logger.info("📊 RESUMO DA POPULAÇÃO DO BANCO DE DADOS")
        logger.info("=" * 60)

        logger.info(f"\n🔢 TOTAIS:")
        logger.info(f"   Documentos coletados: {self.stats['total_scraped']}")
        logger.info(f"   Documentos indexados: {self.stats['total_indexed']}")
        logger.info(f"   Falhas na indexação: {self.stats['total_failed']}")

        logger.info(f"\n📚 POR FONTE:")
        for source, count in self.stats['sources'].items():
            logger.info(f"   {source}: {count} documentos")

        logger.info("\n" + "=" * 60)


def main():
    """Função principal"""
    logger.info("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   JURISIA PRO - POPULAÇÃO DO BANCO DE DADOS             ║
║   Sistema de coleta e indexação de documentos jurídicos ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
    """)

    populator = DatabasePopulator()

    try:
        # 1. Coletar documentos
        documents = populator.collect_from_scrapers()

        if not documents:
            logger.error("❌ Nenhum documento foi coletado!")
            return 1

        # 2. Indexar no banco vetorial (se disponível)
        populator.index_to_vector_db()

        # 3. Salvar em arquivo (backup)
        populator.save_to_mock_data()

        # 4. Resumo
        populator.print_summary()

        logger.info("\n✅ PROCESSO CONCLUÍDO COM SUCESSO!\n")
        return 0

    except KeyboardInterrupt:
        logger.warning("\n⚠️ Processo interrompido pelo usuário")
        return 1

    except Exception as e:
        logger.error(f"\n❌ Erro fatal: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
