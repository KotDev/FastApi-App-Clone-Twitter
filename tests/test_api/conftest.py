import pytest

from aiohttp import ClientSession
from dataclasses import dataclass

BASE_URL = "tweet_api"

@dataclass
class ResponseData:
    json_data: dict
    status_code: int


async def request(
    session: ClientSession,
    url: str,
    method: str,
    json_data: dict | None = None,
) -> ResponseData:
    async with getattr(session, method)(url, json=json_data) as response:
        data = await response.json()
        return ResponseData(json_data=data, status_code=response.status)


@pytest.fixture
def register_fixture() -> dict:
    return {
        "url": f"http://{BASE_URL}:8000/api/users/register",
        "method": "post",
        "json_data": {"name": "Гоша"},
    }


@pytest.fixture
def me_fixture() -> dict:
    return {
        "url": f"http://{BASE_URL}:8000/api/users/me",
        "method": "get",
    }


@pytest.fixture
def user_fixture() -> dict:
    return {"url": f"http://{BASE_URL}:8000/api/users/2", "method": "get"}


@pytest.fixture
def post_follower_fixture() -> dict:
    return {
        "url": f"http://{BASE_URL}:8000/api/users/2/follow",
        "method": "post",
    }


@pytest.fixture
def delete_follower_fixture() -> dict:
    return {"url": f"http://{BASE_URL}:8000/api/users/2/follow", "method": "delete"}


@pytest.fixture
def delete_user_fixture() -> dict:
    return {"url": f"http://{BASE_URL}:8000/api/users/2/delete", "method": "delete"}


@pytest.fixture
def tweet_fixture() -> dict:
    return {
        "url": f"http://{BASE_URL}:8000/api/tweets",
        "method": "post",
        "json_data": {"tweet_data": "Новый твит", "tweet_media_ids": []},
    }


@pytest.fixture
def tweet_feed_fixture() -> dict:
    return {"url": f"http://{BASE_URL}:8000/api/tweets", "method": "get"}


@pytest.fixture
def tweet_delete_fixture() -> dict:
    return {"url": f"http://{BASE_URL}:8000/api/tweets/1", "method": "delete"}


@pytest.fixture
def tweet_post_like_fixture() -> dict:
    return {"url": f"http://{BASE_URL}:8000/api/tweets/1/likes", "method": "post"}


@pytest.fixture
def tweet_delete_like_fixture() -> dict:
    return {"url": f"http://{BASE_URL}:8000/api/tweets/1/likes", "method": "delete"}
