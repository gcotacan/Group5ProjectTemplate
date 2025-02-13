from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import Column, Integer, Float, create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base

# Database setup
DATABASE_URL = "sqlite:///./user_goals.db"  # Replace with actual database URL
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# User Goals Table
class UserGoals(Base):
    __tablename__ = "user_goals"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, nullable=False)
    weight = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    calorie_goal = Column(Integer, nullable=False)

# Create the database tables
Base.metadata.create_all(bind=engine)

# FastAPI instance
app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Request Schema
from pydantic import BaseModel
class UserGoalsCreate(BaseModel):
    user_id: int
    weight: float
    height: float
    calorie_goal: int

# API to Enter User Goals
@app.post("/user-goals/")
def enter_user_goals(goals: UserGoalsCreate, db: Session = Depends(get_db)):
    """Store a user's weight, height, and calorie goal."""
    existing_goal = db.query(UserGoals).filter(UserGoals.user_id == goals.user_id).first()
    
    if existing_goal:
        raise HTTPException(status_code=400, detail="User goals already exist. Use PUT to update.")

    new_goal = UserGoals(**goals.dict())
    db.add(new_goal)
    db.commit()
    db.refresh(new_goal)
    return {"message": "User goals saved successfully!", "user_goals": new_goal}

# API to Retrieve User Goals
@app.get("/user-goals/{user_id}")
def get_user_goals(user_id: int, db: Session = Depends(get_db)):
    """Retrieve a user's stored weight, height, and calorie goal."""
    user_goal = db.query(UserGoals).filter(UserGoals.user_id == user_id).first()
    
    if not user_goal:
        raise HTTPException(status_code=404, detail="User goals not found")

    return user_goal
