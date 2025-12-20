from pydantic import BaseModel, Field, ConfigDict
import uuid
from typing import Optional
from typing import List


class User(BaseModel):
    id : Optional[str]=Field(default_factory=uuid.uuid4,alias="_id")
    username: str = Field(..., description="The username of the user")
    first_name: str = Field(..., description="The first name of the user")
    last_name: str = Field(..., description="The last name of the user")
   
class ChatMessage(BaseModel):
    question: str = Field(..., description="The question asked in the chat message")
    answer: str = Field(..., description="The answer provided in the chat message",default="")
    model_config = ConfigDict(frozen=True)

class Interview(BaseModel):
    id: int = Field(..., description="The unique identifier for the interview")
    interviewee : User = Field(..., description="The interviewee details")
    interviewer: User = Field(..., description="The interviewer details")
    content : list[ChatMessage] = Field(..., description="The list of chat messages in the interview")




