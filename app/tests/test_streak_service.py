from app.core.enums import HabitLogStatus
from app.models.user import User
from app.services.streak_service import StreakService


def test_streak_service_updates_current_and_best_streak():
    service = StreakService()
    user = User(id="u1", email="u1@example.com")

    current, best = service.apply_habit_log(user, HabitLogStatus.COMPLETED)
    assert current == 1
    assert best == 1

    current, best = service.apply_habit_log(user, HabitLogStatus.COMPLETED)
    assert current == 2
    assert best == 2

    current, best = service.apply_habit_log(user, HabitLogStatus.MISSED)
    assert current == 0
    assert best == 2

