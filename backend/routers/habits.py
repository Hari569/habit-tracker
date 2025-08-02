from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.habit import Habit
from database import get_db
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

router = APIRouter()

class HabitCreate(BaseModel):
    name: str
    repeat_frequency: str  # "MONDAY,TUESDAY,..."
    tags: Optional[str] = None
    user_id: int = 1

class HabitResponse(BaseModel):
    id: int
    name: str
    repeat_frequency: str
    tags: Optional[str]
    user_id: int

    class Config:
        from_attributes = True

class HabitUpdate(BaseModel):
    name: Optional[str] = None
    repeat_frequency: Optional[str] = None
    tags: Optional[str] = None

@router.post("/habits/", response_model=HabitResponse)
def create_habit(habit: HabitCreate, db: Session = Depends(get_db)):
    db_habit = Habit(**habit.dict())
    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)
    return db_habit

@router.get("/habits/", response_model=List[HabitResponse])
def read_habits(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Habit).offset(skip).limit(limit).all()

@router.get("/habits/{habit_id}", response_model=HabitResponse)
def read_habit(habit_id: int, db: Session = Depends(get_db)):
    habit = db.query(Habit).filter(Habit.id == habit_id).first()
    if habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit

@router.put("/habits/{habit_id}", response_model=HabitResponse)
def update_habit(habit_id: int, habit_update: HabitUpdate, db: Session = Depends(get_db)):
    habit = db.query(Habit).filter(Habit.id == habit_id).first()
    if habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    for field, value in habit_update.dict(exclude_unset=True).items():
        setattr(habit, field, value)
    
    db.commit()
    db.refresh(habit)
    return habit

@router.delete("/habits/{habit_id}")
def delete_habit(habit_id: int, db: Session = Depends(get_db)):
    habit = db.query(Habit).filter(Habit.id == habit_id).first()
    if habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    db.delete(habit)
    db.commit()
    return {"message": "Habit deleted successfully"}

@router.get("/habits/date/{target_date}")
def get_habits_for_date(target_date: str, db: Session = Depends(get_db)):
    """Get habits scheduled for a specific date"""
    try:
        date_obj = date.fromisoformat(target_date)
        weekday = date_obj.strftime("%A").upper()
        
        habits = db.query(Habit).all()
        habits_for_date = []
        
        for habit in habits:
            if weekday in habit.repeat_frequency:
                habits_for_date.append(habit)
        
        return habits_for_date
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")