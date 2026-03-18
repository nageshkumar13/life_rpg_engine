from datetime import date

from sqlalchemy.orm import Session

from app.core.enums import HabitLogStatus, XPSourceType
from app.core.exceptions import NotFoundError
from app.models.habit import Habit
from app.models.habit_log import HabitLog
from app.repositories.habit_log_repository import HabitLogRepository
from app.repositories.habit_repository import HabitRepository
from app.repositories.user_repository import UserRepository
from app.schemas.habit import HabitCreate, HabitUpdate
from app.services.streak_service import StreakService
from app.services.xp_engine import XPEngine
from app.services.xp_service import XPService
from app.utils.ids import new_id


class HabitService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.habit_repository = HabitRepository(db)
        self.log_repository = HabitLogRepository(db)
        self.user_repository = UserRepository(db)
        self.streak_service = StreakService()
        self.engine = XPEngine()
        self.xp_service = XPService(db)

    def create_habit(self, payload: HabitCreate) -> Habit:
        habit = Habit(id=new_id(), **payload.model_dump())
        self.habit_repository.create(habit)
        self.db.commit()
        self.db.refresh(habit)
        return habit

    def list_habits(self, user_id: str) -> list[Habit]:
        return self.habit_repository.list_for_user(user_id)

    def get_habit(self, habit_id: str) -> Habit:
        habit = self.habit_repository.get(habit_id)
        if not habit:
            raise NotFoundError("Habit not found")
        return habit

    def update_habit(self, habit_id: str, payload: HabitUpdate) -> Habit:
        habit = self.get_habit(habit_id)
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(habit, field, value)
        self.db.add(habit)
        self.db.commit()
        self.db.refresh(habit)
        return habit

    def deactivate_habit(self, habit_id: str) -> Habit:
        habit = self.get_habit(habit_id)
        habit.is_active = False
        self.db.add(habit)
        self.db.commit()
        self.db.refresh(habit)
        return habit

    def log_completion(self, habit_id: str, log_date: date, actual_minutes: int) -> HabitLog:
        habit = self.get_habit(habit_id)
        log = self.log_repository.get_for_day(habit.id, log_date)
        if not log:
            log = HabitLog(id=new_id(), habit_id=habit.id, user_id=habit.user_id, log_date=log_date)
            self.log_repository.create(log)

        user = self.user_repository.get(habit.user_id)
        if not user:
            raise NotFoundError("User not found")

        current_streak, _ = self.streak_service.apply_habit_log(user, HabitLogStatus.COMPLETED)
        xp = self.engine.calculate_habit_xp(habit.xp_base, actual_minutes, habit.target_minutes, current_streak)

        log.actual_minutes = actual_minutes
        log.status = HabitLogStatus.COMPLETED
        log.streak_after_log = current_streak
        log.xp_earned = xp

        self.db.add(log)
        self.db.add(user)
        self.xp_service.grant_xp(
            user_id=habit.user_id,
            source_type=XPSourceType.HABIT_LOG,
            source_id=log.id,
            xp_delta=xp,
            reason=f"Completed habit '{habit.title}'",
        )
        self.db.commit()
        self.db.refresh(log)
        return log

    def mark_missed(self, habit_id: str, log_date: date) -> HabitLog:
        habit = self.get_habit(habit_id)
        log = self.log_repository.get_for_day(habit.id, log_date)
        if not log:
            log = HabitLog(id=new_id(), habit_id=habit.id, user_id=habit.user_id, log_date=log_date)
            self.log_repository.create(log)

        user = self.user_repository.get(habit.user_id)
        if not user:
            raise NotFoundError("User not found")
        current_streak, _ = self.streak_service.apply_habit_log(user, HabitLogStatus.MISSED)

        log.status = HabitLogStatus.MISSED
        log.actual_minutes = 0
        log.streak_after_log = current_streak
        self.db.add(log)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(log)
        return log

