import pytest
from aiohttp import ClientSession

from .conftest import (
    request,
    tweet_fixture,
    tweet_feed_fixture,
    tweet_delete_fixture,
    tweet_delete_like_fixture,
    tweet_post_like_fixture,
)


@pytest.mark.order(1)
@pytest.mark.asyncio
async def test_post_tweet_point(tweet_fixture):
    async with ClientSession(headers={"api-key": "test"}) as session:
        response_data = await request(session, **tweet_fixture)
        assert response_data.status_code == 200
        assert "tweet_id" in response_data.json_data
        assert response_data.json_data["result"]


@pytest.mark.order(2)
@pytest.mark.asyncio
async def test_post_like_point(tweet_post_like_fixture):
    async with ClientSession(headers={"api-key": "test"}) as session:
        response_data = await request(session, **tweet_post_like_fixture)
        assert response_data.status_code == 200
        assert response_data.json_data["result"]


@pytest.mark.order(3)
@pytest.mark.asyncio
async def test_delete_like_point(tweet_delete_like_fixture):
    async with ClientSession(headers={"api-key": "test"}) as session:
        response_data = await request(session, **tweet_delete_like_fixture)
        assert response_data.status_code == 200
        assert response_data.json_data["result"]


@pytest.mark.order(4)
@pytest.mark.asyncio
async def test_get_tweets_point(tweet_feed_fixture):
    async with ClientSession(headers={"api-key": "test"}) as session:
        response_data = await request(session, **tweet_feed_fixture)
        assert response_data.status_code == 200
        assert response_data.json_data["result"]
        assert response_data.json_data["tweets"]


@pytest.mark.order(5)
@pytest.mark.asyncio
async def test_delete_tweet_point(tweet_delete_fixture):
    async with ClientSession(headers={"api-key": "test"}) as session:
        response_data = await request(session, **tweet_delete_fixture)
        assert response_data.status_code == 200
        assert response_data.json_data["result"]
