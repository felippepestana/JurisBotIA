"""
Serviço de cache com Redis para otimização de performance
"""
from typing import Any, Optional, Callable
import json
import logging
import hashlib
from functools import wraps
from datetime import timedelta

try:
    import redis
    from redis import Redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logging.warning("Redis não instalado - cache desabilitado")

from app.core.config import settings

logger = logging.getLogger(__name__)


class RedisCache:
    """Serviço de cache com Redis"""

    def __init__(self):
        """Inicializa conexão com Redis"""
        self.client: Optional[Redis] = None
        self.enabled = False

        if REDIS_AVAILABLE and settings.REDIS_URL:
            try:
                self.client = redis.from_url(
                    settings.REDIS_URL,
                    decode_responses=True,
                    max_connections=settings.REDIS_MAX_CONNECTIONS
                )
                # Testar conexão
                self.client.ping()
                self.enabled = True
                logger.info("✅ Redis conectado com sucesso")
            except Exception as e:
                logger.warning(f"⚠️ Redis não disponível: {e}")
                self.client = None
                self.enabled = False
        else:
            logger.info("ℹ️ Redis não configurado - cache desabilitado")

    def is_available(self) -> bool:
        """Verifica se Redis está disponível"""
        return self.enabled and self.client is not None

    def _generate_key(self, prefix: str, *args, **kwargs) -> str:
        """
        Gera chave única para cache.

        Args:
            prefix: Prefixo da chave
            *args: Argumentos
            **kwargs: Argumentos nomeados

        Returns:
            Chave única
        """
        # Criar string única com todos os parâmetros
        key_data = f"{prefix}:{str(args)}:{str(sorted(kwargs.items()))}"

        # Hash para chave consistente
        key_hash = hashlib.md5(key_data.encode()).hexdigest()

        return f"{settings.APP_NAME}:{prefix}:{key_hash}"

    def get(self, key: str) -> Optional[Any]:
        """
        Busca valor no cache.

        Args:
            key: Chave do cache

        Returns:
            Valor armazenado ou None
        """
        if not self.is_available():
            return None

        try:
            value = self.client.get(key)
            if value:
                logger.debug(f"Cache HIT: {key}")
                return json.loads(value)
            else:
                logger.debug(f"Cache MISS: {key}")
                return None
        except Exception as e:
            logger.error(f"Erro ao ler cache: {e}")
            return None

    def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ) -> bool:
        """
        Armazena valor no cache.

        Args:
            key: Chave do cache
            value: Valor a armazenar
            ttl: Time to live em segundos (None = padrão)

        Returns:
            True se armazenado com sucesso
        """
        if not self.is_available():
            return False

        try:
            ttl = ttl or settings.CACHE_TTL_SECONDS
            serialized = json.dumps(value, default=str)

            self.client.setex(
                key,
                timedelta(seconds=ttl),
                serialized
            )

            logger.debug(f"Cache SET: {key} (TTL: {ttl}s)")
            return True
        except Exception as e:
            logger.error(f"Erro ao escrever cache: {e}")
            return False

    def delete(self, key: str) -> bool:
        """
        Remove valor do cache.

        Args:
            key: Chave do cache

        Returns:
            True se removido com sucesso
        """
        if not self.is_available():
            return False

        try:
            deleted = self.client.delete(key)
            logger.debug(f"Cache DELETE: {key}")
            return deleted > 0
        except Exception as e:
            logger.error(f"Erro ao deletar cache: {e}")
            return False

    def clear_pattern(self, pattern: str) -> int:
        """
        Remove todas as chaves que correspondem ao padrão.

        Args:
            pattern: Padrão de chave (ex: "search:*")

        Returns:
            Número de chaves removidas
        """
        if not self.is_available():
            return 0

        try:
            keys = self.client.keys(f"{settings.APP_NAME}:{pattern}")
            if keys:
                deleted = self.client.delete(*keys)
                logger.info(f"Cache CLEAR: {deleted} chaves removidas ({pattern})")
                return deleted
            return 0
        except Exception as e:
            logger.error(f"Erro ao limpar cache: {e}")
            return 0

    def get_stats(self) -> dict:
        """
        Retorna estatísticas do cache.

        Returns:
            Dict com estatísticas
        """
        if not self.is_available():
            return {
                "enabled": False,
                "status": "unavailable"
            }

        try:
            info = self.client.info()
            return {
                "enabled": True,
                "status": "connected",
                "used_memory_mb": info.get("used_memory", 0) / (1024 * 1024),
                "connected_clients": info.get("connected_clients", 0),
                "total_keys": self.client.dbsize(),
                "hits": info.get("keyspace_hits", 0),
                "misses": info.get("keyspace_misses", 0),
                "hit_rate": self._calculate_hit_rate(info)
            }
        except Exception as e:
            logger.error(f"Erro ao obter stats: {e}")
            return {"enabled": True, "status": "error", "error": str(e)}

    def _calculate_hit_rate(self, info: dict) -> float:
        """Calcula taxa de acertos do cache"""
        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)
        total = hits + misses

        if total == 0:
            return 0.0

        return round((hits / total) * 100, 2)


def cached(
    prefix: str,
    ttl: Optional[int] = None,
    key_func: Optional[Callable] = None
):
    """
    Decorator para cachear resultados de funções.

    Args:
        prefix: Prefixo da chave de cache
        ttl: Time to live em segundos
        key_func: Função customizada para gerar chave

    Usage:
        @cached(prefix="search", ttl=300)
        async def search_documents(query: str):
            ...
    """
    def decorator(func: Callable):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Gerar chave
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                cache_key = cache_service._generate_key(prefix, *args, **kwargs)

            # Tentar buscar no cache
            cached_result = cache_service.get(cache_key)
            if cached_result is not None:
                logger.info(f"Retornando do cache: {prefix}")
                return cached_result

            # Executar função
            result = await func(*args, **kwargs)

            # Armazenar no cache
            cache_service.set(cache_key, result, ttl)

            return result

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            # Gerar chave
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                cache_key = cache_service._generate_key(prefix, *args, **kwargs)

            # Tentar buscar no cache
            cached_result = cache_service.get(cache_key)
            if cached_result is not None:
                logger.info(f"Retornando do cache: {prefix}")
                return cached_result

            # Executar função
            result = func(*args, **kwargs)

            # Armazenar no cache
            cache_service.set(cache_key, result, ttl)

            return result

        # Retornar wrapper apropriado
        import inspect
        if inspect.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


# Instância global do serviço de cache
cache_service = RedisCache()
