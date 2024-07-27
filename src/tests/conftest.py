from functools import wraps

import pytest

from database.schemas import UserCreateSchema, TweetCreateSchema
from database.manager import model_manager


@pytest.fixture
def user_fixture() -> tuple:
    return UserCreateSchema(name="Вова"), UserCreateSchema(name="Боб")


@pytest.fixture
def tweet_fixture():
    return TweetCreateSchema(tweet_data="Новый твит", tweet_media_ids=[])


def auto_clear():
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            await func(*args, **kwargs)
            await model_manager.clear_models()

        return wrapper

    return decorator
