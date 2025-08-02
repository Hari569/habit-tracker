from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.habit import Habit, Completion
from database import get_db
from datetime import date, timedelta
from typing import Dict, List

router = APIRouter()

@router.get("/analytics/completion-rate")
def get_completion_rate(habit_id: int = None, days: int = 30, db: Session = Depends(get_db)):
    """Get completion rate for habits over the last N days"""
    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    
    query = db.query(Habit)
    if habit_id:
        query = query.filter(Habit.id == habit_id)
    
    habits = query.all()
    analytics = []
    
    for habit in habits:
        # Count expected completions based on repeat frequency
        expected_days = []
        current_date = start_date
        while current_date <= end_date:
            weekday = current_date.strftime("%A").upper()
            if weekday in habit.repeat_frequency:
                expected_days.append(current_date.isoformat())
            current_date += timedelta(days=1)
        
        # Count actual completions
        completions = db.query(Completion).filter(
            Completion.habit_id == habit.id,
            Completion.completion_date >= start_date.isoformat(),
            Completion.completion_date <= end_date.isoformat()
        ).count()
        
        completion_rate = (completions / len(expected_days)) * 100 if expected_days else 0
        
        analytics.append({
            "habit_id": habit.id,
            "habit_name": habit.name,
            "expected_completions": len(expected_days),
            "actual_completions": completions,
            "completion_rate": round(completion_rate, 2)
        })
    
    return analytics

@router.get("/analytics/streaks")
def get_streaks(habit_id: int = None, db: Session = Depends(get_db)):
    """Get current streak for habits"""
    query = db.query(Habit)
    if habit_id:
        query = query.filter(Habit.id == habit_id)
    
    habits = query.all()
    streaks = []
    
    for habit in habits:
        # Get all completions for this habit, ordered by date descending
        completions = db.query(Completion).filter(
            Completion.habit_id == habit.id
        ).order_by(Completion.completion_date.desc()).all()
        
        if not completions:
            streaks.append({
                "habit_id": habit.id,
                "habit_name": habit.name,
                "current_streak": 0,
                "longest_streak": 0
            })
            continue
        
        # Calculate current streak
        current_streak = 0
        current_date = date.today()
        
        for completion in completions:
            completion_date = date.fromisoformat(completion.completion_date)
            if completion_date == current_date:
                current_streak += 1
                current_date -= timedelta(days=1)
            else:
                break
        
        # Calculate longest streak (simplified version)
        longest_streak = current_streak  # This could be more sophisticated
        
        streaks.append({
            "habit_id": habit.id,
            "habit_name": habit.name,
            "current_streak": current_streak,
            "longest_streak": longest_streak
        })
    
    return streaks

@router.get("/analytics/summary")
def get_analytics_summary(db: Session = Depends(get_db)):
    """Get overall analytics summary"""
    total_habits = db.query(Habit).count()
    total_completions = db.query(Completion).count()
    
    # Habits completed today
    today = date.today().isoformat()
    completed_today = db.query(Completion).filter(
        Completion.completion_date == today
    ).count()
    
    return {
        "total_habits": total_habits,
        "total_completions": total_completions,
        "completed_today": completed_today
    }