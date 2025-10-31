-- ============================================
-- JURISIA PRO - DATABASE SCHEMA
-- PostgreSQL 15+ com pgvector
-- ============================================

-- Habilitar extensões necessárias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "vector";

-- ============================================
-- ENUMS
-- ============================================

CREATE TYPE tipo_usuario AS ENUM ('admin', 'advogado', 'assinante', 'visitante');
CREATE TYPE tipo_documento AS ENUM ('lei', 'sumula', 'acordao', 'decisao', 'parecer', 'doutrina', 'outro');
CREATE TYPE instancia_judicial AS ENUM ('STF', 'STJ', 'TST', 'TSE', 'STM', 'TRF', 'TJ', 'TRT', 'TRE', 'OUTRA');
CREATE TYPE status_validacao AS ENUM ('pendente', 'aprovado', 'rejeitado', 'em_revisao');
CREATE TYPE tipo_citacao AS ENUM ('principal', 'secundaria', 'contraria', 'complementar');
CREATE TYPE status_processo AS ENUM ('ativo', 'arquivado', 'concluido');

-- ============================================
-- TABELA: usuarios
-- ============================================

CREATE TABLE usuarios (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,

    -- Dados profissionais
    oab_numero VARCHAR(20),
    oab_estado VARCHAR(2),
    cpf VARCHAR(14) UNIQUE,

    -- Tipo e permissões
    tipo_conta tipo_usuario DEFAULT 'visitante',
    ativo BOOLEAN DEFAULT true,
    email_verificado BOOLEAN DEFAULT false,

    -- Preferências
    preferencias JSONB DEFAULT '{}',

    -- Auditoria
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE,
    login_count INTEGER DEFAULT 0,

    -- Índices
    CONSTRAINT email_valido CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_usuarios_oab ON usuarios(oab_numero, oab_estado) WHERE oab_numero IS NOT NULL;
CREATE INDEX idx_usuarios_tipo ON usuarios(tipo_conta);
CREATE INDEX idx_usuarios_ativo ON usuarios(ativo);

-- ============================================
-- TABELA: documentos_juridicos
-- ============================================

CREATE TABLE documentos_juridicos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    -- Identificação
    titulo TEXT NOT NULL,
    tipo_documento tipo_documento NOT NULL,
    numero_processo VARCHAR(100),

    -- Conteúdo
    conteudo_completo TEXT NOT NULL,
    ementa TEXT,
    decisao TEXT,
    sumario TEXT,

    -- Origem
    orgao_emissor VARCHAR(255),
    instancia instancia_judicial,
    relator VARCHAR(255),

    -- Datas
    data_publicacao DATE,
    data_julgamento DATE,

    -- Classificação
    area_direito VARCHAR(100),
    palavras_chave TEXT[],
    assuntos TEXT[],

    -- Metadados
    metadados JSONB DEFAULT '{}',
    fonte_original TEXT,
    url_fonte TEXT,

    -- Relevância
    relevancia_score FLOAT DEFAULT 0.0,
    citacoes_count INTEGER DEFAULT 0,
    visualizacoes INTEGER DEFAULT 0,

    -- Status
    ativo BOOLEAN DEFAULT true,
    revisado BOOLEAN DEFAULT false,

    -- Auditoria
    indexed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    -- Full-text search
    search_vector tsvector GENERATED ALWAYS AS (
        setweight(to_tsvector('portuguese', coalesce(titulo, '')), 'A') ||
        setweight(to_tsvector('portuguese', coalesce(ementa, '')), 'B') ||
        setweight(to_tsvector('portuguese', coalesce(conteudo_completo, '')), 'C')
    ) STORED
);

-- Índices para performance
CREATE INDEX idx_docs_tipo ON documentos_juridicos(tipo_documento);
CREATE INDEX idx_docs_instancia ON documentos_juridicos(instancia);
CREATE INDEX idx_docs_data_pub ON documentos_juridicos(data_publicacao DESC);
CREATE INDEX idx_docs_relevancia ON documentos_juridicos(relevancia_score DESC);
CREATE INDEX idx_docs_palavras_chave ON documentos_juridicos USING GIN(palavras_chave);
CREATE INDEX idx_docs_assuntos ON documentos_juridicos USING GIN(assuntos);
CREATE INDEX idx_docs_search_vector ON documentos_juridicos USING GIN(search_vector);
CREATE INDEX idx_docs_metadados ON documentos_juridicos USING GIN(metadados);
CREATE INDEX idx_docs_numero_processo ON documentos_juridicos(numero_processo) WHERE numero_processo IS NOT NULL;

-- ============================================
-- TABELA: embeddings
-- ============================================

CREATE TABLE embeddings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    documento_id UUID NOT NULL REFERENCES documentos_juridicos(id) ON DELETE CASCADE,

    -- Vector embedding (3072 dimensões para text-embedding-3-large)
    embedding vector(3072) NOT NULL,

    -- Chunk info
    chunk_text TEXT NOT NULL,
    chunk_position INTEGER NOT NULL,
    chunk_metadata JSONB DEFAULT '{}',

    -- Modelo usado
    model_name VARCHAR(100) DEFAULT 'text-embedding-3-large',
    model_version VARCHAR(50),

    -- Auditoria
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    -- Constraint
    UNIQUE(documento_id, chunk_position)
);

-- Índice vetorial para busca de similaridade (HNSW é mais rápido para high-dimensional vectors)
CREATE INDEX idx_embeddings_vector ON embeddings USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
CREATE INDEX idx_embeddings_documento ON embeddings(documento_id);

-- ============================================
-- TABELA: citacoes
-- ============================================

CREATE TABLE citacoes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    -- Relação entre documentos
    documento_origem_id UUID NOT NULL REFERENCES documentos_juridicos(id) ON DELETE CASCADE,
    documento_citado_id UUID NOT NULL REFERENCES documentos_juridicos(id) ON DELETE CASCADE,

    -- Tipo e contexto
    tipo_citacao tipo_citacao DEFAULT 'principal',
    contexto_citacao TEXT,
    posicao_texto INTEGER,

    -- Validação
    confiabilidade FLOAT DEFAULT 1.0,
    verificado BOOLEAN DEFAULT false,

    -- Auditoria
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    -- Constraints
    CONSTRAINT diferentes_documentos CHECK (documento_origem_id != documento_citado_id),
    CONSTRAINT citacao_unica UNIQUE(documento_origem_id, documento_citado_id, posicao_texto)
);

CREATE INDEX idx_citacoes_origem ON citacoes(documento_origem_id);
CREATE INDEX idx_citacoes_citado ON citacoes(documento_citado_id);
CREATE INDEX idx_citacoes_tipo ON citacoes(tipo_citacao);

-- ============================================
-- TABELA: consultas_usuarios
-- ============================================

CREATE TABLE consultas_usuarios (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    usuario_id UUID REFERENCES usuarios(id) ON DELETE SET NULL,

    -- Query
    query_original TEXT NOT NULL,
    query_processada TEXT,
    parametros_busca JSONB DEFAULT '{}',

    -- Resultados
    resultados JSONB,
    num_resultados INTEGER DEFAULT 0,

    -- Métricas
    tempo_resposta_ms INTEGER,
    modelo_usado VARCHAR(100),

    -- Feedback
    feedback_positivo BOOLEAN,
    comentario_feedback TEXT,

    -- Auditoria
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ip_address INET,
    user_agent TEXT
);

CREATE INDEX idx_consultas_usuario ON consultas_usuarios(usuario_id);
CREATE INDEX idx_consultas_data ON consultas_usuarios(created_at DESC);
CREATE INDEX idx_consultas_feedback ON consultas_usuarios(feedback_positivo) WHERE feedback_positivo IS NOT NULL;

-- ============================================
-- TABELA: documentos_gerados
-- ============================================

CREATE TABLE documentos_gerados (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    usuario_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,

    -- Tipo de documento
    tipo_documento VARCHAR(100) NOT NULL,
    titulo VARCHAR(500) NOT NULL,

    -- Conteúdo
    conteudo TEXT NOT NULL,
    template_usado VARCHAR(100),
    parametros_geracao JSONB DEFAULT '{}',

    -- Fontes citadas
    fontes_citadas JSONB DEFAULT '[]',
    documentos_base UUID[],

    -- Validação
    status_validacao status_validacao DEFAULT 'pendente',
    validador_id UUID REFERENCES usuarios(id),
    observacoes_validacao TEXT,

    -- Auditoria
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    versao INTEGER DEFAULT 1
);

CREATE INDEX idx_docs_gerados_usuario ON documentos_gerados(usuario_id);
CREATE INDEX idx_docs_gerados_tipo ON documentos_gerados(tipo_documento);
CREATE INDEX idx_docs_gerados_status ON documentos_gerados(status_validacao);
CREATE INDEX idx_docs_gerados_data ON documentos_gerados(created_at DESC);

-- ============================================
-- TABELA: validacoes_humanas
-- ============================================

CREATE TABLE validacoes_humanas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    documento_gerado_id UUID NOT NULL REFERENCES documentos_gerados(id) ON DELETE CASCADE,
    validador_id UUID NOT NULL REFERENCES usuarios(id),

    -- Validação
    status_validacao status_validacao NOT NULL,
    observacoes TEXT,
    correcoes_sugeridas JSONB DEFAULT '{}',

    -- Métricas
    tempo_validacao_minutos INTEGER,

    -- Auditoria
    validated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_validacoes_documento ON validacoes_humanas(documento_gerado_id);
CREATE INDEX idx_validacoes_validador ON validacoes_humanas(validador_id);
CREATE INDEX idx_validacoes_status ON validacoes_humanas(status_validacao);

-- ============================================
-- TABELA: fontes_juridicas
-- ============================================

CREATE TABLE fontes_juridicas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    -- Identificação
    nome_fonte VARCHAR(255) NOT NULL UNIQUE,
    tipo_fonte VARCHAR(100) NOT NULL,
    url_base TEXT NOT NULL,

    -- Scraping config
    config_scraping JSONB DEFAULT '{}',
    frequencia_update_horas INTEGER DEFAULT 24,

    -- Status
    ativa BOOLEAN DEFAULT true,
    ultimo_update TIMESTAMP WITH TIME ZONE,
    proximo_update TIMESTAMP WITH TIME ZONE,

    -- Métricas
    total_documentos INTEGER DEFAULT 0,
    ultima_quantidade_coletada INTEGER DEFAULT 0,
    erros_consecutivos INTEGER DEFAULT 0,

    -- Auditoria
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_fontes_ativa ON fontes_juridicas(ativa);
CREATE INDEX idx_fontes_proximo_update ON fontes_juridicas(proximo_update) WHERE ativa = true;

-- ============================================
-- TABELA: alertas_jurisprudencia
-- ============================================

CREATE TABLE alertas_jurisprudencia (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    usuario_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,

    -- Configuração do alerta
    nome_alerta VARCHAR(255) NOT NULL,
    palavras_chave TEXT[] NOT NULL,
    filtros_tribunais instancia_judicial[],
    areas_interesse TEXT[],

    -- Notificação
    tipo_notificacao VARCHAR(50) DEFAULT 'email',
    frequencia_dias INTEGER DEFAULT 7,

    -- Status
    ativo BOOLEAN DEFAULT true,
    ultimo_envio TIMESTAMP WITH TIME ZONE,
    proximo_envio TIMESTAMP WITH TIME ZONE,

    -- Métricas
    total_notificacoes_enviadas INTEGER DEFAULT 0,

    -- Auditoria
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_alertas_usuario ON alertas_jurisprudencia(usuario_id);
CREATE INDEX idx_alertas_ativo ON alertas_jurisprudencia(ativo);
CREATE INDEX idx_alertas_proximo_envio ON alertas_jurisprudencia(proximo_envio) WHERE ativo = true;

-- ============================================
-- TABELA: processos_analisados
-- ============================================

CREATE TABLE processos_analisados (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    usuario_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,

    -- Identificação do processo
    numero_processo VARCHAR(100),
    titulo_processo VARCHAR(500),

    -- Arquivo original
    arquivo_original_path TEXT NOT NULL,
    arquivo_hash VARCHAR(64) NOT NULL,
    tamanho_bytes BIGINT,

    -- Extração
    texto_extraido TEXT,
    paginas INTEGER,

    -- Análise IA
    analise_completa JSONB NOT NULL,
    tese_principal TEXT,
    documentos_relacionados UUID[],
    fundamentacao_legal TEXT,
    sugestoes JSONB,

    -- Métricas
    tempo_processamento_segundos INTEGER,
    confianca_analise FLOAT,

    -- Status
    status_processo status_processo DEFAULT 'ativo',

    -- Auditoria
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_processos_usuario ON processos_analisados(usuario_id);
CREATE INDEX idx_processos_numero ON processos_analisados(numero_processo) WHERE numero_processo IS NOT NULL;
CREATE INDEX idx_processos_status ON processos_analisados(status_processo);
CREATE INDEX idx_processos_data ON processos_analisados(created_at DESC);

-- ============================================
-- TABELA: auditoria
-- ============================================

CREATE TABLE auditoria (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    usuario_id UUID REFERENCES usuarios(id) ON DELETE SET NULL,

    -- Ação
    acao VARCHAR(255) NOT NULL,
    tabela VARCHAR(100),
    registro_id UUID,

    -- Dados
    dados_antes JSONB,
    dados_depois JSONB,

    -- Contexto
    ip_address INET,
    user_agent TEXT,

    -- Timestamp
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_auditoria_usuario ON auditoria(usuario_id);
CREATE INDEX idx_auditoria_acao ON auditoria(acao);
CREATE INDEX idx_auditoria_timestamp ON auditoria(timestamp DESC);
CREATE INDEX idx_auditoria_tabela_registro ON auditoria(tabela, registro_id);

-- ============================================
-- VIEWS ÚTEIS
-- ============================================

-- View: Documentos mais citados
CREATE VIEW documentos_mais_citados AS
SELECT
    d.id,
    d.titulo,
    d.tipo_documento,
    d.orgao_emissor,
    d.data_publicacao,
    COUNT(c.id) as total_citacoes
FROM documentos_juridicos d
LEFT JOIN citacoes c ON d.id = c.documento_citado_id
WHERE d.ativo = true
GROUP BY d.id
ORDER BY total_citacoes DESC;

-- View: Estatísticas por tribunal
CREATE VIEW estatisticas_tribunais AS
SELECT
    instancia,
    COUNT(*) as total_documentos,
    COUNT(*) FILTER (WHERE data_publicacao >= CURRENT_DATE - INTERVAL '30 days') as documentos_mes,
    AVG(relevancia_score) as relevancia_media,
    SUM(citacoes_count) as total_citacoes
FROM documentos_juridicos
WHERE ativo = true
GROUP BY instancia
ORDER BY total_documentos DESC;

-- View: Atividade de usuários
CREATE VIEW atividade_usuarios AS
SELECT
    u.id,
    u.nome,
    u.tipo_conta,
    COUNT(DISTINCT c.id) as total_consultas,
    COUNT(DISTINCT dg.id) as documentos_gerados,
    MAX(c.created_at) as ultima_consulta
FROM usuarios u
LEFT JOIN consultas_usuarios c ON u.id = c.usuario_id
LEFT JOIN documentos_gerados dg ON u.id = dg.usuario_id
WHERE u.ativo = true
GROUP BY u.id, u.nome, u.tipo_conta;

-- ============================================
-- FUNCTIONS
-- ============================================

-- Function: Busca por similaridade vetorial
CREATE OR REPLACE FUNCTION buscar_documentos_similares(
    query_embedding vector(3072),
    limite INTEGER DEFAULT 5,
    threshold FLOAT DEFAULT 0.7
)
RETURNS TABLE (
    documento_id UUID,
    titulo TEXT,
    similarity FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        d.id,
        d.titulo,
        1 - (e.embedding <=> query_embedding) as similarity
    FROM embeddings e
    JOIN documentos_juridicos d ON e.documento_id = d.id
    WHERE d.ativo = true
        AND (1 - (e.embedding <=> query_embedding)) >= threshold
    ORDER BY e.embedding <=> query_embedding
    LIMIT limite;
END;
$$ LANGUAGE plpgsql;

-- Function: Atualizar contador de citações
CREATE OR REPLACE FUNCTION atualizar_contador_citacoes()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE documentos_juridicos
    SET citacoes_count = (
        SELECT COUNT(*)
        FROM citacoes
        WHERE documento_citado_id = NEW.documento_citado_id
    )
    WHERE id = NEW.documento_citado_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Function: Atualizar updated_at automaticamente
CREATE OR REPLACE FUNCTION atualizar_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- TRIGGERS
-- ============================================

-- Trigger: Atualizar contador de citações
CREATE TRIGGER trigger_atualizar_citacoes
AFTER INSERT ON citacoes
FOR EACH ROW
EXECUTE FUNCTION atualizar_contador_citacoes();

-- Triggers: Atualizar updated_at
CREATE TRIGGER trigger_usuarios_updated_at
BEFORE UPDATE ON usuarios
FOR EACH ROW
EXECUTE FUNCTION atualizar_updated_at();

CREATE TRIGGER trigger_documentos_updated_at
BEFORE UPDATE ON documentos_juridicos
FOR EACH ROW
EXECUTE FUNCTION atualizar_updated_at();

CREATE TRIGGER trigger_documentos_gerados_updated_at
BEFORE UPDATE ON documentos_gerados
FOR EACH ROW
EXECUTE FUNCTION atualizar_updated_at();

CREATE TRIGGER trigger_processos_updated_at
BEFORE UPDATE ON processos_analisados
FOR EACH ROW
EXECUTE FUNCTION atualizar_updated_at();

-- ============================================
-- SEED DATA - Usuário Admin
-- ============================================

INSERT INTO usuarios (nome, email, senha_hash, tipo_conta, ativo, email_verificado)
VALUES (
    'Administrador',
    'admin@jurisia.com.br',
    crypt('admin123', gen_salt('bf', 12)),
    'admin',
    true,
    true
);

-- ============================================
-- SEED DATA - Fontes Jurídicas
-- ============================================

INSERT INTO fontes_juridicas (nome_fonte, tipo_fonte, url_base, config_scraping) VALUES
('STF - Supremo Tribunal Federal', 'tribunal', 'https://portal.stf.jus.br/', '{"enabled": true, "priority": "high"}'),
('STJ - Superior Tribunal de Justiça', 'tribunal', 'https://www.stj.jus.br/', '{"enabled": true, "priority": "high"}'),
('TST - Tribunal Superior do Trabalho', 'tribunal', 'https://www.tst.jus.br/', '{"enabled": true, "priority": "medium"}'),
('Planalto - Legislação Federal', 'legislacao', 'https://www.planalto.gov.br/ccivil_03/', '{"enabled": true, "priority": "high"}'),
('DOU - Diário Oficial da União', 'diario', 'https://www.in.gov.br/servicos/diario-oficial-da-uniao', '{"enabled": true, "priority": "medium"}'),
('TJSP - Tribunal de Justiça de SP', 'tribunal', 'https://www.tjsp.jus.br/', '{"enabled": true, "priority": "medium"}'),
('TJRJ - Tribunal de Justiça do RJ', 'tribunal', 'https://www.tjrj.jus.br/', '{"enabled": true, "priority": "medium"}');

-- ============================================
-- COMENTÁRIOS E DOCUMENTAÇÃO
-- ============================================

COMMENT ON TABLE usuarios IS 'Usuários do sistema (advogados, assinantes, visitantes)';
COMMENT ON TABLE documentos_juridicos IS 'Repositório central de documentos jurídicos (leis, súmulas, acórdãos, etc)';
COMMENT ON TABLE embeddings IS 'Vetores de embeddings para busca semântica (RAG)';
COMMENT ON TABLE citacoes IS 'Relações de citações entre documentos jurídicos';
COMMENT ON TABLE consultas_usuarios IS 'Histórico de consultas e buscas realizadas';
COMMENT ON TABLE documentos_gerados IS 'Documentos gerados pela IA (petições, contratos, etc)';
COMMENT ON TABLE processos_analisados IS 'Processos judiciais analisados via upload de PDF';
COMMENT ON TABLE alertas_jurisprudencia IS 'Alertas configurados pelos usuários para nova jurisprudência';

-- ============================================
-- GRANTS (ajustar conforme necessário)
-- ============================================

-- GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO jurisia_api_user;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO jurisia_api_user;

-- ============================================
-- FIM DO SCHEMA
-- ============================================
