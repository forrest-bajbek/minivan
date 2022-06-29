import json


def test_post_task(test_app_with_db, test_task_payload):
    response = test_app_with_db.post(
        "/task",
        data=json.dumps(test_task_payload),
    )

    assert response.status_code == 201
    assert response.json()["id"]


def test_post_task_invalid_json(test_app_with_db):
    response = test_app_with_db.post("/task", data=json.dumps({}))

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


def test_get_task(test_app_with_db, test_task_payload):
    response = test_app_with_db.post("/task", data=json.dumps(test_task_payload))
    id = response.json()["id"]

    response = test_app_with_db.get(f"/task/{id}")
    assert response.json()["id"] == id
    assert response.json()["created_at"]
    assert response.json()["updated_at"]
    for k, v in test_task_payload.items():
        assert response.json()[k] == v


def test_get_task_missing_id(test_app_with_db):
    response = test_app_with_db.get("/task/99999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_get_task_invalid_id(test_app_with_db):
    response = test_app_with_db.get("/task/0")
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


def test_delete_task(test_app_with_db, test_task_payload):
    response = test_app_with_db.post("/task", data=json.dumps(test_task_payload))
    id = response.json()["id"]

    response = test_app_with_db.get(f"/task/{id}")
    assert response.status_code == 200
    assert response.json()["id"] == id

    response = test_app_with_db.delete(f"/task/{id}")
    assert response.status_code == 200
    assert response.json() == {"id": id, "deleted": True}


def test_delete_task_missing_id(test_app_with_db):
    response = test_app_with_db.delete("/task/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_delete_task_invalid_id(test_app_with_db):
    response = test_app_with_db.delete("/task/0")
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
