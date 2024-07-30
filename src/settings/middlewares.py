from functools import wraps
from fastapi import Request, HTTPException

from database.manager import model_manager
from database.schemas import ErrorSchema
from .config import settings


def get_request(args: tuple):
    for arg in args:
        if isinstance(arg, Request):
            return arg
    detail_error = ErrorSchema(
        result=False,
        error_type="RequestError",
        error_message="API key is missing or request is missing",
    )
    raise HTTPException(status_code=400, detail=detail_error.dict())


def check_user_authorization(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request: Request = kwargs.get("request")
        if request is None:
            request: Request = get_request(args)
        api_key = request.headers.get("api-key")
        user = await model_manager.get_user(api_key)
        if user is None:
            detail_error = ErrorSchema(
                result=False,
                error_type="AuthorizationError",
                error_message="User is not authorization or register",
            )
            raise HTTPException(status_code=403, detail=detail_error.dict())
        return await func(*args, **kwargs)

    return wrapper


def check_media_file(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request: Request = kwargs.get("request")
        if request is None:
            request: Request = get_request(args)
        form = await request.form()
        file = form.get("file")
        error_message = ""
        if file is None:
            error_message = "No file provided"
        elif not file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
            error_message = "The file is in the wrong format"
        elif file.size > settings.media_settings.max_size:
            error_message = "The file is in the wrong format"
        if error_message:
            error_detail = ErrorSchema(
                result=False,
                error_type=settings.media_settings.error_type,
                error_message=error_message,
            )
            raise HTTPException(status_code=400, detail=error_detail)
        return await func(*args, **kwargs)

    return wrapper
