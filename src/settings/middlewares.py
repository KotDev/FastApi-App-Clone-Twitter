from functools import wraps
from fastapi import Request, HTTPException

from database.manager import model_manager
from database.schemas import ErrorSchema


def check_user_authorization():
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request: Request = kwargs.get("request")
            if request is None:
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break
            if request is None:
                detail_error = ErrorSchema(
                        result=False,
                        error_type="RequestError",
                        error_message="API key is missing or request is missing"
                )
                raise HTTPException(status_code=400, detail=detail_error.dict())
            api_key = request.headers.get("api-key")
            user = await model_manager.get_user(api_key)
            if user is None:
                detail_error = ErrorSchema(
                    result=False,
                    error_type="AuthorizationError",
                    error_message="User is not authorization or register"
                )
                raise HTTPException(status_code=403, detail=detail_error.dict())
            return await func(*args, **kwargs)

        return wrapper

    return decorator
