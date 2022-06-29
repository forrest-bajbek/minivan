import os

import pytest
from starlette.testclient import TestClient
from tortoise.contrib.fastapi import register_tortoise

from app.config import Settings, get_settings
from app.main import create_application


def get_settings_override():
    return Settings(testing=1, database_url=os.environ.get("TEST_DATABASE_URL"))


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
        # db_url=os.environ.get("TEST_DATABASE_URL"),
        db_url="sqlite://:memory:",
        modules={"models": ["app.models.tortoise"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="function")
def test_task_payload():
    yield {
        "task_app": "test_app",
        "task_env": "dev",
        "task_name": "test_name",
        "task_status": "success",
        "task_watermark": "2022-06-01T00:00:00+00:00",
        "task_duration": 402.13,
        "task_metadata": {"key": "value", "some": ["list", "of", "items"]},
    }
