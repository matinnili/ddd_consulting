from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship,mapper
from sqlalchemy import String, JSON
import models



class Base(DeclarativeBase):
    pass

class UserORM(Base):
    __tablename__ = "users"

    id = mapped_column(primary_key=True)
    username = mapped_column(String(50))
    first_name = mapped_column(String(50))
    last_name = mapped_column(String(50))
    




class InterviewORM(Base):
    __tablename__ = "interviews"

    id = mapped_column(primary_key=True)
    interviewee = relationship("UserORM", back_populates="interviews")
    interviewer = relationship("UserORM", back_populates="interviews")
    chat = mapped_column(JSON)


user_mapper = mapper(models.User, UserORM)
interview_mapper = mapper(models.Interview, InterviewORM)
