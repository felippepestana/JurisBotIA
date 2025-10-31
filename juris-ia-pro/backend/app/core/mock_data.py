"""
Dados mockados para desenvolvimento sem banco de dados
"""
from datetime import date
from typing import List, Dict, Any


# Documentos jurídicos mockados
MOCK_LEGAL_DOCUMENTS: List[Dict[str, Any]] = [
    {
        "id": "stj-sumula-297",
        "titulo": "STJ - Súmula 297",
        "tipo_documento": "sumula",
        "conteudo_completo": "O Código de Defesa do Consumidor é aplicável às instituições financeiras.",
        "ementa": "Aplicabilidade do CDC às instituições financeiras",
        "orgao_emissor": "Superior Tribunal de Justiça",
        "instancia": "STJ",
        "data_publicacao": date(2004, 9, 15),
        "relevancia_score": 0.98,
        "citacoes_count": 1247,
        "palavras_chave": ["cdc", "instituições financeiras", "bancos", "consumidor"],
        "assuntos": ["Direito do Consumidor", "Direito Bancário"],
        "indexed_at": "2024-01-15T10:00:00Z"
    },
    {
        "id": "stf-re-591054",
        "titulo": "STF - RE 591.054",
        "tipo_documento": "decisao",
        "conteudo_completo": "É inconstitucional a cobrança de tarifa de abertura de conta corrente, por constituir venda casada vedada pelo art. 39, I, do CDC. A cobrança de tarifas bancárias deve observar os princípios da boa-fé objetiva, da transparência e da razoabilidade.",
        "ementa": "CONSTITUCIONAL. DIREITO DO CONSUMIDOR. Tarifa de abertura de conta corrente. Inconstitucionalidade.",
        "orgao_emissor": "Supremo Tribunal Federal",
        "instancia": "STF",
        "relator": "Min. Marco Aurélio",
        "data_publicacao": date(2016, 5, 24),
        "relevancia_score": 0.95,
        "citacoes_count": 423,
        "palavras_chave": ["tarifa", "conta corrente", "venda casada", "cdc", "inconstitucional"],
        "assuntos": ["Direito do Consumidor", "Direito Bancário", "Direito Constitucional"],
        "indexed_at": "2024-01-15T10:30:00Z"
    },
    {
        "id": "lei-8078-art3",
        "titulo": "Lei 8.078/90 - Art. 3º, § 2º",
        "tipo_documento": "lei",
        "conteudo_completo": "Art. 3º. Fornecedor é toda pessoa física ou jurídica, pública ou privada, nacional ou estrangeira, bem como os entes despersonalizados, que desenvolvem atividade de produção, montagem, criação, construção, transformação, importação, exportação, distribuição ou comercialização de produtos ou prestação de serviços.\n\n§ 2º Serviço é qualquer atividade fornecida no mercado de consumo, mediante remuneração, inclusive as de natureza bancária, financeira, de crédito e securitária, salvo as decorrentes das relações de caráter trabalhista.",
        "ementa": "Definição de fornecedor e serviço no CDC",
        "orgao_emissor": "Congresso Nacional",
        "instancia": "OUTRA",
        "numero_processo": "Lei 8.078/1990",
        "data_publicacao": date(1990, 9, 11),
        "relevancia_score": 0.92,
        "citacoes_count": 2834,
        "palavras_chave": ["serviço", "consumo", "bancária", "financeira", "crédito", "fornecedor"],
        "assuntos": ["Direito do Consumidor", "Legislação"],
        "indexed_at": "2024-01-15T11:00:00Z"
    },
    {
        "id": "tjsp-apelacao-123",
        "titulo": "TJSP - Apelação Cível nº 1001234-56.2023.8.26.0100",
        "tipo_documento": "acordao",
        "conteudo_completo": "DIREITO DO CONSUMIDOR. SERVIÇOS BANCÁRIOS. Aplicabilidade do CDC às instituições financeiras, conforme Súmula 297 do STJ. Cobrança de tarifa abusiva. Tarifa de manutenção de conta superior aos limites razoáveis. Restituição em dobro. Art. 42, parágrafo único, do CDC. Recurso provido.",
        "ementa": "Direito do Consumidor. Serviços bancários. Tarifa abusiva. Restituição em dobro.",
        "decisao": "RECURSO PROVIDO",
        "orgao_emissor": "Tribunal de Justiça de São Paulo",
        "instancia": "TJ",
        "numero_processo": "1001234-56.2023.8.26.0100",
        "relator": "Des. João Silva Santos",
        "data_publicacao": date(2023, 11, 15),
        "data_julgamento": date(2023, 11, 10),
        "relevancia_score": 0.89,
        "citacoes_count": 12,
        "palavras_chave": ["direito consumidor", "serviços bancários", "tarifa abusiva", "restituição"],
        "assuntos": ["Direito do Consumidor", "Direito Bancário", "Responsabilidade Civil"],
        "indexed_at": "2024-01-15T11:30:00Z"
    },
    {
        "id": "stj-resp-1255573",
        "titulo": "STJ - REsp 1.255.573/RS",
        "tipo_documento": "acordao",
        "conteudo_completo": "RECURSO ESPECIAL. DIREITO DO CONSUMIDOR. AÇÃO COLETIVA. DANO MORAL. SUPERENDIVIDAMENTO. O superendividamento do consumidor é questão relevante que merece atenção especial. A concessão irresponsável de crédito configura prática abusiva passível de reparação por danos morais coletivos.",
        "ementa": "Direito do consumidor. Superendividamento. Concessão irresponsável de crédito. Dano moral coletivo.",
        "decisao": "RECURSO PARCIALMENTE PROVIDO",
        "orgao_emissor": "Superior Tribunal de Justiça",
        "instancia": "STJ",
        "numero_processo": "REsp 1.255.573/RS",
        "relator": "Min. Nancy Andrighi",
        "data_publicacao": date(2015, 8, 25),
        "data_julgamento": date(2015, 8, 11),
        "relevancia_score": 0.94,
        "citacoes_count": 567,
        "palavras_chave": ["superendividamento", "crédito irresponsável", "dano moral coletivo", "consumidor"],
        "assuntos": ["Direito do Consumidor", "Direito Bancário", "Responsabilidade Civil"],
        "indexed_at": "2024-01-15T12:00:00Z"
    },
    {
        "id": "cf-art5-xxxii",
        "titulo": "Constituição Federal - Art. 5º, XXXII",
        "tipo_documento": "lei",
        "conteudo_completo": "Art. 5º Todos são iguais perante a lei, sem distinção de qualquer natureza, garantindo-se aos brasileiros e aos estrangeiros residentes no País a inviolabilidade do direito à vida, à liberdade, à igualdade, à segurança e à propriedade, nos termos seguintes:\n\nXXXII - o Estado promoverá, na forma da lei, a defesa do consumidor;",
        "ementa": "Proteção constitucional do consumidor",
        "orgao_emissor": "Congresso Nacional",
        "instancia": "OUTRA",
        "data_publicacao": date(1988, 10, 5),
        "relevancia_score": 0.97,
        "citacoes_count": 4521,
        "palavras_chave": ["constituição", "consumidor", "defesa", "direito fundamental"],
        "assuntos": ["Direito Constitucional", "Direito do Consumidor"],
        "indexed_at": "2024-01-15T12:30:00Z"
    }
]


def search_mock_documents(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Busca simples em documentos mockados.

    Args:
        query: Termos de busca
        limit: Número máximo de resultados

    Returns:
        Lista de documentos que correspondem à busca
    """
    query_lower = query.lower()
    results = []

    for doc in MOCK_LEGAL_DOCUMENTS:
        score = 0

        # Score por palavras-chave
        for keyword in doc.get("palavras_chave", []):
            if keyword.lower() in query_lower:
                score += 0.3

        # Score por título
        if any(word in doc["titulo"].lower() for word in query_lower.split()):
            score += 0.4

        # Score por conteúdo
        if any(word in doc["conteudo_completo"].lower() for word in query_lower.split()):
            score += 0.3

        if score > 0:
            doc_copy = doc.copy()
            doc_copy["similarity_score"] = min(score, 1.0)
            results.append(doc_copy)

    # Ordenar por score
    results.sort(key=lambda x: x["similarity_score"], reverse=True)

    return results[:limit]


def get_mock_document_by_id(doc_id: str) -> Dict[str, Any] | None:
    """
    Busca documento mockado por ID.

    Args:
        doc_id: ID do documento

    Returns:
        Documento ou None se não encontrado
    """
    for doc in MOCK_LEGAL_DOCUMENTS:
        if doc["id"] == doc_id:
            return doc.copy()
    return None


def get_mock_stats() -> Dict[str, Any]:
    """
    Retorna estatísticas dos dados mockados.

    Returns:
        Dict com estatísticas
    """
    instancias = set()
    tipos = set()

    for doc in MOCK_LEGAL_DOCUMENTS:
        instancias.add(doc.get("instancia", "OUTRA"))
        tipos.add(doc["tipo_documento"])

    return {
        "total_documents": len(MOCK_LEGAL_DOCUMENTS),
        "tribunais": list(instancias),
        "tipos_documentos": list(tipos),
        "total_citacoes": sum(doc["citacoes_count"] for doc in MOCK_LEGAL_DOCUMENTS),
        "relevancia_media": sum(doc["relevancia_score"] for doc in MOCK_LEGAL_DOCUMENTS) / len(MOCK_LEGAL_DOCUMENTS)
    }
