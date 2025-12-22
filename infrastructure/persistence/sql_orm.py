from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship,mapper
from sqlalchemy import String, JSON, TypeDecorator
import models


class ResumeDetailType(TypeDecorator):
    impl = JSON
    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if not isinstance(value, models.ResumeDetail):
            raise ValueError("Value must be a ResumeDetail object")
        return value.model_dump()
    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return models.ResumeDetail.model_validate(value)


class Base(DeclarativeBase):
    pass

class UserORM(Base):
    __tablename__ = "users"

    id = mapped_column(primary_key=True)
    username = mapped_column(String(50))
    first_name = mapped_column(String(50))
    last_name = mapped_column(String(50))
    resume_details = mapped_column(ResumeDetailType, nullable=True)
    personality_test = mapped_column(JSON, nullable=True)
    gender = mapped_column(String(50))



class ChatORM(Base):
    __tablename__ = "chats"

    id = mapped_column(primary_key=True)
    messages = mapped_column(JSON)
    chat_id = mapped_column(String(50))
    
class InterviewORM(Base):
    __tablename__ = "interviews"

    id = mapped_column(primary_key=True)
    interviewee = relationship("UserORM", back_populates="interviews")
    interviewer = relationship("UserORM", back_populates="interviews")
    chats = relationship("ChatORM", back_populates="interviews")


user_mapper = mapper(models.User, UserORM)
interview_mapper = mapper(models.Interview, InterviewORM)
chat_mapper = mapper(models.Chat, ChatORM)