from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, FoodEntry, Food
from pydantic import BaseModel

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Request Schema for Editing a Food Entry
class FoodEntryUpdate(BaseModel):
    amount_eaten: float  # New amount eaten

# API Endpoint to Edit a Food Log Entry
@app.put("/food-log/{entry_id}")
def edit_food_entry(entry_id: int, update_data: FoodEntryUpdate, db: Session = Depends(get_db)):
    """Modify an existing food entry in the database."""
    food_entry = db.query(FoodEntry).filter(FoodEntry.id == entry_id).first()

    if not food_entry:
        raise HTTPException(status_code=404, detail="Food entry not found")

    # Update the amount eaten and recalculate total calories
    food = db.query(Food).filter(Food.id == food_entry.food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")

    food_entry.amount_eaten = update_data.amount_eaten
    food_entry.total_calories = update_data.amount_eaten * food.calories_per_serving

    db.commit()
    db.refresh(food_entry)

    return {"message": "Food entry updated successfully", "updated_entry": food_entry}
