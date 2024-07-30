from fastapi import Request
from settings.config import settings
from database.schemas import (
    TweetCreateSchema,
    TweetResponseSchema,
    SuccessfulResponseSchema,
    TweetSchema,
    TweetsFeed,
    AuthorSchema,
    LikeSchema,
)
from database.manager import model_manager
from .decorators.deocrators_tweets_logic import check_tweet, check_tweet_user
from settings.middlewares import check_user_authorization


class TweetOperations:
    def __init__(self, user_id):
        self.tweet_settings = settings.tweet_settings
        self.user_id: int = user_id

    async def tweet_post(self, tweet_schema: TweetCreateSchema):
        tweet_id: int = await model_manager.create_tweet(
            tweet_schema.tweet_data, self.user_id
        )
        if tweet_schema.tweet_media_ids:
            for media_id in tweet_schema.tweet_media_ids:
                await model_manager.update_image(image_id=media_id, tweet_id=tweet_id)
        return TweetResponseSchema(result=True, tweet_id=tweet_id)

    @check_tweet_user
    async def tweet_delete(self, tweet_id: int):
        await model_manager.delete_tweet(tweet_id=tweet_id)
        return SuccessfulResponseSchema(result=True)

    @check_tweet
    async def like_tweets(self, tweet_id: int):
        await model_manager.create_like_tweet(tweet_id=tweet_id, user_id=self.user_id)
        return SuccessfulResponseSchema(result=True)

    @check_tweet
    async def like_tweets_delete(self, tweet_id: int):
        await model_manager.delete_like_tweet(tweet_id=tweet_id, user_id=self.user_id)
        return SuccessfulResponseSchema(result=True)

    async def get_all_tweets(self):
        tweets = await model_manager.get_tweets(self.user_id)
        if not tweets:
            return TweetsFeed(result=True)
        tweets_feed = list()
        for tweet in tweets:
            author = AuthorSchema(id=tweet.user_id, name=tweet.user.name)
            tweet_schema = TweetSchema(
                id=tweet.id,
                content=tweet.content,
                attachments=(
                    [f"/api/medias/{img.file_path}" for img in tweet.image]
                    if tweet.image is not None
                    else []
                ),
                author=author,
                likes=(
                    [
                        LikeSchema(user_id=like_user.id, name=like_user.name)
                        for like_user in tweet.like_by_user
                    ]
                    if tweet.like_by_user is not None
                    else []
                ),
            )
            tweets_feed.append(tweet_schema)
        return TweetsFeed(result=True, tweets=tweets_feed)


@check_user_authorization
async def get_operation_tweets(request: Request):
    api_key = request.headers.get("api-key")
    user = await model_manager.get_user(api_key=api_key)
    tweet = TweetOperations(user_id=user.id)
    return tweet
