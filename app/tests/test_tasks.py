from datetime import date


def test_task_chunk_completion_updates_parent_and_logs_xp(client, user):
    task_response = client.post(
        "/api/v1/tasks",
        json={
            "user_id": user.id,
            "title": "Ship task service",
            "type": "PLANNED",
            "importance_score": 4,
            "estimated_minutes_total": 120,
            "assigned_day": date.today().isoformat(),
        },
    )
    task_id = task_response.json()["id"]

    chunk_a = client.post(f"/api/v1/tasks/{task_id}/chunks", json={"title": "Model layer", "estimated_minutes": 45, "order_index": 1})
    chunk_b = client.post(f"/api/v1/tasks/{task_id}/chunks", json={"title": "Service layer", "estimated_minutes": 45, "order_index": 2})

    response = client.post(f"/api/v1/tasks/{task_id}/chunks/{chunk_a.json()['id']}/done")
    assert response.status_code == 200
    assert response.json()["status"] == "ACTIVE"
    assert response.json()["completion_percentage"] == 50.0

    response = client.post(f"/api/v1/tasks/{task_id}/chunks/{chunk_b.json()['id']}/done")
    assert response.status_code == 200
    assert response.json()["status"] == "DONE"
    assert response.json()["completion_percentage"] == 100.0

    xp_response = client.get("/api/v1/xp/logs", params={"user_id": user.id})
    assert xp_response.status_code == 200
    assert len(xp_response.json()["items"]) == 3


def test_done_task_cannot_be_marked_active_again(client, user):
    task_response = client.post(
        "/api/v1/tasks",
        json={
            "user_id": user.id,
            "title": "Close the loop",
            "type": "PLANNED",
            "importance_score": 3,
            "estimated_minutes_total": 30,
            "assigned_day": date.today().isoformat(),
        },
    )
    task_id = task_response.json()["id"]

    done_response = client.post(f"/api/v1/tasks/{task_id}/done")
    assert done_response.status_code == 200

    invalid_response = client.post(f"/api/v1/tasks/{task_id}/active")
    assert invalid_response.status_code == 400
