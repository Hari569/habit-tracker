from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import habits, completions, analytics, auth
from database import engine
from models import habit, user

# Create tables
habit.Base.metadata.create_all(bind=engine)
user.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Habit Tracker API", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(habits.router, prefix="/api", tags=["habits"])
app.include_router(completions.router, prefix="/api", tags=["completions"])
app.include_router(analytics.router, prefix="/api", tags=["analytics"])
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])

@app.get("/")
def read_root():
    return {"message": "Habit Tracker API", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)