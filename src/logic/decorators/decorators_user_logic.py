from functools import wraps

from fastapi import HTTPException

from database.manager import model_manager
from database.schemas import ErrorSchema


def check_user(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        user_id: int = kwargs.get("user_id") or args[0]
        follower_id: int = kwargs.get("follower_id")
        if follower_id is not None:
            user_id = follower_id
        user = await model_manager.get_user(user_id=user_id)
        if user is None:
            detail_error = ErrorSchema(
                result=False,
                error_type=self.settings_user.error_type,
                error_message="User is not found",
            )
            raise HTTPException(status_code=404, detail=detail_error.dict())
        return await func(self, *args, **kwargs)

    return wrapper
