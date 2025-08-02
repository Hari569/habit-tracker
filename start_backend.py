#!/usr/bin/env python3
"""
Startup script for the Habit Tracker backend
"""
import os
import sys
import sqlite3
from pathlib import Path

def create_database():
    """Create the database and tables if they don't exist"""
    db_path = "habits.db"
    # Create database connection
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create habits table (compatible with existing structure)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            repeat_frequency TEXT NOT NULL,
            tags TEXT,
            user_id INTEGER DEFAULT 1
        )
    ''')
    
    # Create completions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS completions (
            habit_id INTEGER,
            completion_date TEXT,
            PRIMARY KEY (habit_id, completion_date),
            FOREIGN KEY (habit_id) REFERENCES habits (id)
        )
    ''')
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            full_name TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Database created successfully!")

def main():
    print("🚀 Starting Habit Tracker Backend...")
    
    # Check if we're in the right directory
    if not Path("backend").exists():
        print("❌ Error: backend directory not found. Please run this script from the project root.")
        sys.exit(1)
    
    # Create database
    create_database()
    
    # Add backend directory to Python path
    backend_path = Path("backend").resolve()
    sys.path.insert(0, str(backend_path))
    
    # Start the server
    print("🌟 Starting FastAPI server on http://localhost:8000")
    print("📖 API docs available at http://localhost:8000/docs")
    
    # Import and run
    try:
        import uvicorn
        # Run from the backend directory but with correct module path
        uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True, reload_dirs=["backend"])
    except ImportError:
        print("❌ Error: uvicorn not installed. Please run: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()