import json


def test_create_user(test_app_with_db, test_admin_access_token):
    user_info = {
        "username": "amyrose",
        "email": "amyrose@hedgehog.com",
        "password": "mysweetpassion",
        "full_name": "Amy Rose",
        "category": "human",
    }
    response = test_app_with_db.post(
        "/user/create",
        data=json.dumps(user_info),
        headers={"Authorization": f"Bearer {test_admin_access_token}"},
    )

    assert response.status_code == 201
    assert response.json() == {"message": "Successfully created user 'amyrose'"}


def test_user_login_read(test_app_with_db, test_user_credentials):
    response = test_app_with_db.post(
        "/token",
        data=f"username={test_user_credentials['username']}&password={test_user_credentials['password']}",
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    assert response.json()["access_token"]
    assert response.json()["token_type"] == "bearer"
