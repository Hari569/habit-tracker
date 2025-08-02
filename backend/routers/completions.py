from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.habit import Habit, Completion
from database import get_db
from pydantic import BaseModel
from typing import List
from datetime import date

router = APIRouter()

class CompletionCreate(BaseModel):
    habit_id: int
    completion_date: str  # ISO format date string

class CompletionResponse(BaseModel):
    habit_id: int
    completion_date: str

    class Config:
        from_attributes = True

@router.post("/completions/", response_model=CompletionResponse)
def complete_habit(completion: CompletionCreate, db: Session = Depends(get_db)):
    # Check if habit exists
    habit = db.query(Habit).filter(Habit.id == completion.habit_id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    # Validate date format
    try:
        date.fromisoformat(completion.completion_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    # Create or update completion
    db_completion = db.query(Completion).filter(
        Completion.habit_id == completion.habit_id,
        Completion.completion_date == completion.completion_date
    ).first()
    
    if not db_completion:
        db_completion = Completion(**completion.dict())
        db.add(db_completion)
        db.commit()
        db.refresh(db_completion)
    
    return db_completion

@router.get("/completions/", response_model=List[CompletionResponse])
def read_completions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Completion).offset(skip).limit(limit).all()

@router.get("/completions/habit/{habit_id}")
def get_habit_completions(habit_id: int, db: Session = Depends(get_db)):
    completions = db.query(Completion).filter(Completion.habit_id == habit_id).all()
    return completions

@router.delete("/completions/")
def uncomplete_habit(habit_id: int, completion_date: str, db: Session = Depends(get_db)):
    completion = db.query(Completion).filter(
        Completion.habit_id == habit_id,
        Completion.completion_date == completion_date
    ).first()
    
    if not completion:
        raise HTTPException(status_code=404, detail="Completion not found")
    
    db.delete(completion)
    db.commit()
    return {"message": "Completion removed successfully"}