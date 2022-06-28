import pytest
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from starlette.testclient import TestClient

from app.config import Settings, get_settings
from app.db import redis_cache, redis_data
from app.main import create_application
from app.models.redis import Task


def get_settings_override():
    return Settings(testing=True)


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

    settings = get_settings_override()
    Task.Meta.database = redis_data(testing=settings.testing)
    FastAPICache.init(
        RedisBackend(redis_cache(testing=settings.testing)),
        prefix="testing-fastapi-cache",
    )

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="module")
def test_task_payload():
    yield {
        "task_app": "test_app",
        "task_env": "dev",
        "task_name": "test_name",
        "task_status": "success",
        "task_watermark": "2022-06-01T00:00:00+00:00",
        "task_start_at": "2022-06-01T01:00:00+00:00",
        "task_stop_at": "2022-06-01T02:00:00+00:00",
        "task_metadata": {"key": "value", "some": ["list", "of", "items"]},
    }
