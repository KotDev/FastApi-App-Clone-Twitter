import pytest
from logic.tweets_logic import TweetOperations
from logic.users_logic import UserOperations
from .conftest import auto_clear


@pytest.mark.asyncio
@auto_clear()
async def test_create_tweet(tweet_fixture, user_fixture):
    user_operation = UserOperations()
    user = await user_operation.create_user(user_fixture[0])
    tweet_operation = TweetOperations(user_id=user.id)
    result = await tweet_operation.tweet_post(tweet_fixture)
    assert result.result
    assert result.tweet_id == 1


@pytest.mark.asyncio
@auto_clear()
async def test_delete_tweet(tweet_fixture, user_fixture):
    user_operation = UserOperations()
    user = await user_operation.create_user(user_fixture[0])
    tweet_operation = TweetOperations(user_id=user.id)
    tweet = await tweet_operation.tweet_post(tweet_fixture)
    result = await tweet_operation.tweet_delete(tweet.tweet_id)
    assert result.result


@pytest.mark.asyncio
@auto_clear()
async def test_add_like_tweet(tweet_fixture, user_fixture):
    user_operation = UserOperations()
    user_1 = await user_operation.create_user(user_fixture[0])
    user_2 = await user_operation.create_user(user_fixture[1])
    tweet_operation_user_1 = TweetOperations(user_id=user_1.id)
    tweet = await tweet_operation_user_1.tweet_post(tweet_fixture)
    tweet_operation_user_2 = TweetOperations(user_id=user_2.id)
    result = await tweet_operation_user_2.like_tweets(tweet.tweet_id)
    assert result.result


@pytest.mark.asyncio
@auto_clear()
async def test_delete_like_tweet(tweet_fixture, user_fixture):
    user_operation = UserOperations()
    user_1 = await user_operation.create_user(user_fixture[0])
    user_2 = await user_operation.create_user(user_fixture[1])
    tweet_operation_user_1 = TweetOperations(user_id=user_1.id)
    tweet = await tweet_operation_user_1.tweet_post(tweet_fixture)
    tweet_operation_user_2 = TweetOperations(user_id=user_2.id)
    await tweet_operation_user_2.like_tweets(tweet.tweet_id)
    result = await tweet_operation_user_2.like_tweets_delete(tweet.tweet_id)
    assert result.result


@pytest.mark.asyncio
@auto_clear()
async def test_delete_like_tweet(tweet_fixture, user_fixture):
    user_operation = UserOperations()
    user_1 = await user_operation.create_user(user_fixture[0])
    user_2 = await user_operation.create_user(user_fixture[1])
    tweet_operation_user_1 = TweetOperations(user_id=user_1.id)
    tweet_operation_user_2 = TweetOperations(user_id=user_2.id)
    await user_operation.add_follow(user_id=user_1.id, follower_id=user_2.id)
    await tweet_operation_user_1.tweet_post(tweet_fixture)
    await tweet_operation_user_2.tweet_post(tweet_fixture)
    result = await tweet_operation_user_1.get_all_tweets()
    assert result.result

