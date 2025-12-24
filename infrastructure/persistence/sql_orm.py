from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship,mapper
from sqlalchemy import String, JSON, TypeDecorator, ARRAY, Integer, ForeignKey
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

    id = mapped_column(String)
    username = mapped_column(String(50),primary_key=True)
    first_name = mapped_column(String(50))
    last_name = mapped_column(String(50))
    resume_details = mapped_column(ResumeDetailType, nullable=True)
    personality_test = mapped_column(JSON, nullable=True)
    gender = mapped_column(String(50))
    resume_details = relationship("ResumeDetailORM", back_populates="user")


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

class ResumeDetailORM(Base):
    __tablename__ = "resume_details"
    id = mapped_column(String, primary_key=True)
    courses = mapped_column(ARRAY(String))
    experience = mapped_column(ARRAY(String))
    skills = mapped_column(ARRAY(String))
    english_proficiency = mapped_column(String(50))
    question_answer = mapped_column(str)
    age = mapped_column(Integer)
    education = mapped_column(ARRAY(String))
    user_id = mapped_column(String, ForeignKey("users.username"))

class PersonalityTestORM(Base):
    __tablename__ = "personality_tests"
    id = mapped_column(String, primary_key=True)
    holland_result = mapped_column(JSON)
    neo_result = mapped_column(JSON)
    clifton_result = mapped_column(JSON)
    username = mapped_column(String, ForeignKey("users.username"))
    

user_mapper = mapper(models.User, UserORM)
interview_mapper = mapper(models.Interview, InterviewORM)
chat_mapper = mapper(models.Chat, ChatORM)
resume_detail_mapper = mapper(models.ResumeDetail, ResumeDetailORM)