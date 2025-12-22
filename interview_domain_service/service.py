from uow import InterviewUnitOfWork
from models import Interview
from models import ChatMessage, Chat
from typing import List

class InterviewService:
    def __init__(self, uow: InterviewUnitOfWork):
        self.uow = uow

    async def create_interview(self, interview: Interview) -> Interview:
        with self.uow as uow:
            await uow.interviews.add(interview)
            await uow.commit()
        return interview
        
    async def add_chat(self, interview_id: str, chat: Chat) -> None:
        with self.uow as uow:
            interview = await uow.interviews.get(interview_id)
            if not interview:
                raise ValueError("Interview not found")
            interview.add_chat(chat)
            await uow.interviews.update(interview_id)
            await uow.commit()