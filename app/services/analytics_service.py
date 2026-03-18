from collections import defaultdict
from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.enums import HabitLogStatus, TaskStatus, TaskType
from app.core.exceptions import NotFoundError
from app.models.habit import Habit
from app.models.habit_log import HabitLog
from app.models.task import Task
from app.models.xp_log import XPLog
from app.repositories.user_repository import UserRepository
from app.schemas.analytics import AnalyticsOverview, HabitLeaderboardEntry, StreakSummary, TimeSeriesPoint


class AnalyticsService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.user_repository = UserRepository(db)

    def overview(self, user_id: str) -> AnalyticsOverview:
        user = self.user_repository.get(user_id)
        if not user:
            raise NotFoundError("User not found")

        planned_total = self._count_tasks(user_id, TaskType.PLANNED)
        planned_done = self._count_tasks(user_id, TaskType.PLANNED, TaskStatus.DONE)
        unplanned_total = self._count_tasks(user_id, TaskType.UNPLANNED)
        unplanned_done = self._count_tasks(user_id, TaskType.UNPLANNED, TaskStatus.DONE)
        habit_total = self._count_habits(user_id)
        habit_done = self._count_habits(user_id, HabitLogStatus.COMPLETED)

        focus_stmt = select(func.coalesce(func.sum(HabitLog.actual_minutes), 0)).where(HabitLog.user_id == user_id)
        total_focus_minutes = int(self.db.scalar(focus_stmt) or 0)

        return AnalyticsOverview(
            xp_growth=self._xp_growth(user_id),
            streak_summary=StreakSummary(current_streak=user.current_streak, best_streak=user.best_streak),
            planned_completion_ratio=(planned_done / planned_total) if planned_total else 0.0,
            unplanned_completion_ratio=(unplanned_done / unplanned_total) if unplanned_total else 0.0,
            habit_consistency_ratio=(habit_done / habit_total) if habit_total else 0.0,
            total_focus_minutes=total_focus_minutes,
            task_completion_trend=self._task_completion_trend(user_id),
            top_habits=self._top_habits(user_id),
        )

    def _xp_growth(self, user_id: str) -> list[TimeSeriesPoint]:
        rows = list(self.db.scalars(select(XPLog).where(XPLog.user_id == user_id).order_by(XPLog.created_at.asc())).all())
        by_day: dict[date, int] = defaultdict(int)
        for row in rows:
            by_day[row.created_at.date()] += row.xp_delta
        return [TimeSeriesPoint(date=day, value=value) for day, value in sorted(by_day.items())]

    def _task_completion_trend(self, user_id: str) -> list[TimeSeriesPoint]:
        rows = list(self.db.scalars(select(Task).where(Task.user_id == user_id, Task.assigned_day.is_not(None))).all())
        by_day: dict[date, int] = defaultdict(int)
        for row in rows:
            if row.status == TaskStatus.DONE and row.assigned_day:
                by_day[row.assigned_day] += 1
        return [TimeSeriesPoint(date=day, value=value) for day, value in sorted(by_day.items())]

    def _top_habits(self, user_id: str) -> list[HabitLeaderboardEntry]:
        habits = list(self.db.scalars(select(Habit).where(Habit.user_id == user_id)).all())
        ranking: list[HabitLeaderboardEntry] = []
        for habit in habits:
            logs = list(self.db.scalars(select(HabitLog).where(HabitLog.habit_id == habit.id)).all())
            ranking.append(
                HabitLeaderboardEntry(
                    habit_id=habit.id,
                    title=habit.title,
                    total_xp=sum(log.xp_earned for log in logs),
                    total_minutes=sum(log.actual_minutes for log in logs),
                    completion_count=sum(1 for log in logs if log.status == HabitLogStatus.COMPLETED),
                )
            )
        ranking.sort(key=lambda item: item.total_xp, reverse=True)
        return ranking[:5]

    def _count_tasks(self, user_id: str, task_type: TaskType, status: TaskStatus | None = None) -> int:
        stmt = select(func.count(Task.id)).where(Task.user_id == user_id, Task.type == task_type)
        if status:
            stmt = stmt.where(Task.status == status)
        return int(self.db.scalar(stmt) or 0)

    def _count_habits(self, user_id: str, status: HabitLogStatus | None = None) -> int:
        stmt = select(func.count(HabitLog.id)).where(HabitLog.user_id == user_id)
        if status:
            stmt = stmt.where(HabitLog.status == status)
        return int(self.db.scalar(stmt) or 0)
