import pytest

from logic.users_logic import UserOperations
from src.database.schemas import UserCreateSchema
from src.database.manager import model_manager
import asyncio
from .conftest import auto_clear


@pytest.mark.asyncio
@auto_clear()
async def test_create_user(user_fixture):
    user_operation = UserOperations()
    print(user_fixture)
    result = await user_operation.create_user(user_fixture[0])
    assert result.id == 1


@pytest.mark.asyncio
@auto_clear()
async def test_follow_user_add(user_fixture):
    user_operation = UserOperations()
    user_1 = await user_operation.create_user(user_fixture[0])
    user_2 = await user_operation.create_user(user_fixture[1])
    result = await user_operation.add_follow(user_1.id, user_2.id)
    assert result.result


@pytest.mark.asyncio
@auto_clear()
async def test_follow_user_delete(user_fixture):
    user_operation = UserOperations()
    user_1 = await user_operation.create_user(user_fixture[0])
    user_2 = await user_operation.create_user(user_fixture[1])
    await user_operation.add_follow(user_1.id, user_2.id)
    result = await user_operation.delete_follow(user_1.id, user_2.id)
    assert result.result




