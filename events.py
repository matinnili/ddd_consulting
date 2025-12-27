from pydantic import BaseModel, Field

class Event(BaseModel):
    pass
class InterviewCreateMessage(Event):
    topic : str
    interviewee_username : str
    interviewer_username : str
    message : str=Field(..., description="The message to create the interview",default="Interview created")

class InterviewCompleteMessage(Event):
    topic : str
    interviewee_username : str
    interviewer_username : str
    message : str=Field(..., description="The message to complete the interview",default="Interview completed")