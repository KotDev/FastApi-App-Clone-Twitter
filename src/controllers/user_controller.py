from fastapi import APIRouter, Depends, Request
from logic.users_logic import UserOperations, get_user_operations
from database.schemas import (
    UserCreateSchema,
    UserInfoSchema,
    SuccessfulResponseSchema,
)
from database.manager import model_manager
from settings.middlewares import check_user_authorization

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register")
async def register_user_router(
    operation: UserOperations = Depends(get_user_operations),
    create_schema: UserCreateSchema = UserCreateSchema,
):
    result = await operation.create_user(create_schema)
    return result


@router.get("/me")
@check_user_authorization
async def get_user_me_router(
    request: Request,
    operation: UserOperations = Depends(get_user_operations),
):
    api_key: str = request.headers.get("api-key")
    result: UserInfoSchema = await operation.get_me(api_key)
    return result


@router.get("/{user_id}")
@check_user_authorization
async def get_user_router(
    user_id: int,
    request: Request,
    operation: UserOperations = Depends(get_user_operations),
):
    result: UserInfoSchema = await operation.get_user(user_id)
    print(result)
    return result


@router.post("/{follower_id}/follow")
@check_user_authorization
async def follow_user_router(
    follower_id: int,
    request: Request,
    operation: UserOperations = Depends(get_user_operations),
):
    api_key: str = request.headers.get("api-key")
    user = await model_manager.get_user(api_key)
    user_id: int = user.id
    result: SuccessfulResponseSchema = await operation.add_follow(user_id, follower_id)
    return result


@router.delete("/{follower_id}/follow")
@check_user_authorization
async def follow_user_router(
    follower_id: int,
    request: Request,
    operation: UserOperations = Depends(get_user_operations),
):
    api_key: str = request.headers.get("api-key")
    user = await model_manager.get_user(api_key)
    user_id: int = user.id
    result: SuccessfulResponseSchema = await operation.delete_follow(
        user_id, follower_id
    )
    return result


@router.delete("/{user_id}/delete")
@check_user_authorization
async def delete_user_router(
    user_id: int,
    request: Request,
    operation: UserOperations = Depends(get_user_operations),
):
    result: SuccessfulResponseSchema = await operation.delete_profile(user_id)
    return result
