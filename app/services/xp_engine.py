from app.utils.math_helpers import clamp


class XPEngine:
    def calculate_task_chunk_xp(self, estimated_minutes: int, importance_score: int, completion_ratio: float = 1.0) -> int:
        base = estimated_minutes * 0.5 + importance_score * 5
        return int(round(base * clamp(completion_ratio, 0.0, 1.0)))

    def calculate_task_completion_bonus(self, estimated_minutes_total: int, importance_score: int) -> int:
        return int(round(estimated_minutes_total * 0.1 + importance_score * 3))

    def calculate_habit_xp(self, base_xp: int, actual_minutes: int, target_minutes: int, streak: int) -> int:
        effort_ratio = 1.0 if target_minutes <= 0 else clamp(actual_minutes / max(target_minutes, 1), 0.25, 1.5)
        streak_multiplier = 1.0 + min(streak, 10) * 0.05
        return int(round(base_xp * effort_ratio * streak_multiplier))

