from datetime import date

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.common import MessageResponse
from app.schemas.habit import HabitCreate, HabitRead, HabitUpdate
from app.schemas.habit_log import HabitLogCreate, HabitLogRead
from app.services.habit_generator_service import HabitGeneratorService
from app.services.habit_service import HabitService


router = APIRouter()


@router.post("", response_model=HabitRead, status_code=status.HTTP_201_CREATED)
def create_habit(payload: HabitCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return HabitService(db).create_habit(payload.model_copy(update={"user_id": current_user.id}))


@router.get("", response_model=list[HabitRead])
def list_habits(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return HabitService(db).list_habits(current_user.id)


@router.get("/{habit_id}", response_model=HabitRead)
def get_habit(habit_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return HabitService(db).get_habit(current_user.id, habit_id)


@router.patch("/{habit_id}", response_model=HabitRead)
def update_habit(habit_id: str, payload: HabitUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return HabitService(db).update_habit(current_user.id, habit_id, payload)


@router.post("/{habit_id}/deactivate", response_model=HabitRead)
def deactivate_habit(habit_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return HabitService(db).deactivate_habit(current_user.id, habit_id)


@router.delete("/{habit_id}", response_model=MessageResponse)
def delete_habit(habit_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    HabitService(db).delete_habit(current_user.id, habit_id)
    return MessageResponse(message="Habit deleted")


@router.post("/generate", response_model=list[HabitLogRead])
def generate_daily_instances(target_date: date = Query(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return HabitGeneratorService(db).generate_for_day(current_user.id, target_date)


@router.post("/{habit_id}/log", response_model=HabitLogRead)
def log_habit_completion(habit_id: str, payload: HabitLogCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return HabitService(db).log_completion(current_user.id, habit_id, payload.log_date, payload.actual_minutes)


@router.post("/{habit_id}/missed", response_model=HabitLogRead)
def mark_habit_missed(habit_id: str, log_date: date = Query(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return HabitService(db).mark_missed(current_user.id, habit_id, log_date)
