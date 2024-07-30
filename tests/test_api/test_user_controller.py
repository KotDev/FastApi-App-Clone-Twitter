import pytest
from aiohttp import ClientSession
from .conftest import (
    me_fixture,
    register_fixture,
    user_fixture,
    post_follower_fixture,
    delete_follower_fixture,
    delete_user_fixture,
    request,
)


@pytest.mark.order(1)
@pytest.mark.asyncio
async def test_register_point(register_fixture: dict) -> None:
    async with ClientSession() as session:
        response_data = await request(session, **register_fixture)
        assert "id" in response_data.json_data
        assert response_data.status_code == 200


@pytest.mark.order(2)
@pytest.mark.asyncio
async def test_get_me_point(me_fixture: dict) -> None:
    async with ClientSession(headers={"api-key": "test"}) as session:
        response_data = await request(session, **me_fixture)
        tes_data = "result", "user"
        assert response_data.status_code == 200
        for arg in tes_data:
            assert arg in response_data.json_data
        assert response_data.json_data["result"]


@pytest.mark.order(3)
@pytest.mark.asyncio
async def test_get_user_point(user_fixture: dict) -> None:
    async with ClientSession(headers={"api-key": "test"}) as session:
        response_data = await request(session, **user_fixture)
        tes_data = "result", "user"
        assert response_data.status_code == 200
        for arg in tes_data:
            assert arg in response_data.json_data
        assert response_data.json_data["result"]


@pytest.mark.order(4)
@pytest.mark.asyncio
async def test_post_follower_point(
    post_follower_fixture: dict, user_fixture: dict, me_fixture: dict
) -> None:
    async with ClientSession(headers={"api-key": "test"}) as session:
        response_data_follower = await request(session, **post_follower_fixture)
        response_data_user = await request(session, **user_fixture)
        assert response_data_follower.status_code == 200
        assert response_data_user.status_code == 200
        assert response_data_follower.json_data["result"]
        assert response_data_user.json_data["user"]["followers"]
        assert not response_data_user.json_data["user"]["following"]


@pytest.mark.order(5)
@pytest.mark.asyncio
async def test_delete_follower_point(
    user_fixture: dict, delete_follower_fixture: dict
) -> None:
    async with ClientSession(headers={"api-key": "test"}) as session:
        response_data_follower_delete = await request(
            session, **delete_follower_fixture
        )
        response_data_user = await request(session, **user_fixture)
        assert response_data_follower_delete.status_code == 200
        assert response_data_user.status_code == 200
        assert response_data_follower_delete.json_data["result"]
        assert not response_data_user.json_data["user"]["followers"]
        assert not response_data_user.json_data["user"]["following"]


@pytest.mark.order(6)
@pytest.mark.asyncio
async def test_middleware_authorization_point(user_fixture: dict) -> None:
    async with ClientSession(headers={"api-key": "123"}) as session:
        response_data_user = await request(session, **user_fixture)
        assert "detail" in response_data_user.json_data
        assert response_data_user.status_code == 403


@pytest.mark.order(7)
@pytest.mark.asyncio
async def test_delete_user_point(delete_user_fixture) -> None:
    async with ClientSession(headers={"api-key": "test"}) as session:
        response_data_user = await request(session, **delete_user_fixture)
        assert response_data_user.status_code == 200
        assert response_data_user.json_data["result"]
