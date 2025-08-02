from sqlalchemy import Column, Integer, String, Date, Boolean, Text
from sqlalchemy.orm import relationship
from database import Base

class Habit(Base):
    __tablename__ = "habits"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    repeat_frequency = Column(String, nullable=False)  # "MONDAY,TUESDAY,..."
    tags = Column(String, nullable=True)  # "tag1,tag2,..."
    user_id = Column(Integer, index=True, default=1)  # For user association

class Completion(Base):
    __tablename__ = "completions"
    
    habit_id = Column(Integer, primary_key=True)
    completion_date = Column(String, primary_key=True)  # ISO format date string