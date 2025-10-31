"""
Serviço de análise de PDF de processos jurídicos
"""
from typing import Dict, Any, Optional, BinaryIO
import logging
from datetime import datetime
import re
import hashlib

try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    logging.warning("PyPDF2 não instalado - funcionalidade de PDF limitada")

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

from app.services.openai_service import openai_service
from app.core.config import settings

logger = logging.getLogger(__name__)


class PDFService:
    """Serviço para processamento e análise de PDFs jurídicos"""

    def __init__(self):
        """Inicializa o serviço de PDF"""
        self.max_pages = 100  # Limite de páginas para processar
        self.max_file_size_mb = settings.MAX_UPLOAD_SIZE_MB

    def validate_pdf(self, file: BinaryIO, filename: str) -> Dict[str, Any]:
        """
        Valida arquivo PDF.

        Args:
            file: Arquivo binário
            filename: Nome do arquivo

        Returns:
            Dict com resultado da validação

        Raises:
            ValueError: Se arquivo inválido
        """
        # Verificar extensão
        if not filename.lower().endswith('.pdf'):
            raise ValueError("Arquivo deve ser PDF")

        # Verificar tamanho
        file.seek(0, 2)  # Ir para o final
        size_bytes = file.tell()
        file.seek(0)  # Voltar ao início

        size_mb = size_bytes / (1024 * 1024)

        if size_mb > self.max_file_size_mb:
            raise ValueError(
                f"Arquivo muito grande: {size_mb:.1f}MB "
                f"(máximo: {self.max_file_size_mb}MB)"
            )

        # Calcular hash
        file_hash = hashlib.sha256(file.read()).hexdigest()
        file.seek(0)

        return {
            "valid": True,
            "size_mb": size_mb,
            "size_bytes": size_bytes,
            "hash": file_hash
        }

    def extract_text_from_pdf(
        self,
        file: BinaryIO,
        max_pages: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Extrai texto de PDF.

        Args:
            file: Arquivo PDF
            max_pages: Número máximo de páginas (None = todas)

        Returns:
            Dict com texto extraído e metadados

        Raises:
            Exception: Se houver erro na extração
        """
        if not PDF_AVAILABLE:
            raise Exception("PyPDF2 não está instalado")

        try:
            # Tentar com pdfplumber primeiro (melhor qualidade)
            if PDFPLUMBER_AVAILABLE:
                return self._extract_with_pdfplumber(file, max_pages)
            else:
                return self._extract_with_pypdf2(file, max_pages)

        except Exception as e:
            logger.error(f"Erro ao extrair texto do PDF: {e}")
            raise

    def _extract_with_pypdf2(
        self,
        file: BinaryIO,
        max_pages: Optional[int]
    ) -> Dict[str, Any]:
        """Extrai texto usando PyPDF2"""
        logger.info("Extraindo texto com PyPDF2...")

        reader = PyPDF2.PdfReader(file)
        total_pages = len(reader.pages)

        pages_to_process = min(
            max_pages or self.max_pages,
            total_pages
        )

        text_parts = []
        pages_data = []

        for i in range(pages_to_process):
            try:
                page = reader.pages[i]
                text = page.extract_text()

                if text.strip():
                    text_parts.append(text)
                    pages_data.append({
                        'page_number': i + 1,
                        'text_length': len(text),
                        'has_text': True
                    })
                else:
                    pages_data.append({
                        'page_number': i + 1,
                        'text_length': 0,
                        'has_text': False
                    })

            except Exception as e:
                logger.warning(f"Erro ao extrair página {i+1}: {e}")
                pages_data.append({
                    'page_number': i + 1,
                    'error': str(e)
                })

        full_text = '\n\n'.join(text_parts)

        logger.info(
            f"✅ Texto extraído: {total_pages} páginas, "
            f"{len(full_text)} caracteres"
        )

        return {
            'text': full_text,
            'total_pages': total_pages,
            'pages_processed': pages_to_process,
            'pages_data': pages_data,
            'extraction_method': 'PyPDF2'
        }

    def _extract_with_pdfplumber(
        self,
        file: BinaryIO,
        max_pages: Optional[int]
    ) -> Dict[str, Any]:
        """Extrai texto usando pdfplumber (melhor qualidade)"""
        logger.info("Extraindo texto com pdfplumber...")

        import pdfplumber

        text_parts = []
        pages_data = []

        with pdfplumber.open(file) as pdf:
            total_pages = len(pdf.pages)
            pages_to_process = min(
                max_pages or self.max_pages,
                total_pages
            )

            for i in range(pages_to_process):
                try:
                    page = pdf.pages[i]
                    text = page.extract_text()

                    if text and text.strip():
                        text_parts.append(text)
                        pages_data.append({
                            'page_number': i + 1,
                            'text_length': len(text),
                            'has_text': True
                        })
                    else:
                        pages_data.append({
                            'page_number': i + 1,
                            'text_length': 0,
                            'has_text': False
                        })

                except Exception as e:
                    logger.warning(f"Erro ao extrair página {i+1}: {e}")
                    pages_data.append({
                        'page_number': i + 1,
                        'error': str(e)
                    })

        full_text = '\n\n'.join(text_parts)

        logger.info(
            f"✅ Texto extraído: {total_pages} páginas, "
            f"{len(full_text)} caracteres"
        )

        return {
            'text': full_text,
            'total_pages': total_pages,
            'pages_processed': pages_to_process,
            'pages_data': pages_data,
            'extraction_method': 'pdfplumber'
        }

    def analyze_legal_document(
        self,
        text: str,
        analysis_type: str = "completa"
    ) -> Dict[str, Any]:
        """
        Analisa documento jurídico extraído.

        Args:
            text: Texto do documento
            analysis_type: Tipo de análise

        Returns:
            Dict com análise estruturada
        """
        logger.info(f"Analisando documento jurídico ({analysis_type})...")

        # Extrair informações básicas do texto
        basic_info = self._extract_basic_info(text)

        # Se OpenAI disponível, fazer análise com IA
        if openai_service.is_available():
            try:
                ai_analysis = openai_service.analyze_legal_document(
                    document_text=text,
                    analysis_type=analysis_type
                )
            except Exception as e:
                logger.error(f"Erro na análise com IA: {e}")
                ai_analysis = {"error": str(e)}
        else:
            logger.warning("OpenAI não disponível - análise limitada")
            ai_analysis = {"note": "Análise com IA não disponível"}

        # Combinar análises
        result = {
            **basic_info,
            **ai_analysis,
            'tipo_analise': analysis_type,
            'timestamp': datetime.utcnow().isoformat()
        }

        logger.info("✅ Análise concluída")

        return result

    def _extract_basic_info(self, text: str) -> Dict[str, Any]:
        """
        Extrai informações básicas do texto sem IA.

        Args:
            text: Texto do documento

        Returns:
            Dict com informações extraídas
        """
        info = {
            'caracteres': len(text),
            'palavras': len(text.split()),
            'linhas': len(text.split('\n'))
        }

        # Extrair número de processo (padrão CNJ)
        processo_match = re.search(
            r'\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}',
            text
        )
        if processo_match:
            info['numero_processo'] = processo_match.group(0)

        # Identificar partes (padrão comum)
        autor_match = re.search(
            r'(?:AUTOR|REQUERENTE|EXEQUENTE):\s*([A-ZÀÁÂÃÉÊÍÓÔÕÚÇ\s]+)',
            text,
            re.IGNORECASE
        )
        if autor_match:
            info['autor'] = autor_match.group(1).strip()

        reu_match = re.search(
            r'(?:RÉU|REQUERIDO|EXECUTADO):\s*([A-ZÀÁÂÃÉÊÍÓÔÕÚÇ\s]+)',
            text,
            re.IGNORECASE
        )
        if reu_match:
            info['reu'] = reu_match.group(1).strip()

        # Identificar tribunal/vara
        tribunal_match = re.search(
            r'(TRIBUNAL|VARA|JUÍZO)\s+([A-Z\s]+)',
            text,
            re.IGNORECASE
        )
        if tribunal_match:
            info['tribunal'] = tribunal_match.group(0).strip()

        # Palavras-chave jurídicas
        legal_keywords = [
            'sentença', 'decisão', 'acórdão', 'recurso', 'apelação',
            'agravo', 'mandado', 'liminar', 'tutela', 'embargos',
            'execução', 'petição', 'contestação', 'réplica'
        ]

        text_lower = text.lower()
        found_keywords = [kw for kw in legal_keywords if kw in text_lower]
        info['palavras_chave_identificadas'] = found_keywords[:10]

        return info

    def process_and_analyze(
        self,
        file: BinaryIO,
        filename: str,
        analysis_type: str = "completa"
    ) -> Dict[str, Any]:
        """
        Processa PDF completo (validação + extração + análise).

        Args:
            file: Arquivo PDF
            filename: Nome do arquivo
            analysis_type: Tipo de análise

        Returns:
            Dict com resultado completo
        """
        start_time = datetime.utcnow()

        logger.info(f"Processando PDF: {filename}")

        # 1. Validar
        validation = self.validate_pdf(file, filename)
        logger.info(f"✅ Validação: {validation['size_mb']:.1f}MB")

        # 2. Extrair texto
        extraction = self.extract_text_from_pdf(file)
        logger.info(
            f"✅ Extração: {extraction['pages_processed']} páginas, "
            f"{len(extraction['text'])} caracteres"
        )

        # 3. Analisar
        analysis = self.analyze_legal_document(
            text=extraction['text'],
            analysis_type=analysis_type
        )
        logger.info("✅ Análise concluída")

        # Tempo total
        end_time = datetime.utcnow()
        processing_time = (end_time - start_time).total_seconds()

        return {
            'filename': filename,
            'validation': validation,
            'extraction': {
                'total_pages': extraction['total_pages'],
                'pages_processed': extraction['pages_processed'],
                'method': extraction['extraction_method'],
                'text_length': len(extraction['text'])
            },
            'analysis': analysis,
            'processing_time_seconds': processing_time,
            'timestamp': end_time.isoformat()
        }


# Instância global
pdf_service = PDFService()
