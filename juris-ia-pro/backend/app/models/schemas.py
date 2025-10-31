"""
Schemas Pydantic para validação de request/response
"""
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from enum import Enum


# ============================================
# ENUMS
# ============================================

class TipoUsuario(str, Enum):
    ADMIN = "admin"
    ADVOGADO = "advogado"
    ASSINANTE = "assinante"
    VISITANTE = "visitante"


class TipoDocumento(str, Enum):
    LEI = "lei"
    SUMULA = "sumula"
    ACORDAO = "acordao"
    DECISAO = "decisao"
    PARECER = "parecer"
    DOUTRINA = "doutrina"
    OUTRO = "outro"


class InstanciaJudicial(str, Enum):
    STF = "STF"
    STJ = "STJ"
    TST = "TST"
    TSE = "TSE"
    STM = "STM"
    TRF = "TRF"
    TJ = "TJ"
    TRT = "TRT"
    TRE = "TRE"
    OUTRA = "OUTRA"


class StatusValidacao(str, Enum):
    PENDENTE = "pendente"
    APROVADO = "aprovado"
    REJEITADO = "rejeitado"
    EM_REVISAO = "em_revisao"


# ============================================
# SCHEMAS - USUARIO
# ============================================

class UsuarioBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=255)
    email: EmailStr


class UsuarioCreate(UsuarioBase):
    senha: str = Field(..., min_length=8)
    oab_numero: Optional[str] = None
    oab_estado: Optional[str] = Field(None, max_length=2)
    cpf: Optional[str] = None

    @field_validator('oab_estado')
    @classmethod
    def validate_oab_estado(cls, v):
        if v is not None:
            return v.upper()
        return v


class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    oab_numero: Optional[str] = None
    oab_estado: Optional[str] = None
    preferencias: Optional[Dict[str, Any]] = None


class UsuarioResponse(UsuarioBase):
    id: str
    tipo_conta: TipoUsuario
    ativo: bool
    email_verificado: bool
    oab_numero: Optional[str] = None
    oab_estado: Optional[str] = None
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================
# SCHEMAS - AUTH
# ============================================

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str  # user_id
    exp: datetime
    iat: datetime


class LoginRequest(BaseModel):
    email: EmailStr
    senha: str


# ============================================
# SCHEMAS - DOCUMENTO JURIDICO
# ============================================

class DocumentoJuridicoBase(BaseModel):
    titulo: str = Field(..., min_length=5, max_length=1000)
    tipo_documento: TipoDocumento
    conteudo_completo: str = Field(..., min_length=10)
    ementa: Optional[str] = None
    orgao_emissor: Optional[str] = None
    instancia: Optional[InstanciaJudicial] = None


class DocumentoJuridicoCreate(DocumentoJuridicoBase):
    numero_processo: Optional[str] = None
    decisao: Optional[str] = None
    relator: Optional[str] = None
    data_publicacao: Optional[date] = None
    data_julgamento: Optional[date] = None
    area_direito: Optional[str] = None
    palavras_chave: Optional[List[str]] = []
    assuntos: Optional[List[str]] = []
    fonte_original: Optional[str] = None
    url_fonte: Optional[str] = None


class DocumentoJuridicoResponse(DocumentoJuridicoBase):
    id: str
    numero_processo: Optional[str] = None
    relator: Optional[str] = None
    data_publicacao: Optional[date] = None
    relevancia_score: float
    citacoes_count: int
    palavras_chave: List[str] = []
    assuntos: List[str] = []
    indexed_at: datetime

    class Config:
        from_attributes = True


class DocumentoJuridicoDetail(DocumentoJuridicoResponse):
    """Documento com todos os detalhes"""
    decisao: Optional[str] = None
    sumario: Optional[str] = None
    data_julgamento: Optional[date] = None
    metadados: Dict[str, Any] = {}
    url_fonte: Optional[str] = None


# ============================================
# SCHEMAS - BUSCA
# ============================================

class SearchRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=500)
    filters: Optional[Dict[str, Any]] = Field(default_factory=dict)
    limit: int = Field(default=10, ge=1, le=50)
    offset: int = Field(default=0, ge=0)

    # Filtros específicos
    tipo_documento: Optional[TipoDocumento] = None
    instancia: Optional[InstanciaJudicial] = None
    data_inicio: Optional[date] = None
    data_fim: Optional[date] = None
    area_direito: Optional[str] = None


class SearchResult(BaseModel):
    id: str
    titulo: str
    tipo_documento: TipoDocumento
    ementa: Optional[str] = None
    orgao_emissor: Optional[str] = None
    data_publicacao: Optional[date] = None
    relevancia_score: float
    similarity_score: Optional[float] = None
    citacoes_count: int
    highlight: Optional[str] = None  # Trecho relevante


class SearchResponse(BaseModel):
    query: str
    total: int
    results: List[SearchResult]
    time_ms: int
    filters_applied: Dict[str, Any] = {}


# ============================================
# SCHEMAS - CHAT
# ============================================

class ChatMessage(BaseModel):
    message: str = Field(..., min_length=3, max_length=2000)
    conversation_id: Optional[str] = None
    context: Optional[List[str]] = None  # IDs de documentos para contexto


class SourceReference(BaseModel):
    documento_id: str
    titulo: str
    orgao: Optional[str] = None
    data: Optional[date] = None
    trecho_relevante: Optional[str] = None
    confianca: float = Field(..., ge=0.0, le=1.0)


class ChatResponse(BaseModel):
    response: str
    sources: List[SourceReference]
    confidence: float = Field(..., ge=0.0, le=1.0)
    conversation_id: str
    processing_time_ms: int


# ============================================
# SCHEMAS - ANÁLISE DE PROCESSO
# ============================================

class ProcessoAnaliseRequest(BaseModel):
    numero_processo: Optional[str] = None
    tipo_analise: str = Field(default="completa")
    opcoes: Optional[Dict[str, Any]] = Field(default_factory=dict)


class ProcessoAnaliseResponse(BaseModel):
    id: str
    numero_processo: Optional[str] = None
    tese_principal: Optional[str] = None
    analise_completa: Dict[str, Any]
    documentos_relacionados: List[str] = []
    fundamentacao_legal: Optional[str] = None
    sugestoes: Dict[str, Any] = {}
    confianca_analise: float
    tempo_processamento_segundos: int
    created_at: datetime


# ============================================
# SCHEMAS - DOCUMENTO GERADO
# ============================================

class DocumentoGeradoRequest(BaseModel):
    tipo_documento: str = Field(..., min_length=3, max_length=100)
    titulo: str = Field(..., min_length=5, max_length=500)
    parametros: Dict[str, Any] = Field(..., min_examples=1)
    template_id: Optional[str] = None


class DocumentoGeradoResponse(BaseModel):
    id: str
    tipo_documento: str
    titulo: str
    conteudo: str
    fontes_citadas: List[Dict[str, Any]] = []
    status_validacao: StatusValidacao
    created_at: datetime
    versao: int

    class Config:
        from_attributes = True


# ============================================
# SCHEMAS - ALERTAS
# ============================================

class AlertaCreate(BaseModel):
    nome_alerta: str = Field(..., min_length=3, max_length=255)
    palavras_chave: List[str] = Field(..., min_length=1)
    filtros_tribunais: Optional[List[InstanciaJudicial]] = None
    areas_interesse: Optional[List[str]] = None
    frequencia_dias: int = Field(default=7, ge=1, le=30)


class AlertaResponse(BaseModel):
    id: str
    nome_alerta: str
    palavras_chave: List[str]
    filtros_tribunais: List[InstanciaJudicial]
    ativo: bool
    ultimo_envio: Optional[datetime] = None
    proximo_envio: Optional[datetime] = None
    total_notificacoes_enviadas: int
    created_at: datetime

    class Config:
        from_attributes = True


# ============================================
# SCHEMAS - ESTATÍSTICAS
# ============================================

class EstatisticasSistema(BaseModel):
    total_documentos: int
    total_usuarios: int
    total_consultas_hoje: int
    total_documentos_gerados: int
    tribunais_ativos: List[str]
    ultima_atualizacao: datetime


class EstatisticasUsuario(BaseModel):
    total_consultas: int
    total_documentos_gerados: int
    ultima_consulta: Optional[datetime] = None
    areas_mais_buscadas: List[str] = []


# ============================================
# SCHEMAS - HEALTH CHECK
# ============================================

class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: datetime
    database: str
    redis: str
    qdrant: str
    openai: str


# ============================================
# SCHEMAS - ERROR
# ============================================

class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
