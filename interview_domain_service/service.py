from uow import InterviewUnitOfWork
from models import Interview
from models import ChatMessage
from typing import List

class InterviewService:
    def __init__(self, uow: InterviewUnitOfWork):
        self.uow = uow

    async def create_interview(self, interview: Interview) -> Interview:
        with self.uow as uow:
            await uow.interviews.add(interview)
            await uow.commit()
        return interview
        
    async def add_chat(self, interview_id: str, chat: List[ChatMessage]) -> None:
        with self.uow as uow:
            interview = await uow.interviews.get(interview_id)
            if not interview:
                raise ValueError("Interview not found")
            interview.content=chat
            await uow.interviews.update(interview_id)
            await uow.commit()