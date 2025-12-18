from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional
from models import Interview, User



class InterviewRepository(ABC):



    @abstractmethod
    async def add(self, interview: Interview) -> None:
        pass

    @abstractmethod
    async def get(self, item_id: str) -> Optional[Interview]:
        pass

    @abstractmethod
    async def list(self) -> List[Interview]:
        pass

class UserRepository(ABC):



    @abstractmethod
    async def add(self, user: User) -> None:
        pass

    @abstractmethod
    async def get(self, user_id: str) -> Optional[User]:
        pass

    @abstractmethod
    async def list(self) -> List[User]:
        pass