import json


def test_post_task(test_app_with_db):
    response = test_app_with_db.post(
        "/task",
        data=json.dumps(
            {
                "task_app": "test_app",
                "task_env": "dev",
                "task_name": "test_name",
                "task_status": "success",
                "task_watermark": "2022-06-01 00:00:00+00:00",
                "task_start_at": "2022-06-01 01:00:00+00:00",
                "task_stop_at": "2022-06-01 02:00:00+00:00",
                "task_metadata": {"key": "value", "some": ["list", "of", "items"]},
            }
        ),
    )

    assert response.status_code == 201
    assert response.json()["pk"]


# def test_get_task(test_app_with_db):
#     response = test_app_with_db.post(
#         "/task",
#         data=json.dumps(
#             {
#                 "task_app": "test_app",
#                 "task_env": "dev",
#                 "task_name": "test_name",
#                 "task_status": "success",
#                 "task_watermark": "2022-06-01 00:00:00+00:00",
#                 "task_start_at": "2022-06-01 01:00:00+00:00",
#                 "task_stop_at": "2022-06-01 02:00:00+00:00",
#                 "task_metadata": {"key": "value", "some": ["list", "of", "items"]},
#             }
#         ),
#     )

#     pk = response.json()["pk"]
#     response = test_app_with_db.get(f"/task/{pk}")
#     assert response.json()["pk"] == pk
#     assert response.json()["created_at"]
#     assert response.json()["updated_at"]
#     assert response.json()["task_app"] == "test_app"
#     assert response.json()["task_env"] == "dev"
#     assert response.json()["task_name"] == "test_name"
#     assert response.json()["task_status"] == "success"
#     assert response.json()["task_watermark"] == "2022-06-01T00:00:00+00:00"
#     assert response.json()["task_start_at"] == "2022-06-01T01:00:00+00:00"
#     assert response.json()["task_stop_at"] == "2022-06-01T02:00:00+00:00"
#     assert response.json()["task_metadata"] == {
#         "key": "value",
#         "some": ["list", "of", "items"],
#     }


# def test_get_task_missing_pk(test_app_with_db):
#     response = test_app_with_db.get("/task/notarealpk")
#     assert response.status_code == 404
#     assert response.json()["detail"] == "Summary not found"
