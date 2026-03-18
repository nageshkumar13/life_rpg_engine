from datetime import date

from pydantic import BaseModel


class TimeSeriesPoint(BaseModel):
    date: date
    value: int | float


class StreakSummary(BaseModel):
    current_streak: int
    best_streak: int


class HabitLeaderboardEntry(BaseModel):
    habit_id: str
    title: str
    total_xp: int
    total_minutes: int
    completion_count: int


class AnalyticsOverview(BaseModel):
    xp_growth: list[TimeSeriesPoint]
    streak_summary: StreakSummary
    planned_completion_ratio: float
    unplanned_completion_ratio: float
    habit_consistency_ratio: float
    total_focus_minutes: int
    task_completion_trend: list[TimeSeriesPoint]
    top_habits: list[HabitLeaderboardEntry]
