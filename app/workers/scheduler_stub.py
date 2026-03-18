from app.workers.daily_reset_worker import run_daily_reset


def nightly_job(user_id: str) -> None:
    run_daily_reset(user_id)
