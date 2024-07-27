from functools import wraps

from fastapi import HTTPException

from database.manager import model_manager
from database.schemas import ErrorSchema


def check_tweet():
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            tweet_id: int = kwargs.get("tweet_id") or args[0]
            tweet = await model_manager.get_tweet(tweet_id)
            if tweet is None:
                error_detail: ErrorSchema = ErrorSchema(result=False,
                                                        type_error=self.tweet_settings.error_type.get_error,
                                                        error_message="Tweet is not fount")
                raise HTTPException(status_code=404, detail=error_detail.dict())
            return await func(self, *args, **kwargs)
        return wrapper
    return decorator


def check_tweet_user():
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            tweet_id = kwargs.get("tweet_id") or args[0]
            tweet = await model_manager.get_tweet_user(self.user_id, tweet_id)
            if tweet is None:
                error_detail: ErrorSchema = ErrorSchema(result=False,
                                                        type_error=self.tweet_settings.error_type.get_error,
                                                        error_message="Tweet is not fount")
                raise HTTPException(status_code=404, detail=error_detail.dict())
            return await func(self, *args, **kwargs)
        return wrapper
    return decorator