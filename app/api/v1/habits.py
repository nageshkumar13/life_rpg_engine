from datetime import date

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.habit import HabitCreate, HabitRead, HabitUpdate
from app.schemas.habit_log import HabitLogCreate, HabitLogRead
from app.services.habit_generator_service import HabitGeneratorService
from app.services.habit_service import HabitService


router = APIRouter()


@router.post("", response_model=HabitRead, status_code=status.HTTP_201_CREATED)
def create_habit(payload: HabitCreate, db: Session = Depends(get_db)):
    return HabitService(db).create_habit(payload)


@router.get("", response_model=list[HabitRead])
def list_habits(user_id: str = Query(...), db: Session = Depends(get_db)):
    return HabitService(db).list_habits(user_id)


@router.get("/{habit_id}", response_model=HabitRead)
def get_habit(habit_id: str, db: Session = Depends(get_db)):
    return HabitService(db).get_habit(habit_id)


@router.patch("/{habit_id}", response_model=HabitRead)
def update_habit(habit_id: str, payload: HabitUpdate, db: Session = Depends(get_db)):
    return HabitService(db).update_habit(habit_id, payload)


@router.post("/{habit_id}/deactivate", response_model=HabitRead)
def deactivate_habit(habit_id: str, db: Session = Depends(get_db)):
    return HabitService(db).deactivate_habit(habit_id)


@router.post("/generate", response_model=list[HabitLogRead])
def generate_daily_instances(user_id: str = Query(...), target_date: date = Query(...), db: Session = Depends(get_db)):
    return HabitGeneratorService(db).generate_for_day(user_id, target_date)


@router.post("/{habit_id}/log", response_model=HabitLogRead)
def log_habit_completion(habit_id: str, payload: HabitLogCreate, db: Session = Depends(get_db)):
    return HabitService(db).log_completion(habit_id, payload.log_date, payload.actual_minutes)


@router.post("/{habit_id}/missed", response_model=HabitLogRead)
def mark_habit_missed(habit_id: str, log_date: date = Query(...), db: Session = Depends(get_db)):
    return HabitService(db).mark_missed(habit_id, log_date)

