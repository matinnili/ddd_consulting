from abc import ABC, abstractmethod
from repository import UserRepository
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import config
from infrastructure.persistence.user_repository import SqlUserRepository
from infrastructure.persistence.database import get_database

class UserUnitOfWork(ABC):

    users : UserRepository

    @abstractmethod
    def __enter__(self):
        return self

    @abstractmethod
    def __exit__(self, *args):
        self.rollback()

    @abstractmethod
    async def commit(self) -> None:
        pass

    @abstractmethod
    async def rollback(self) -> None:
        pass

DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(
        config.get_postgres_uri(),
    )
)


class SqlUserUnitOfWork(UserUnitOfWork):
    def __init__(self, sessionmaker: sessionmaker ):
        self.sessionmaker = get_database().session_factory

    def __enter__(self):
        self.session = self.sessionmaker()
        self.users = SqlUserRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()
        

    async def commit(self) -> None:
        self.session.commit()

    async def rollback(self) -> None:
        self.session.rollback()