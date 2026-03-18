from app.services.xp_engine import XPEngine


def test_xp_engine_returns_positive_values():
    engine = XPEngine()
    assert engine.calculate_task_chunk_xp(estimated_minutes=30, importance_score=3) > 0
    assert engine.calculate_task_completion_bonus(estimated_minutes_total=90, importance_score=4) > 0
    assert engine.calculate_habit_xp(base_xp=20, actual_minutes=30, target_minutes=30, streak=3) > 20

