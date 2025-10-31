"""
Configuração de conexão com banco de dados PostgreSQL
"""
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool
from contextlib import contextmanager
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

# Engine do SQLAlchemy
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_pre_ping=True,  # Verifica conexões antes de usar
    echo=settings.DEBUG,  # Log SQL queries em debug mode
)

# SessionLocal para criar sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base para models
Base = declarative_base()


# Dependency para FastAPI
def get_db():
    """
    Dependency para obter session do banco de dados.

    Uso:
        @app.get("/items")
        def read_items(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_context():
    """
    Context manager para uso fora do FastAPI.

    Uso:
        with get_db_context() as db:
            result = db.query(Model).all()
    """
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


# Event listeners para performance monitoring
@event.listens_for(engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    """Log de queries lentas"""
    context._query_start_time = logging.time.time()
    if settings.DEBUG:
        logger.debug(f"Start Query: {statement}")


@event.listens_for(engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    """Log de queries lentas"""
    total = logging.time.time() - context._query_start_time
    if total > 1.0:  # Queries mais lentas que 1 segundo
        logger.warning(f"Slow Query ({total:.2f}s): {statement}")


def init_db():
    """
    Inicializa o banco de dados criando todas as tabelas.
    Usar apenas em desenvolvimento ou migrations.
    """
    logger.info("Inicializando banco de dados...")
    Base.metadata.create_all(bind=engine)
    logger.info("Banco de dados inicializado com sucesso!")


def check_db_connection():
    """
    Verifica se a conexão com o banco está funcionando.

    Returns:
        bool: True se conectado, False caso contrário
    """
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        logger.info("✅ Conexão com banco de dados estabelecida")
        return True
    except Exception as e:
        logger.error(f"❌ Erro ao conectar no banco de dados: {e}")
        return False


def get_db_stats():
    """
    Retorna estatísticas da connection pool.

    Returns:
        dict: Estatísticas da pool
    """
    pool = engine.pool
    return {
        "size": pool.size(),
        "checked_in": pool.checkedin(),
        "checked_out": pool.checkedout(),
        "overflow": pool.overflow(),
        "total": pool.size() + pool.overflow()
    }
