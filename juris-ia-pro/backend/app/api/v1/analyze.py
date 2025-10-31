"""
Router para endpoints de análise de processos e documentos
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import Optional
import logging

from app.models.schemas import ProcessoAnaliseResponse
from app.services.pdf_service import pdf_service, PDF_AVAILABLE
from app.core.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/pdf", response_model=dict)
async def analyze_pdf(
    file: UploadFile = File(...),
    analysis_type: str = Form(default="completa")
):
    """
    Analisa um PDF de processo jurídico.

    Args:
        file: Arquivo PDF do processo
        analysis_type: Tipo de análise (completa, sumaria, especifica)

    Returns:
        Análise estruturada do processo

    Raises:
        HTTPException: Se houver erro no processamento
    """
    if not settings.ENABLE_PDF_ANALYSIS:
        raise HTTPException(
            status_code=503,
            detail="Análise de PDF não está habilitada"
        )

    if not PDF_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Biblioteca de PDF não está instalada. Execute: pip install PyPDF2 pdfplumber"
        )

    # Validar tipo de arquivo
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Apenas arquivos PDF são aceitos"
        )

    logger.info(f"Recebendo arquivo para análise: {file.filename}")

    try:
        # Ler conteúdo do arquivo
        contents = await file.read()

        # Criar file-like object
        from io import BytesIO
        pdf_file = BytesIO(contents)

        # Processar PDF
        result = pdf_service.process_and_analyze(
            file=pdf_file,
            filename=file.filename,
            analysis_type=analysis_type
        )

        logger.info(
            f"✅ Análise concluída: {file.filename} "
            f"({result['processing_time_seconds']:.1f}s)"
        )

        return {
            "success": True,
            "message": "Análise concluída com sucesso",
            **result
        }

    except ValueError as e:
        logger.warning(f"Erro de validação: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(f"Erro ao analisar PDF: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar PDF: {str(e)}"
        )


@router.get("/pdf/check")
async def check_pdf_support():
    """
    Verifica se análise de PDF está disponível.

    Returns:
        Status do suporte a PDF
    """
    return {
        "enabled": settings.ENABLE_PDF_ANALYSIS,
        "pdf_library_available": PDF_AVAILABLE,
        "max_file_size_mb": settings.MAX_UPLOAD_SIZE_MB,
        "allowed_extensions": settings.ALLOWED_EXTENSIONS,
        "status": "available" if (settings.ENABLE_PDF_ANALYSIS and PDF_AVAILABLE) else "unavailable"
    }


@router.post("/text")
async def analyze_text(
    text: str = Form(...),
    analysis_type: str = Form(default="completa")
):
    """
    Analisa texto de documento jurídico.

    Args:
        text: Texto do documento
        analysis_type: Tipo de análise

    Returns:
        Análise estruturada
    """
    if not text or len(text.strip()) < 100:
        raise HTTPException(
            status_code=400,
            detail="Texto muito curto (mínimo 100 caracteres)"
        )

    logger.info(f"Analisando texto ({len(text)} caracteres)")

    try:
        analysis = pdf_service.analyze_legal_document(
            text=text,
            analysis_type=analysis_type
        )

        return {
            "success": True,
            "message": "Análise concluída",
            "analysis": analysis
        }

    except Exception as e:
        logger.error(f"Erro ao analisar texto: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro na análise: {str(e)}"
        )
