from events import InterviewCreateMessage,InterviewCompleteMessage
from interview_domain_service.uow import InterviewUnitOfWork

def interview_creation_handler(event : InterviewCreateMessage, uow : InterviewUnitOfWork):
    "send message to employee"
    pass

def interview_completion_handler(event : InterviewCompleteMessage, uow : InterviewUnitOfWork):
    "send message to Manager"
    pass