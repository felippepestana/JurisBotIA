"""
Scraper para legislação do Planalto
Coleta leis federais, decretos, medidas provisórias, etc.
"""
from typing import List, Dict, Any, Optional
import logging
import re
from datetime import datetime

from app.scrapers.base_scraper import BaseScraper

logger = logging.getLogger(__name__)


class PlanaltoScraper(BaseScraper):
    """Scraper para legislação do Planalto"""

    def __init__(self):
        super().__init__(
            source_name="Planalto",
            base_url="https://www.planalto.gov.br"
        )

        # URLs principais
        self.leis_url = f"{self.base_url}/ccivil_03/leis/"
        self.decretos_url = f"{self.base_url}/ccivil_03/_ato2023-2026/2024/decreto/"

        # Leis importantes para começar
        self.important_laws = [
            ("L8078.htm", "Lei 8.078/1990", "Código de Defesa do Consumidor"),
            ("L5869.htm", "Lei 5.869/1973", "Código de Processo Civil"),
            ("L10406.htm", "Lei 10.406/2002", "Código Civil"),
            ("L13105.htm", "Lei 13.105/2015", "Novo Código de Processo Civil"),
            ("L8069.htm", "Lei 8.069/1990", "Estatuto da Criança e do Adolescente"),
            ("L9099.htm", "Lei 9.099/1995", "Juizados Especiais"),
            ("L4737.htm", "Lei 4.737/1965", "Código Eleitoral"),
        ]

    def scrape(
        self,
        scrape_mode: str = "important",
        start_year: Optional[int] = None,
        end_year: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Scrape legislação do Planalto.

        Args:
            scrape_mode: "important" para leis importantes, "year_range" para intervalo
            start_year: Ano inicial (para mode="year_range")
            end_year: Ano final (para mode="year_range")

        Returns:
            Lista de documentos legislativos
        """
        logger.info(f"Iniciando scraping Planalto - Modo: {scrape_mode}")

        if scrape_mode == "important":
            self._scrape_important_laws()
        elif scrape_mode == "year_range":
            if not start_year or not end_year:
                raise ValueError("start_year e end_year são obrigatórios para mode='year_range'")
            self._scrape_by_year_range(start_year, end_year)
        else:
            raise ValueError(f"Modo inválido: {scrape_mode}")

        logger.info(f"✅ Scraping concluído: {len(self.documents_scraped)} documentos")
        return self.documents_scraped

    def _scrape_important_laws(self) -> None:
        """Scrape leis importantes pré-definidas"""
        logger.info("Scraping leis importantes...")

        for i, (file_name, lei_numero, descricao) in enumerate(self.important_laws, 1):
            try:
                self.log_progress(i, len(self.important_laws), "leis")

                url = f"{self.leis_url}{file_name}"
                html = self.fetch_page(url)

                if html:
                    document = self._parse_law_page(html, lei_numero, descricao)
                    if document:
                        document['url_fonte'] = url
                        self.save_document(document)

                self.rate_limit(0.5)

            except Exception as e:
                logger.error(f"Erro ao scrapear {lei_numero}: {e}")
                continue

    def _scrape_by_year_range(self, start_year: int, end_year: int) -> None:
        """
        Scrape leis por intervalo de anos.

        Args:
            start_year: Ano inicial
            end_year: Ano final
        """
        logger.info(f"Scraping leis de {start_year} a {end_year}...")

        # TODO: Implementar lógica de descoberta de leis por ano
        # Isso requer análise mais profunda da estrutura do site
        logger.warning("Scraping por ano ainda não implementado - use mode='important'")

    def _parse_law_page(
        self,
        html: str,
        lei_numero: str,
        descricao: str
    ) -> Optional[Dict[str, Any]]:
        """
        Parse página de uma lei.

        Args:
            html: HTML da página
            lei_numero: Número da lei
            descricao: Descrição da lei

        Returns:
            Dicionário com dados da lei ou None
        """
        try:
            soup = self.parse_html(html)

            # Extrair conteúdo principal
            # O Planalto usa estrutura específica
            content_div = soup.find('div', class_='textoLei') or soup.find('body')

            if not content_div:
                logger.warning(f"Não foi possível encontrar conteúdo para {lei_numero}")
                return None

            # Extrair texto completo
            full_text = self.extract_text(content_div)

            if len(full_text) < 100:
                logger.warning(f"Texto muito curto para {lei_numero}")
                return None

            # Extrair ementa (geralmente no início)
            ementa = self._extract_ementa(full_text)

            # Extrair data de publicação
            data_pub = self._extract_publication_date(html, soup)

            # Extrair artigos principais (primeiros 3)
            artigos = self._extract_main_articles(soup)

            # Identificar palavras-chave
            palavras_chave = self._extract_keywords(descricao, full_text)

            # Montar documento
            document = {
                'titulo': f"{lei_numero} - {descricao}",
                'tipo_documento': 'lei',
                'numero_processo': lei_numero,
                'conteudo_completo': full_text[:10000],  # Limitar para não ficar muito grande
                'ementa': ementa,
                'orgao_emissor': 'Presidência da República',
                'instancia': 'OUTRA',
                'data_publicacao': data_pub,
                'palavras_chave': palavras_chave,
                'assuntos': [self._categorize_law(descricao)],
                'metadados': {
                    'artigos_principais': artigos,
                    'tipo_legislacao': 'lei_federal',
                    'origem': 'planalto'
                },
                'relevancia_score': 0.9,  # Leis são sempre relevantes
                'citacoes_count': 0,  # Será atualizado depois
                'fonte_original': 'Planalto - Presidência da República'
            }

            return document

        except Exception as e:
            logger.error(f"Erro ao parsear lei {lei_numero}: {e}")
            return None

    def _extract_ementa(self, text: str) -> str:
        """
        Extrai ementa da lei (primeiras linhas).

        Args:
            text: Texto completo

        Returns:
            Ementa extraída
        """
        # Ementa geralmente está nas primeiras linhas
        lines = text.split('\n')
        ementa_lines = []

        for line in lines[:10]:
            line = line.strip()
            if line and len(line) > 20:
                ementa_lines.append(line)
                if len(' '.join(ementa_lines)) > 200:
                    break

        return ' '.join(ementa_lines)[:500]

    def _extract_publication_date(
        self,
        html: str,
        soup: BeautifulSoup
    ) -> Optional[datetime]:
        """
        Extrai data de publicação.

        Args:
            html: HTML bruto
            soup: Objeto BeautifulSoup

        Returns:
            Data de publicação ou None
        """
        # Procurar padrões de data no HTML
        date_patterns = [
            r'(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})',
            r'(\d{2})/(\d{2})/(\d{4})',
        ]

        months = {
            'janeiro': 1, 'fevereiro': 2, 'março': 3, 'abril': 4,
            'maio': 5, 'junho': 6, 'julho': 7, 'agosto': 8,
            'setembro': 9, 'outubro': 10, 'novembro': 11, 'dezembro': 12
        }

        for pattern in date_patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                try:
                    if len(match.groups()) == 3:
                        day, month, year = match.groups()

                        # Se mês é nome
                        if month.lower() in months:
                            month = months[month.lower()]

                        return datetime(int(year), int(month), int(day))
                except:
                    continue

        return None

    def _extract_main_articles(self, soup: BeautifulSoup) -> List[str]:
        """
        Extrai artigos principais da lei.

        Args:
            soup: Objeto BeautifulSoup

        Returns:
            Lista com artigos principais
        """
        articles = []

        # Procurar por tags de artigo (estrutura varia)
        article_tags = soup.find_all('p', limit=10)

        for tag in article_tags:
            text = self.extract_text(tag)
            # Identificar se é um artigo (começa com "Art." ou "Artigo")
            if re.match(r'Art[º°\.]?\s*\d+', text, re.IGNORECASE):
                articles.append(text[:200])

            if len(articles) >= 3:
                break

        return articles

    def _extract_keywords(self, descricao: str, text: str) -> List[str]:
        """
        Extrai palavras-chave relevantes.

        Args:
            descricao: Descrição da lei
            text: Texto completo

        Returns:
            Lista de palavras-chave
        """
        keywords = set()

        # Palavras da descrição
        desc_words = descricao.lower().split()
        keywords.update([w for w in desc_words if len(w) > 4])

        # Termos jurídicos comuns
        legal_terms = [
            'consumidor', 'civil', 'processo', 'direito', 'código',
            'federal', 'constituição', 'lei', 'decreto', 'artigo'
        ]

        text_lower = text.lower()
        for term in legal_terms:
            if term in text_lower:
                keywords.add(term)

        return list(keywords)[:10]

    def _categorize_law(self, descricao: str) -> str:
        """
        Categoriza a lei por área do direito.

        Args:
            descricao: Descrição da lei

        Returns:
            Categoria/área do direito
        """
        categories = {
            'consumidor': 'Direito do Consumidor',
            'processo civil': 'Direito Processual Civil',
            'civil': 'Direito Civil',
            'penal': 'Direito Penal',
            'trabalhista': 'Direito do Trabalho',
            'tributário': 'Direito Tributário',
            'administrativo': 'Direito Administrativo',
            'constitucional': 'Direito Constitucional',
            'eleitoral': 'Direito Eleitoral',
            'criança': 'Direito da Criança e Adolescente',
        }

        desc_lower = descricao.lower()
        for key, category in categories.items():
            if key in desc_lower:
                return category

        return 'Direito Geral'


# Exemplo de uso
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    scraper = PlanaltoScraper()
    documents = scraper.scrape(scrape_mode="important")

    print(f"\n📊 Total de documentos: {len(documents)}")
    for doc in documents[:3]:
        print(f"\n✅ {doc['titulo']}")
        print(f"   Ementa: {doc['ementa'][:100]}...")
