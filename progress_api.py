from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List
import statistics

app = FastAPI()

# Progress tracking endpoints
@app.post("/weekly-progress/")
async def log_daily_progress(
    user_id: int,
    calories: int,
    activity_level: str,
    water_intake: float = None,
    weight: float = None,
    db: Session = Depends(get_db)
):
    today = datetime.now().date()
    
    # Check if entry exists for today
    existing_entry = db.query(WeeklyProgress).filter(
        WeeklyProgress.user_id == user_id,
        func.date(WeeklyProgress.date) == today
    ).first()
    
    if existing_entry:
        existing_entry.calories_consumed = calories
        existing_entry.activity_level = activity_level
        existing_entry.water_intake = water_intake
        existing_entry.weight = weight
    else:
        new_entry = WeeklyProgress(
            user_id=user_id,
            date=today,
            calories_consumed=calories,
            activity_level=activity_level,
            water_intake=water_intake,
            weight=weight
        )
        db.add(new_entry)
    
    db.commit()
    return {"message": "Progress logged successfully"}

@app.get("/weekly-progress/{user_id}")
async def get_weekly_progress(user_id: int, db: Session = Depends(get_db)):
    # Get last 7 days of progress
    week_ago = datetime.now().date() - timedelta(days=7)
    progress = db.query(WeeklyProgress).filter(
        WeeklyProgress.user_id == user_id,
        WeeklyProgress.date >= week_ago
    ).all()
    
    # Calculate weekly stats
    calories_list = [p.calories_consumed for p in progress if p.calories_consumed]
    weekly_stats = {
        "avg_calories": statistics.mean(calories_list) if calories_list else 0,
        "daily_records": [
            {
                "date": p.date.strftime("%Y-%m-%d"),
                "calories": p.calories_consumed,
                "activity": p.activity_level,
                "water": p.water_intake,
                "weight": p.weight
            }
            for p in progress
        ]
    }
    
    return weekly_stats 