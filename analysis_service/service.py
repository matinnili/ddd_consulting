from infrastructure.persistence.interview_repository import SqlInterviewRepository
from infrastructure.persistence.database import get_database
from typing import List
from models import Interview


class AnalysisService:
    def __init__(self, repo: SqlInterviewRepository):
        self.repo = repo
    
    async def __prepare_content(self, ids : List[str]) -> str:
        content=""
        interviews = await self.repo(get_database().session_factory())
        selected_interviews=await interviews.query(Interview).filter(Interview.id.in_(ids)).all()
        for interview in selected_interviews:
            content+=interview.content
    async def analyze_interview(self, ids : List[str]) -> str:
        content=await self.__prepare_content(ids)
        analysis=get_analysis(content)
        return analysis