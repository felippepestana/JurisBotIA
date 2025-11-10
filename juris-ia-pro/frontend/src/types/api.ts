/**
 * Tipos para integração com a API do JurisIA Pro
 */

// ============================================
// DOCUMENTOS JURÍDICOS
// ============================================

export type TipoDocumento = 'lei' | 'sumula' | 'acordao' | 'decreto' | 'outro'
export type Instancia = 'STF' | 'STJ' | 'TST' | 'TJSP' | 'TJRJ' | 'TRF' | 'FEDERAL' | 'OUTRA'

export interface DocumentoJuridico {
  id: string
  titulo: string
  tipo_documento: TipoDocumento
  numero_processo?: string
  ementa?: string
  conteudo_completo: string
  orgao_emissor?: string
  instancia: Instancia
  data_publicacao?: string
  palavras_chave: string[]
  assuntos: string[]
  relevancia_score: number
  similarity_score?: number
  citacoes_count: number
  highlight?: string
  fonte_original?: string
  url_fonte?: string
}

// ============================================
// BUSCA
// ============================================

export interface SearchRequest {
  query: string
  limit?: number
  tipo_documento?: TipoDocumento
  instancia?: Instancia
  data_inicio?: string
  data_fim?: string
}

export interface SearchResult {
  id: string
  titulo: string
  tipo_documento: TipoDocumento
  ementa?: string
  orgao_emissor?: string
  data_publicacao?: string
  relevancia_score: number
  similarity_score: number
  citacoes_count: number
  highlight?: string
}

export interface SearchResponse {
  query: string
  total: number
  results: SearchResult[]
  time_ms: number
  filters_applied: Record<string, any>
}

export interface KeywordSuggestion {
  query: string
  suggestions: string[]
}

// ============================================
// CHAT
// ============================================

export interface ChatMessage {
  message: string
  conversation_id?: string
}

export interface SourceReference {
  documento_id: string
  titulo: string
  orgao?: string
  data?: string
  trecho_relevante?: string
  confianca: number
}

export interface ChatResponse {
  response: string
  sources: SourceReference[]
  confidence: number
  conversation_id: string
  processing_time_ms: number
}

export interface ChatHistory {
  conversation_id: string
  messages: Array<{
    role: 'user' | 'assistant'
    content: string
    timestamp: string
  }>
  created_at: string
}

// ============================================
// ANÁLISE DE PDF
// ============================================

export type TipoAnalise = 'rapida' | 'completa' | 'identificacao' | 'riscos'

export interface PDFAnalysisRequest {
  file: File
  analysis_type: TipoAnalise
  focus_areas?: string[]
}

export interface LegalFrameworkItem {
  documento: string
  aplicabilidade: 'Alta' | 'Média' | 'Baixa'
  fundamento: string
  artigos?: string[]
}

export interface PDFAnalysisResponse {
  status: 'success' | 'error'
  filename: string
  extracted_text: string
  metadata: {
    pages: number
    file_size: string
    extraction_method: string
  }
  analysis: {
    document_type: string
    legal_area: string
    parties: string[]
    key_issues: string[]
    applicable_framework: LegalFrameworkItem[]
    recommendations: string[]
    similar_cases?: any[]
    confidence_score: number
  }
  time_ms: number
}

// ============================================
// GERAÇÃO DE DOCUMENTOS
// ============================================

export type TipoDocumentoGerado = 'inicial' | 'contestacao' | 'recurso' | 'memoriais' | 'contrato' | 'parecer'

export interface DocumentGenerationRequest {
  document_type: TipoDocumentoGerado
  parameters: Record<string, any>
  template?: string
}

export interface DocumentGenerationResponse {
  document_type: TipoDocumentoGerado
  content: string
  metadata: {
    generated_at: string
    template_used?: string
    word_count: number
  }
  suggestions: string[]
  time_ms: number
}

export interface DocumentTemplate {
  id: string
  name: string
  document_type: TipoDocumentoGerado
  description: string
  required_fields: string[]
  optional_fields: string[]
}

// ============================================
// ESTATÍSTICAS
// ============================================

export interface ServiceStatus {
  available: boolean
  status: 'online' | 'offline' | 'degraded'
}

export interface SystemStats {
  timestamp: string
  system: {
    version: string
    status: string
    uptime_check_ms: number
  }
  services: {
    redis: ServiceStatus
    qdrant: ServiceStatus
    openai: ServiceStatus
  }
  cache?: {
    total_keys: number
    used_memory_human: string
    hit_rate?: number
  }
  vector_database?: {
    collection_name: string
    documents_indexed: number
    vector_dimension: number
  }
  configuration: {
    environment: string
    cache_ttl_seconds: number
    rag_similarity_threshold: number
  }
}

export interface PerformanceMetrics {
  timestamp: string
  current_metrics: {
    cache_roundtrip_ms: number | null
    vector_search_ms: number | null
  }
  target_benchmarks: {
    cache_hit_target_ms: number
    cache_miss_target_ms: number
    chat_response_target_ms: number
    pdf_analysis_target_ms: number
  }
  status: string
}

// ============================================
// HEALTH CHECK
// ============================================

export interface HealthResponse {
  status: 'healthy' | 'degraded' | 'unhealthy'
  version: string
  timestamp: string
  database?: string
  redis?: string
  qdrant?: string
  openai?: string
}

// ============================================
// ERROS
// ============================================

export interface APIError {
  detail: string
  error_code?: string
  status_code: number
}

// ============================================
// UTILITÁRIOS
// ============================================

export interface PaginationParams {
  page: number
  limit: number
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  limit: number
  pages: number
}
