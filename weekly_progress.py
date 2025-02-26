from sqlalchemy import Column, Integer, Float, DateTime, String, Boolean, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

class WeeklyProgress(Base):
    __tablename__ = "weekly_progress"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
    calories_consumed = Column(Integer)
    activity_level = Column(String)
    goal_met = Column(Boolean, default=False)
    water_intake = Column(Float, nullable=True)  # in liters
    weight = Column(Float, nullable=True)  # for tracking weight changes

# Create tables
engine = create_engine("sqlite:///./fitness_tracker.db", connect_args={"check_same_thread": False})
Base.metadata.create_all(bind=engine) 