"""Database connection and session management."""
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager

from app.core.config import settings


@contextmanager
def get_db_connection():
    """Get a database connection."""
    conn = None
    try:
        conn = psycopg2.connect(
            settings.DATABASE_URL,
            cursor_factory=RealDictCursor
        )
        yield conn
    finally:
        if conn is not None:
            conn.close()


@contextmanager
def get_db_cursor():
    """Get a database cursor."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close() 