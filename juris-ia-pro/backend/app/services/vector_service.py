"""
Serviço de busca vetorial com Qdrant
"""
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime
import uuid

try:
    from qdrant_client import QdrantClient
    from qdrant_client.http import models
    QDRANT_AVAILABLE = True
except ImportError:
    QDRANT_AVAILABLE = False
    logging.warning("Qdrant client não instalado")

from app.core.config import settings
from app.services.openai_service import openai_service

logger = logging.getLogger(__name__)


class VectorService:
    """Serviço de busca vetorial com Qdrant"""

    def __init__(self):
        """Inicializa cliente Qdrant"""
        self.client: Optional[QdrantClient] = None
        self.collection_name = settings.QDRANT_COLLECTION_NAME
        self.embedding_dim = settings.EMBEDDING_DIMENSION
        self.enabled = False

        if QDRANT_AVAILABLE:
            try:
                self.client = QdrantClient(
                    url=settings.QDRANT_URL,
                    api_key=settings.QDRANT_API_KEY,
                    timeout=30
                )

                # Verificar se coleção existe, se não, criar
                self._ensure_collection()

                self.enabled = True
                logger.info(f"✅ Qdrant conectado: {settings.QDRANT_URL}")
            except Exception as e:
                logger.warning(f"⚠️ Qdrant não disponível: {e}")
                self.client = None
                self.enabled = False
        else:
            logger.info("ℹ️ Qdrant não instalado - busca vetorial desabilitada")

    def is_available(self) -> bool:
        """Verifica se Qdrant está disponível"""
        return self.enabled and self.client is not None

    def _ensure_collection(self):
        """Garante que a coleção existe"""
        try:
            # Verificar se coleção existe
            collections = self.client.get_collections().collections
            collection_names = [c.name for c in collections]

            if self.collection_name not in collection_names:
                logger.info(f"Criando coleção: {self.collection_name}")

                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=self.embedding_dim,
                        distance=models.Distance.COSINE
                    )
                )

                logger.info(f"✅ Coleção criada: {self.collection_name}")
            else:
                logger.info(f"Coleção já existe: {self.collection_name}")

        except Exception as e:
            logger.error(f"Erro ao verificar/criar coleção: {e}")
            raise

    def add_document(
        self,
        document_id: str,
        text: str,
        metadata: Dict[str, Any]
    ) -> bool:
        """
        Adiciona documento ao índice vetorial.

        Args:
            document_id: ID único do documento
            text: Texto para gerar embedding
            metadata: Metadados do documento

        Returns:
            True se adicionado com sucesso
        """
        if not self.is_available():
            logger.warning("Qdrant não disponível")
            return False

        if not openai_service.is_available():
            logger.warning("OpenAI não disponível para gerar embeddings")
            return False

        try:
            # Gerar embedding
            logger.info(f"Gerando embedding para documento: {document_id}")
            embedding = openai_service.generate_embedding(text)

            # Preparar payload
            payload = {
                "document_id": document_id,
                "indexed_at": datetime.utcnow().isoformat(),
                **metadata
            }

            # Inserir no Qdrant
            self.client.upsert(
                collection_name=self.collection_name,
                points=[
                    models.PointStruct(
                        id=str(uuid.uuid4()),
                        vector=embedding,
                        payload=payload
                    )
                ]
            )

            logger.info(f"✅ Documento indexado: {document_id}")
            return True

        except Exception as e:
            logger.error(f"Erro ao adicionar documento: {e}")
            return False

    def add_documents_batch(
        self,
        documents: List[Dict[str, Any]],
        text_field: str = "conteudo_completo"
    ) -> Dict[str, int]:
        """
        Adiciona múltiplos documentos em lote.

        Args:
            documents: Lista de documentos
            text_field: Campo com o texto para embedding

        Returns:
            Dict com estatísticas
        """
        if not self.is_available() or not openai_service.is_available():
            return {"success": 0, "failed": 0}

        success_count = 0
        failed_count = 0

        for i, doc in enumerate(documents, 1):
            try:
                logger.info(f"Processando documento {i}/{len(documents)}")

                text = doc.get(text_field, "")
                if not text or len(text) < 50:
                    logger.warning(f"Texto muito curto: {doc.get('id', 'unknown')}")
                    failed_count += 1
                    continue

                # Preparar metadados
                metadata = {
                    k: v for k, v in doc.items()
                    if k != text_field and k != "id"
                }

                # Adicionar
                if self.add_document(
                    document_id=doc.get("id", str(uuid.uuid4())),
                    text=text[:4000],  # Limitar tamanho
                    metadata=metadata
                ):
                    success_count += 1
                else:
                    failed_count += 1

            except Exception as e:
                logger.error(f"Erro ao processar documento {i}: {e}")
                failed_count += 1

        logger.info(
            f"Batch completo: {success_count} sucesso, "
            f"{failed_count} falhas"
        )

        return {
            "success": success_count,
            "failed": failed_count,
            "total": len(documents)
        }

    def search(
        self,
        query: str,
        limit: int = 10,
        filters: Optional[Dict[str, Any]] = None,
        score_threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Busca documentos por similaridade vetorial.

        Args:
            query: Texto da busca
            limit: Número máximo de resultados
            filters: Filtros de metadados
            score_threshold: Threshold de similaridade mínima

        Returns:
            Lista de documentos encontrados
        """
        if not self.is_available():
            logger.warning("Qdrant não disponível")
            return []

        if not openai_service.is_available():
            logger.warning("OpenAI não disponível para busca")
            return []

        try:
            # Gerar embedding da query
            logger.info(f"Buscando por: {query[:50]}...")
            query_embedding = openai_service.generate_embedding(query)

            # Preparar filtros do Qdrant
            qdrant_filter = None
            if filters:
                qdrant_filter = self._build_qdrant_filter(filters)

            # Buscar
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit,
                query_filter=qdrant_filter,
                score_threshold=score_threshold
            )

            # Formatar resultados
            documents = []
            for result in results:
                doc = {
                    **result.payload,
                    "similarity_score": result.score,
                    "vector_id": result.id
                }
                documents.append(doc)

            logger.info(f"✅ Encontrados {len(documents)} documentos")
            return documents

        except Exception as e:
            logger.error(f"Erro na busca vetorial: {e}")
            return []

    def _build_qdrant_filter(self, filters: Dict[str, Any]):
        """
        Constrói filtro do Qdrant a partir de dict.

        Args:
            filters: Dict com filtros

        Returns:
            Objeto Filter do Qdrant
        """
        conditions = []

        for key, value in filters.items():
            if isinstance(value, list):
                # OR condition
                conditions.append(
                    models.FieldCondition(
                        key=key,
                        match=models.MatchAny(any=value)
                    )
                )
            else:
                # Exact match
                conditions.append(
                    models.FieldCondition(
                        key=key,
                        match=models.MatchValue(value=value)
                    )
                )

        if conditions:
            return models.Filter(must=conditions)

        return None

    def delete_document(self, document_id: str) -> bool:
        """
        Remove documento do índice.

        Args:
            document_id: ID do documento

        Returns:
            True se removido com sucesso
        """
        if not self.is_available():
            return False

        try:
            # Buscar pontos com esse document_id
            points = self.client.scroll(
                collection_name=self.collection_name,
                scroll_filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="document_id",
                            match=models.MatchValue(value=document_id)
                        )
                    ]
                ),
                limit=100
            )

            # Deletar pontos encontrados
            if points and points[0]:
                point_ids = [p.id for p in points[0]]

                self.client.delete(
                    collection_name=self.collection_name,
                    points_selector=models.PointIdsList(
                        points=point_ids
                    )
                )

                logger.info(f"✅ Documento removido: {document_id}")
                return True

            logger.warning(f"Documento não encontrado: {document_id}")
            return False

        except Exception as e:
            logger.error(f"Erro ao remover documento: {e}")
            return False

    def get_collection_stats(self) -> Dict[str, Any]:
        """
        Retorna estatísticas da coleção.

        Returns:
            Dict com estatísticas
        """
        if not self.is_available():
            return {
                "enabled": False,
                "status": "unavailable"
            }

        try:
            info = self.client.get_collection(self.collection_name)

            return {
                "enabled": True,
                "status": "connected",
                "collection_name": self.collection_name,
                "vectors_count": info.vectors_count,
                "indexed_vectors_count": info.indexed_vectors_count,
                "points_count": info.points_count,
                "segments_count": info.segments_count,
                "vector_dimension": self.embedding_dim
            }

        except Exception as e:
            logger.error(f"Erro ao obter stats: {e}")
            return {"enabled": True, "status": "error", "error": str(e)}

    def clear_collection(self) -> bool:
        """
        Remove todos os documentos da coleção.

        Returns:
            True se limpo com sucesso
        """
        if not self.is_available():
            return False

        try:
            self.client.delete_collection(self.collection_name)
            self._ensure_collection()

            logger.info(f"✅ Coleção limpa: {self.collection_name}")
            return True

        except Exception as e:
            logger.error(f"Erro ao limpar coleção: {e}")
            return False


# Instância global
vector_service = VectorService()
