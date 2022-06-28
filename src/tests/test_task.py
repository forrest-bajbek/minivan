import json


def test_post_task(test_app_with_db, test_task_payload):
    response = test_app_with_db.post(
        "/task",
        data=json.dumps(test_task_payload),
    )

    assert response.status_code == 201
    assert response.json()["pk"]


def test_post_task_invalid_json(test_app_with_db, test_task_payload):
    response = test_app_with_db.post("/task", data=json.dumps({}))

    expected_fields = [
        "task_app",
        "task_env",
        "task_name",
        "task_status",
        "task_watermark",
        "task_start_at",
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
    pk = response.json()["pk"]

    response = test_app_with_db.get(f"/task/{pk}")
    assert response.json()["pk"] == pk
    assert response.json()["created_at"]
    assert response.json()["updated_at"]

    for k, v in test_task_payload.items():
        assert response.json()[k] == v


def test_get_task_missing_pk(test_app_with_db):
    response = test_app_with_db.get("/task/notarealpk")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_delete_task(test_app_with_db, test_task_payload):
    response = test_app_with_db.post("/task", data=json.dumps(test_task_payload))
    pk = response.json()["pk"]

    response = test_app_with_db.get(f"/task/{pk}")
    assert response.status_code == 200
    assert response.json()["pk"] == pk

    response = test_app_with_db.delete(f"/task/{pk}")
    assert response.status_code == 200
    assert response.json() == {"pk": pk, "deleted": True}


def test_delete_task_missing_pk(test_app_with_db):
    response = test_app_with_db.delete("/task/notarealpk")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"
