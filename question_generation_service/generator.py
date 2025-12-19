from infrastructure.persistence.interview_repository import SqlInterviewRepository
from infrastructure.persistence.user_repository import SqlUserRepository    
from models import Interview, User
from utils import generate_questions

class QuestionGenerationService:
    def __init__(self, interview_repo: SqlInterviewRepository, user_repo: SqlUserRepository):
        self.interview_repo = interview_repo
        self.user_repo = user_repo

    async def generate_questions_for_interview(self, user_id: str) -> list[str]:
        user = await self.user_repo.get(user_id).model_dump()
        questions = generate_questions(prompt=user["bio"], max_questions=5,**user)

        interviewee = await self.user_repo.get(Interview.interviewee_id)
        if not interviewee:
            raise ValueError("Interviewee not found")

        # Placeholder logic for question generation
        questions = [
            f"What motivated you to apply for this position, {interviewee.first_name}?",
            "Can you describe a challenging situation you faced at work and how you handled it?",
            "Where do you see yourself in five years?"
        ]
        return questions