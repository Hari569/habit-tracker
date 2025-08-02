from langchain_core.tools import tool
from langchain_core.pydantic_v1 import BaseModel, Field
from datetime import date
from typing import Set, List, Optional
from enum import Enum, auto
import sqlite3

class DayOfWeek(Enum):
    MONDAY = auto()
    TUESDAY = auto()
    WEDNESDAY = auto()
    THURSDAY = auto()
    FRIDAY = auto()
    SATURDAY = auto()
    SUNDAY = auto()

DB_NAME = "habits.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

class CompleteHabitParams(BaseModel):
    habit_id: int = Field(description="Id (number) of the habit e.g. 2")
    day: int = Field(description="Day of the month (1-31) e.g. 18")
    month: int = Field(description="Month of the year (1-12) e.g. 3")
    year: int = Field(description="Year for which to complete the habit e.g. 2024")

@tool(args_schema=CompleteHabitParams)
def complete_habit_tool(habit_id: int, day: int, month: int, year: int):
    """Completes a habit for a specific date"""
    completion_date = date(year, month, day)
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO completions (habit_id, completion_date)
            VALUES (?, ?)
        """,
            (habit_id, completion_date.isoformat()),
        )
        conn.commit()
    return f"Habit {habit_id} completed for {completion_date}"

class HabitsForDateParams(BaseModel):
    day: int = Field(description="Day of the month (1-31) e.g. 18")
    month: int = Field(description="Month of the year (1-12) e.g. 3")
    year: int = Field(description="Year for which to get habits e.g. 2024")

@tool(args_schema=HabitsForDateParams)
def habits_for_date_tool(day: int, month: int, year: int):
    """Returns a list of habits for a given date"""
    target_date = date(year, month, day)
    weekday = DayOfWeek(target_date.weekday() + 1).name
    
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT h.id, h.name, h.tags, c.completion_date IS NOT NULL as completed
            FROM habits h
            LEFT JOIN completions c ON h.id = c.habit_id AND c.completion_date = ?
            WHERE instr(h.repeat_frequency, ?) > 0
        """,
            (target_date.isoformat(), weekday),
        )
        results = cursor.fetchall()
        
    habits = []
    for habit_id, name, tags, completed in results:
        habits.append({
            "id": habit_id,
            "name": name,
            "tags": tags.split(",") if tags else [],
            "completed": bool(completed)
        })
    
    return habits

class AddHabitParams(BaseModel):
    name: str = Field(description="Name of the habit")
    repeat_frequency: Set[DayOfWeek] = Field(
        description="Which days of the week the habit should repeat"
    )
    tags: Optional[List[str]] = Field(
        description="Optional list of tags for this habit"
    )

@tool(args_schema=AddHabitParams)
def add_habit_tool(
    name: str, repeat_frequency: Set[DayOfWeek], tags: List[str] = []
) -> int:
    """Adds a new habit with specific repeat frequency. Returns the ID of the habit."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO habits (name, repeat_frequency, tags)
            VALUES (?, ?, ?)
        """,
            (name, ",".join(day.name for day in repeat_frequency), ",".join(tags)),
        )
        conn.commit()
        return cursor.lastrowid

class DeleteHabitParams(BaseModel):
    habit_id: int = Field(description="Id of the habit to delete")

@tool(args_schema=DeleteHabitParams)
def delete_habit_tool(habit_id: int):
    """Deletes a habit by its ID"""
    with get_connection() as conn:
        cursor = conn.cursor()
        # Delete completions first
        cursor.execute("DELETE FROM completions WHERE habit_id = ?", (habit_id,))
        # Delete habit
        cursor.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
        conn.commit()
    return f"Habit {habit_id} deleted successfully"

# Export all tools
tools = [complete_habit_tool, habits_for_date_tool, add_habit_tool, delete_habit_tool]