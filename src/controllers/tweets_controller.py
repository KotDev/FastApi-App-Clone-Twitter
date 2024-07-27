from fastapi import APIRouter, Depends
from logic.tweets_logic import get_operation_tweets, TweetOperations
from database.schemas import TweetCreateSchema, TweetResponseSchema, SuccessfulResponseSchema, TweetsFeed
from settings.middlewares import check_user_authorization

router = APIRouter(prefix="/tweets", tags=["Tweets"])


@router.post("")
@check_user_authorization()
async def create_tweet_router(schema_create: TweetCreateSchema,
                              operation: TweetOperations = Depends(get_operation_tweets)):
    result: TweetResponseSchema = await operation.tweet_post(schema_create)
    return result


@router.get("")
@check_user_authorization()
async def get_all_tweets_router(operation: TweetOperations = Depends(get_operation_tweets)):
    result: TweetsFeed = await operation.get_all_tweets()
    return result


@router.delete("/{tweet_id}")
@check_user_authorization()
async def delete_tweet_router(tweet_id: int,
                              operation: TweetOperations = Depends(get_operation_tweets)):
    result: SuccessfulResponseSchema = await operation.tweet_delete(tweet_id=tweet_id)
    return result


@router.post("/{tweet_id}/likes")
@check_user_authorization()
async def add_like_tweet_router(tweet_id: int,
                                operation: TweetOperations = Depends(get_operation_tweets)):
    result: SuccessfulResponseSchema = await operation.like_tweets(tweet_id=tweet_id)
    return result


@router.delete("/{tweet_id}/likes")
@check_user_authorization()
async def delete_like_tweet_router(tweet_id: int,
                                   operation: TweetOperations = Depends(get_operation_tweets)):
    result: SuccessfulResponseSchema = await operation.like_tweets_delete(tweet_id=tweet_id)
    return result


