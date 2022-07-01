import os
import json

import pytest
from starlette.testclient import TestClient
from tortoise.contrib.fastapi import register_tortoise

from app.config import Settings, get_settings
from app.main import create_application

test_database_url = "sqlite://:memory:"


def get_settings_override():
    return Settings(testing=1)


@pytest.fixture(scope="module")
def test_app():
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="module")
def test_app_with_db():
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    register_tortoise(
        app=app,
        db_url=test_database_url,
        modules={"models": ["app.models.tortoise"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="module")
def test_admin_access_token(test_app_with_db):
    admin_info = {
        "username": "sonic",
        "email": "sonic@hedgehog.com",
        "password": "openyourheart",
        "full_name": "Sonic The Hedgehog",
        "category": "human",
    }
    # Create admin account
    response = test_app_with_db.post(
        "/admin/create",
        data=json.dumps(admin_info),
    )
    # Log in as admin, get access_token
    response = test_app_with_db.post(
        "/token",
        data=f"username={admin_info['username']}&password={admin_info['password']}",
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    yield response.json()["access_token"]


@pytest.fixture(scope="module")
def test_user_credentials(test_app_with_db, test_admin_access_token):
    user_info = {
        "username": "amyrose",
        "email": "amyrose@hedgehog.com",
        "password": "mysweetpassion",
        "full_name": "Amy Rose",
        "category": "human",
    }
    # Create user account
    response = test_app_with_db.post(
        "/user/create",
        data=json.dumps(user_info),
        headers={"Authorization": f"Bearer {test_admin_access_token}"},
    )
    yield {"username": user_info["username"], "password": user_info["password"]}


@pytest.fixture(scope="module")
def test_user_access_token_read(test_app_with_db, test_user_credentials):
    # Log in as user with read scope, get access_token
    response = test_app_with_db.post(
        "/token",
        data=f"username={test_user_credentials['username']}&password={test_user_credentials['password']}&scope=read",
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    yield response.json()["access_token"]


@pytest.fixture(scope="module")
def test_user_access_token_write(test_app_with_db, test_user_credentials):
    # Log in as user with write scope, get access_token
    response = test_app_with_db.post(
        "/token",
        data=f"username={test_user_credentials['username']}&password={test_user_credentials['password']}&scope=write",
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    yield response.json()["access_token"]
