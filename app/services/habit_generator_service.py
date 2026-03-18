from datetime import date

from sqlalchemy.orm import Session

from app.core.enums import HabitLogStatus
from app.models.habit_log import HabitLog
from app.repositories.habit_log_repository import HabitLogRepository
from app.repositories.habit_repository import HabitRepository
from app.utils.ids import new_id


class HabitGeneratorService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.habit_repository = HabitRepository(db)
        self.log_repository = HabitLogRepository(db)

    def generate_for_day(self, user_id: str, day: date) -> list[HabitLog]:
        habits = self.habit_repository.list_for_user(user_id, active_only=True)
        logs: list[HabitLog] = []
        for habit in habits:
            existing = self.log_repository.get_for_day(habit.id, day)
            if existing:
                logs.append(existing)
                continue
            log = HabitLog(
                id=new_id(),
                habit_id=habit.id,
                user_id=user_id,
                log_date=day,
                status=HabitLogStatus.EXPECTED,
            )
            self.log_repository.create(log)
            logs.append(log)
        self.db.commit()
        return logs

