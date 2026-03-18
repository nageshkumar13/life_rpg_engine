from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.enums import HabitLogStatus, TaskStatus, TaskType
from app.core.exceptions import ConflictError
from app.models.daily_review import DailyReview
from app.models.habit_log import HabitLog
from app.models.task import Task
from app.repositories.review_repository import ReviewRepository
from app.repositories.xp_repository import XPRepository
from app.utils.ids import new_id


class DailyReviewService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.review_repository = ReviewRepository(db)
        self.xp_repository = XPRepository(db)

    def create_review(self, user_id: str, review_date: date, remark: str | None = None) -> DailyReview:
        existing = self.review_repository.get_for_day(user_id, review_date)
        if existing:
            raise ConflictError("Daily review already exists for this date")

        planned_total = self._count_tasks(user_id, review_date, TaskType.PLANNED)
        planned_completed = self._count_tasks(user_id, review_date, TaskType.PLANNED, TaskStatus.DONE)
        unplanned_completed = self._count_tasks(user_id, review_date, TaskType.UNPLANNED, TaskStatus.DONE)
        habit_completed = self._count_habits(user_id, review_date, HabitLogStatus.COMPLETED)
        habit_expected = self._count_habits(user_id, review_date)
        xp_earned = self.xp_repository.total_for_day(user_id, review_date)

        discipline = int(round((planned_completed / planned_total) * 100)) if planned_total else 0
        productivity_total = planned_total + unplanned_completed
        productivity = int(round(((planned_completed + unplanned_completed) / productivity_total) * 100)) if productivity_total else 0
        habit_score = int(round((habit_completed / habit_expected) * 100)) if habit_expected else 0

        review = DailyReview(
            id=new_id(),
            user_id=user_id,
            review_date=review_date,
            discipline_score=discipline,
            productivity_score=productivity,
            habit_score=habit_score,
            xp_earned=xp_earned,
            planned_completed=planned_completed,
            planned_total=planned_total,
            unplanned_completed=unplanned_completed,
            habit_completed=habit_completed,
            remark=remark,
        )
        self.review_repository.create(review)
        self.db.commit()
        self.db.refresh(review)
        return review

    def list_reviews(self, user_id: str) -> list[DailyReview]:
        return self.review_repository.list_for_user(user_id)

    def freeze_day(self, user_id: str, target_date: date) -> DailyReview:
        tasks = list(
            self.db.scalars(
                select(Task).where(
                    Task.user_id == user_id,
                    Task.assigned_day == target_date,
                    Task.type.in_([TaskType.PLANNED, TaskType.HABIT_INSTANCE]),
                    Task.status.in_([TaskStatus.PLANNED, TaskStatus.ACTIVE]),
                )
            ).all()
        )
        for task in tasks:
            task.status = TaskStatus.MISSED
            self.db.add(task)

        logs = list(
            self.db.scalars(
                select(HabitLog).where(
                    HabitLog.user_id == user_id,
                    HabitLog.log_date == target_date,
                    HabitLog.status == HabitLogStatus.EXPECTED,
                )
            ).all()
        )
        for log in logs:
            log.status = HabitLogStatus.MISSED
            self.db.add(log)

        self.db.flush()
        return self.create_review(user_id, target_date, "Frozen nightly snapshot")

    def _count_tasks(self, user_id: str, target_date: date, task_type: TaskType, status: TaskStatus | None = None) -> int:
        stmt = select(func.count(Task.id)).where(Task.user_id == user_id, Task.assigned_day == target_date, Task.type == task_type)
        if status:
            stmt = stmt.where(Task.status == status)
        return int(self.db.scalar(stmt) or 0)

    def _count_habits(self, user_id: str, target_date: date, status: HabitLogStatus | None = None) -> int:
        stmt = select(func.count(HabitLog.id)).where(HabitLog.user_id == user_id, HabitLog.log_date == target_date)
        if status:
            stmt = stmt.where(HabitLog.status == status)
        return int(self.db.scalar(stmt) or 0)

