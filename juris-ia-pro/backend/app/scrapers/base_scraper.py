"""
Classe base para scrapers de dados jurídicos
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import time
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import settings

logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """Classe base para todos os scrapers"""

    def __init__(self, source_name: str, base_url: str):
        """
        Inicializa o scraper.

        Args:
            source_name: Nome da fonte (ex: "STF", "STJ")
            base_url: URL base do site
        """
        self.source_name = source_name
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': settings.SCRAPING_USER_AGENT
        })
        self.documents_scraped = []

    @abstractmethod
    def scrape(self, **kwargs) -> List[Dict[str, Any]]:
        """
        Método principal de scraping.
        Deve ser implementado por cada scraper específico.

        Returns:
            Lista de documentos scrapeados
        """
        pass

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def fetch_page(self, url: str, timeout: int = 30) -> Optional[str]:
        """
        Faz fetch de uma página com retry.

        Args:
            url: URL para fazer fetch
            timeout: Timeout em segundos

        Returns:
            HTML da página ou None se falhar
        """
        try:
            logger.info(f"Fetching: {url}")
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()

            logger.info(f"✅ Fetch successful: {url} ({response.status_code})")
            return response.text

        except requests.RequestException as e:
            logger.error(f"❌ Erro ao fazer fetch de {url}: {e}")
            raise

    def parse_html(self, html: str) -> BeautifulSoup:
        """
        Parse HTML com BeautifulSoup.

        Args:
            html: String HTML

        Returns:
            Objeto BeautifulSoup
        """
        return BeautifulSoup(html, 'lxml')

    def extract_text(self, element) -> str:
        """
        Extrai texto limpo de um elemento HTML.

        Args:
            element: Elemento BeautifulSoup

        Returns:
            Texto limpo
        """
        if element is None:
            return ""

        text = element.get_text(separator=' ', strip=True)
        # Limpar espaços múltiplos
        text = ' '.join(text.split())

        return text

    def normalize_date(self, date_str: str) -> Optional[datetime]:
        """
        Normaliza string de data para datetime.

        Args:
            date_str: String de data em formato BR

        Returns:
            Objeto datetime ou None
        """
        # Formatos comuns brasileiros
        formats = [
            "%d/%m/%Y",
            "%d-%m-%Y",
            "%d.%m.%Y",
            "%Y-%m-%d",
            "%d/%m/%Y %H:%M",
            "%d/%m/%Y %H:%M:%S"
        ]

        for fmt in formats:
            try:
                return datetime.strptime(date_str.strip(), fmt)
            except ValueError:
                continue

        logger.warning(f"Não foi possível parsear data: {date_str}")
        return None

    def save_document(self, document: Dict[str, Any]) -> None:
        """
        Salva documento na lista de scrapeados.

        Args:
            document: Dicionário com dados do documento
        """
        # Validação mínima
        required_fields = ['titulo', 'conteudo_completo', 'tipo_documento']

        if all(field in document for field in required_fields):
            document['scraped_at'] = datetime.utcnow()
            document['source'] = self.source_name
            self.documents_scraped.append(document)
            logger.info(f"✅ Documento salvo: {document['titulo'][:50]}...")
        else:
            missing = [f for f in required_fields if f not in document]
            logger.warning(f"⚠️ Documento incompleto, faltam: {missing}")

    def get_documents(self) -> List[Dict[str, Any]]:
        """
        Retorna todos os documentos scrapeados.

        Returns:
            Lista de documentos
        """
        return self.documents_scraped

    def clear_documents(self) -> None:
        """Limpa lista de documentos scrapeados"""
        self.documents_scraped = []

    def rate_limit(self, seconds: float = 1.0) -> None:
        """
        Rate limiting entre requisições.

        Args:
            seconds: Segundos para aguardar
        """
        time.sleep(seconds)

    def log_progress(self, current: int, total: int, item: str = "items") -> None:
        """
        Log de progresso.

        Args:
            current: Item atual
            total: Total de items
            item: Nome do item (ex: "documentos")
        """
        percentage = (current / total * 100) if total > 0 else 0
        logger.info(
            f"[{self.source_name}] Progresso: {current}/{total} {item} "
            f"({percentage:.1f}%)"
        )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(source={self.source_name})>"
