from datetime import date


def test_backlog_assignment_creates_task(client, user):
    backlog_response = client.post(
        "/api/v1/backlog",
        json={
            "user_id": user.id,
            "title": "Plan quarterly engine",
            "importance_score": 5,
            "estimated_effort": 180,
            "xp_reward": 100,
        },
    )
    backlog_id = backlog_response.json()["id"]

    assign_response = client.post(
        f"/api/v1/backlog/{backlog_id}/assign",
        json={"assigned_day": date.today().isoformat()},
    )
    assert assign_response.status_code == 200
    body = assign_response.json()
    assert body["backlog"]["status"] == "ASSIGNED"
    assert body["task"]["source_backlog_id"] == backlog_id

