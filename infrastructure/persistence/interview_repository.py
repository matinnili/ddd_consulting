from repository import InterviewRepository
from models import Interview
from typing import List, Optional

class SqlInterviewRepository(InterviewRepository):


    def __init__(self, session):
        self.session = session

    async def add(self, interview: Interview) -> None:
        # Implementation for adding an interview to a SQL database
        session=self.session
        session.add(interview)
        session.commit()

    async def get(self, item_id: str) -> Optional[Interview]:
        # Implementation for retrieving an interview by ID from a SQL database
        session=self.session
        interview=session.query(Interview).filter_by(id=item_id)
        return interview.first()

    async def list(self) -> List[Interview]:
        # Implementation for listing all interviews from a SQL database
        session=self.session
        interviews=session.query(Interview).all()
        return interviews
    async def update(self, id:str) -> None:
        session=self.session
        interview=session.query(Interview).filter_by(id=id)
        interview.update(interview)
        session.commit()