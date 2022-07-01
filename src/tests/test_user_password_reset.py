import json


def test_user_password_reset(test_app_with_db, test_admin_access_token):
    # Create user
    # ---------------------------------------------------------------------------------
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

    # Log in as new user
    # ---------------------------------------------------------------------------------
    response = test_app_with_db.post(
        "/token",
        data=f"username={user_info['username']}&password={user_info['password']}",
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    assert response.json()["access_token"]
    assert response.json()["token_type"] == "bearer"

    # Change user password
    # ---------------------------------------------------------------------------------
    new_user_info = {
        "username": "amyrose",
        "new_password": "spinninghammer",
    }
    response = test_app_with_db.put(
        "/user/password/reset",
        data=json.dumps(new_user_info),
        headers={"Authorization": f"Bearer {test_admin_access_token}"},
    )
    assert response.status_code == 202
    assert response.json() == {
        "message": "Password successfully reset for user 'amyrose'"
    }

    # Log in as user with new password
    # ---------------------------------------------------------------------------------
    response = test_app_with_db.post(
        "/token",
        data=f"username={new_user_info['username']}&password={new_user_info['new_password']}",
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    assert response.json()["access_token"]
    assert response.json()["token_type"] == "bearer"
