from datetime import date


def test_habit_completion_updates_streak_and_xp(client, user):
    habit_response = client.post(
        "/api/v1/habits",
        json={
            "user_id": user.id,
            "title": "Workout",
            "target_minutes": 30,
            "xp_base": 20,
        },
    )
    habit_id = habit_response.json()["id"]

    generate_response = client.post(
        "/api/v1/habits/generate",
        params={"user_id": user.id, "target_date": date.today().isoformat()},
    )
    assert generate_response.status_code == 200
    assert len(generate_response.json()) == 1

    log_response = client.post(
        f"/api/v1/habits/{habit_id}/log",
        json={"log_date": date.today().isoformat(), "actual_minutes": 30},
    )
    assert log_response.status_code == 200
    assert log_response.json()["status"] == "COMPLETED"
    assert log_response.json()["streak_after_log"] == 1

    users_response = client.get("/api/v1/users")
    assert users_response.json()[0]["current_streak"] == 1


def test_habit_completion_is_idempotent_for_same_day(client, user):
    habit_response = client.post(
        "/api/v1/habits",
        json={
            "user_id": user.id,
            "title": "Read",
            "target_minutes": 20,
            "xp_base": 15,
        },
    )
    habit_id = habit_response.json()["id"]

    first = client.post(
        f"/api/v1/habits/{habit_id}/log",
        json={"log_date": date.today().isoformat(), "actual_minutes": 20},
    )
    second = client.post(
        f"/api/v1/habits/{habit_id}/log",
        json={"log_date": date.today().isoformat(), "actual_minutes": 20},
    )

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["id"] == second.json()["id"]

    xp_response = client.get("/api/v1/xp/logs", params={"user_id": user.id})
    assert len(xp_response.json()["items"]) == 1
