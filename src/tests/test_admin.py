import json


def test_create_admin(test_app_with_db):
    admin_info = {
        "username": "sonic",
        "email": "sonic@hedgehog.com",
        "password": "openyourheart",
        "full_name": "Sonic The Hedgehog",
        "category": "human",
    }
    response = test_app_with_db.post("/admin/create", data=json.dumps(admin_info))
    assert response.status_code == 201
    assert response.json() == {"message": "Admin account created for user 'sonic'"}
