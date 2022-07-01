import json


def test_post_task(test_app_with_db, test_user_access_token_write):
    payload = {
        "task_app": "Tornado",
        "task_env": "dev",
        "task_name": "Chase the Egg Carrier",
        "task_status": "complete",
        "task_watermark": "2022-06-27T00:00:00+00:00",
        "task_duration": 120.54,
        "task_metadata": {"score": 152113, "rank": "A"},
    }
    response = test_app_with_db.post(
        "/task",
        data=json.dumps(payload),
        headers={"Authorization": f"Bearer {test_user_access_token_write}"},
    )
    assert response.status_code == 201
    assert response.json()["id"]


def test_post_task_invalid_json(test_app_with_db, test_user_access_token_write):
    response = test_app_with_db.post(
        "/task",
        data=json.dumps({}),
        headers={"Authorization": f"Bearer {test_user_access_token_write}"},
    )

    expected_fields = [
        "task_app",
        "task_env",
        "task_name",
        "task_status",
        "task_watermark",
    ]

    expected_json = {
        "detail": [
            {
                "loc": ["body", field],
                "msg": "field required",
                "type": "value_error.missing",
            }
            for field in expected_fields
        ]
    }

    assert response.status_code == 422
    assert response.json() == expected_json


def test_get_task(test_app_with_db, test_user_access_token_write):
    # Post a Task
    payload = {
        "task_app": "Tornado",
        "task_env": "dev",
        "task_name": "Chase the Egg Carrier",
        "task_status": "complete",
        "task_watermark": "2022-06-27T00:00:00+00:00",
        "task_duration": 120.54,
        "task_metadata": {"score": 152113, "rank": "A"},
    }
    response = test_app_with_db.post(
        "/task",
        data=json.dumps(payload),
        headers={"Authorization": f"Bearer {test_user_access_token_write}"},
    )
    assert response.status_code == 201
    assert response.json()["id"]

    id = response.json()["id"]

    # Get the Task that was posted
    response = test_app_with_db.get(
        f"/task/{id}",
        headers={"Authorization": f"Bearer {test_user_access_token_write}"},
    )
    assert response.json()["id"] == id
    assert response.json()["created_at"]
    assert response.json()["updated_at"]
    for k, v in payload.items():
        assert response.json()[k] == v


def test_get_task_missing_id(test_app_with_db, test_user_access_token_read):
    response = test_app_with_db.get(
        "/task/99999999",
        headers={"Authorization": f"Bearer {test_user_access_token_read}"},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_get_task_invalid_id(test_app_with_db, test_user_access_token_read):
    response = test_app_with_db.get(
        "/task/0",
        headers={"Authorization": f"Bearer {test_user_access_token_read}"},
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["path", "id"],
                "msg": "ensure this value is greater than 0",
                "type": "value_error.number.not_gt",
                "ctx": {"limit_value": 0},
            }
        ]
    }


def test_delete_task(test_app_with_db, test_user_access_token_write):
    # Post a Task
    payload = {
        "task_app": "Tornado",
        "task_env": "dev",
        "task_name": "Chase the Egg Carrier",
        "task_status": "complete",
        "task_watermark": "2022-06-27T00:00:00+00:00",
        "task_duration": 120.54,
        "task_metadata": {"score": 152113, "rank": "A"},
    }
    response = test_app_with_db.post(
        "/task",
        data=json.dumps(payload),
        headers={"Authorization": f"Bearer {test_user_access_token_write}"},
    )
    assert response.status_code == 201
    assert response.json()["id"]

    id = response.json()["id"]

    response = test_app_with_db.delete(
        f"/task/{id}",
        headers={"Authorization": f"Bearer {test_user_access_token_write}"},
    )
    assert response.status_code == 200
    assert response.json() == {"deleted": True}


def test_delete_task_missing_id(test_app_with_db, test_user_access_token_write):
    response = test_app_with_db.delete(
        "/task/999999",
        data=json.dumps({}),
        headers={"Authorization": f"Bearer {test_user_access_token_write}"},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_delete_task_invalid_id(test_app_with_db, test_user_access_token_write):
    response = test_app_with_db.delete(
        "/task/0",
        data=json.dumps({}),
        headers={"Authorization": f"Bearer {test_user_access_token_write}"},
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["path", "id"],
                "msg": "ensure this value is greater than 0",
                "type": "value_error.number.not_gt",
                "ctx": {"limit_value": 0},
            }
        ]
    }
