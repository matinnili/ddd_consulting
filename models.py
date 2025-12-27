from pydantic import BaseModel, Field, ConfigDict
import uuid
from typing import Optional
from typing import List,Literal




class AuthenticatedUser(BaseModel):

    

class ResumeDetail(BaseModel):
    age: str =Field(default="اطلاعاتی در این زمینه وجود ندارد")
    education: List[str] = Field(default=["اطلاعاتی در این زمینه وجود ندارد"])
    experience: List[str] = Field(default=["اطلاعاتی در این زمینه وجود ندارد"])
    skills: List[str] = Field(default=["اطلاعاتی در این زمینه وجود ندارد"])
    english_proficiency: str = Field(default="اطلاعاتی در این زمینه وجود ندارد", description="English proficiency level")
    Question_Answer: Optional[str] = Field(default="اطلاعاتی در این زمینه وجود ندارد")
    courses: List[str] = Field(default=["اطلاعاتی در این زمینه وجود ندارد"])
    user : str = Field(..., description="The username")


class User(BaseModel):
    id : Optional[str]=Field(default_factory=uuid.uuid4,alias="_id")
    username: str = Field(..., description="The username of the user")
    first_name: str = Field(..., description="The first name of the user")
    last_name: str = Field(..., description="The last name of the user")
    resume_details:Optional[ResumeDetail] = Field(..., description="The resume details of the user",default=None)
    personality_test:Optional[dict] = Field(..., description="The personality traits of the user",default=None)
    gender: Literal["male", "female"] = Field(..., description="The gender of the user")

    def add_resumedetails(self, resume_details: ResumeDetail) -> None:
        if not isinstance(resume_details, ResumeDetail):
            raise ValueError("Resume details must be a ResumeDetail object")
        if self.resume_details is None:
            self.resume_details = resume_details
        else:
            raise ValueError("Resume details already exists")

    def add_personality_test(self, personality_test: dict) -> None:
        if not isinstance(personality_test, dict):
            raise ValueError("Personality test must be a dictionary")
        if self.personality_test is None:
            self.personality_test = personality_test
        else:
            raise ValueError("Personality test already exists")

class ChatMessage(BaseModel):
    question: str = Field(..., description="The question asked in the chat message")
    answer: Optional[str] = Field(..., description="The answer provided in the chat message",default=None)
   
class Chat(BaseModel):
    messages: list[ChatMessage] = Field(..., description="The list of chat messages in the chat")
    chat_id: str = Field(..., description="The unique identifier for the chat")
    model_config = ConfigDict(frozen=True)
    
    def add_message(self, message: ChatMessage) -> None:
        if ChatMessage.answer is None:
            raise ValueError("Answer is required")
        else:
            self.messages.append(message)
            


class Interview(BaseModel):
    id: int = Field(..., description="The unique identifier for the interview")
    interviewee : User = Field(..., description="The interviewee details")
    interviewer: User = Field(..., description="The interviewer details")
    questions: list[str] = Field(..., description="The list of questions asked in the interview")
    content : Optional[Chat] = Field(..., description="The chat details for the interview",default=None)
    
    def add_chat(self, chat: Chat) -> None:
        if self.content is None:
            self.content = chat
        else:
            raise ValueError("Chat already exists")