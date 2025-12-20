from abc import ABC, abstractmethod
from typing import List, Optional
from models import RAG

class RAGRepository(ABC):

    @abstractmethod
    async def add_document(self, document: str) -> None:
        pass

    @abstractmethod
    async def find_chunks(self, query:str) -> List[str]:
        pass



class ChromaRepository(RAGRepository):  
    def __init__(self, collection_name: str):
        self.collection_name = collection_name

    async def add_document(self, document: str) -> None:
        pass

    async def find_chunks(self, query:str) -> List[str]:
        pass