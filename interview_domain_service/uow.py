from abc import ABC, abstractmethod
from repository import InterviewRepository
from infrastructure.persistence.interview_repository import SqlInterviewRepository
from infrastructure.persistence.database import get_database
from sqlalchemy.orm import sessionmaker


class InterviewUnitOfWork(ABC):
    interviews : InterviewRepository

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


    class SqlInterviewUnitOfWork(InterviewUnitOfWork):

        def __init__(self, sessionmaker: sessionmaker):
            self.sessionmaker = get_database().session_factory

        def __enter__(self):
            self.session = self.sessionmaker()
            self.interviews = SqlInterviewRepository(self.session)
            return super().__enter__()

        def __exit__(self, *args):
            super().__exit__(*args)
            self.session.close()

        def commit(self) -> None:
            self.session.commit()

        def rollback(self) -> None:
            self.session.rollback()