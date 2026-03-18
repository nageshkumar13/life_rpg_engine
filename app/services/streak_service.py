from app.core.enums import HabitLogStatus
from app.models.user import User


class StreakService:
    def apply_habit_log(self, user: User, status: HabitLogStatus) -> tuple[int, int]:
        if status == HabitLogStatus.COMPLETED:
            user.current_streak += 1
            user.best_streak = max(user.best_streak, user.current_streak)
        elif status == HabitLogStatus.MISSED:
            user.current_streak = 0
        return user.current_streak, user.best_streak

