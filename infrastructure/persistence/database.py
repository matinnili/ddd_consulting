from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from threading import Lock
from typing import Optional


class Database:
    """
    Singleton database connection manager.
    Thread-safe, lazy initialization.
    """
    _instance: Optional["Database"] = None
    _lock: Lock = Lock()
    
    _engine = None
    _session_factory = None
    
    def __new__(cls, connection_string: str = None):
        if cls._instance is None:
            with cls._lock:
                # Double-checked locking
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def initialize(self, connection_string: str, **engine_kwargs):
        """Initialize the database engine (only runs once)."""
        if not self._initialized:
            with self._lock:
                if not self._initialized:
                    self._engine = create_engine(
                        connection_string,
                        pool_pre_ping=True,  # Verify connections before use
                        pool_size=5,
                        max_overflow=10,
                        **engine_kwargs
                    )
                    self._session_factory = sessionmaker(
                        bind=self._engine,
                        autocommit=False,
                        autoflush=False,
                    )
                    self._initialized = True
    
    @property
    def engine(self):
        if not self._initialized:
            raise RuntimeError("Database not initialized. Call initialize() first.")
        return self._engine
    
    @property
    def session_factory(self) -> sessionmaker:
        if not self._initialized:
            raise RuntimeError("Database not initialized. Call initialize() first.")
        return self._session_factory
    
    def get_session(self) -> Session:
        """Get a new database session."""
        return self.session_factory()
    
    @classmethod
    def reset(cls):
        """Reset singleton (useful for testing)."""
        with cls._lock:
            if cls._instance and cls._instance._engine:
                cls._instance._engine.dispose()
            cls._instance = None


# Convenience function
def get_database() -> Database:
    """Get the singleton database instance."""
    return Database()