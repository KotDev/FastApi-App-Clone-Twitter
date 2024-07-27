from functools import wraps

from fastapi import HTTPException

from database.manager import model_manager
from database.schemas import ErrorSchema


def check_follower():
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            follower_id: int = kwargs.get("follower_id") or args[1]
            follower = await model_manager.check_user_for_id(follower_id)
            if follower is None:
                detail_error = ErrorSchema(
                    result=False,
                    error_type=self.settings_user.error_type,
                    error_message="Follower is not found"
                ).error_message
                raise HTTPException(status_code=404, detail=detail_error.dict())
            return await func(self, *args, **kwargs)
        return wrapper
    return decorator


def check_user():
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            user_id: int = kwargs.get("user_id") or args[0]
            user = await model_manager.check_user_for_id(user_id)
            if user is None:
                detail_error = ErrorSchema(
                    result=False,
                    error_type=self.settings_user.error_type,
                    error_message="User is not found"
                ).error_message
                raise HTTPException(status_code=404, detail=detail_error.dict())
            return await func(self, *args, **kwargs)
        return wrapper
    return decorator