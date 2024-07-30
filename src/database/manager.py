from .db import DB
from .model import ProfileUser, Image, Followers, Tweet, LikeTweet, Base
from sqlalchemy import update, select, delete, and_, desc, func
from sqlalchemy.orm import joinedload, selectinload
from settings.config import settings


class ManagerDB:
    def __init__(self, db_url: str) -> None:
        self.db = DB(db_url)
        self.async_session = self.db.async_session

    async def create_user(self, user_data: dict) -> ProfileUser:
        async with self.async_session() as session:
            new_user: ProfileUser = ProfileUser(**user_data)
            session.add(new_user)
            await session.commit()
            user: ProfileUser = new_user
            return user

    async def create_test_user(self) -> None:
        async with self.async_session() as session:
            session.add(ProfileUser(name="Тестовый пользователь", api_key="test"))
            await session.commit()

    async def get_user(
        self, api_key: str | None = None, user_id: int | None = None
    ) -> ProfileUser | None:
        async with self.async_session() as session:
            request_model = select(ProfileUser)
            if api_key is None:
                request_model = request_model.where(ProfileUser.id == user_id)
            else:
                request_model = request_model.where(ProfileUser.api_key == api_key)
            user = await session.execute(request_model)
            return user.scalar_one_or_none()

    async def create_tweet(self, tweet_data: str, user_id: int) -> int:
        async with self.async_session() as session:
            new_tweet: Tweet = Tweet(content=tweet_data, user_id=user_id)
            session.add(new_tweet)
            await session.commit()
            tweet_id: int = new_tweet.id
            return tweet_id

    async def create_image(self, image_data: dict) -> int:
        async with self.async_session() as session:
            new_image: Image = Image(**image_data)
            session.add(new_image)
            await session.commit()
            image_id: int = new_image.id
            return image_id

    async def update_image(self, image_id: int, tweet_id: int) -> None:
        async with self.async_session() as session:
            await session.execute(
                update(Image).filter(Image.id == image_id).values(tweet_id=tweet_id)
            )
            await session.commit()

    async def delete_tweet(self, tweet_id: int):
        async with self.async_session() as session:
            await session.execute(delete(Tweet).filter(Tweet.id == tweet_id))
            await session.commit()

    async def get_tweet_user(self, tweet_id: int, user_id: int) -> Tweet | None:
        async with self.async_session() as session:
            request_model = (
                select(Tweet)
                .options(joinedload(Tweet.user))
                .filter(and_(Tweet.user_id == user_id, Tweet.id == tweet_id))
            )
            result = await session.execute(request_model)
            return result.scalar_one_or_none()

    async def get_tweet(self, tweet_id: int) -> Tweet | None:
        async with self.async_session() as session:
            request_model = select(Tweet).filter(Tweet.id == tweet_id)
            tweet = await session.execute(request_model)
            return tweet.scalar_one_or_none()

    async def create_like_tweet(self, tweet_id: int, user_id: int) -> None:
        async with self.async_session() as session:
            session.add(LikeTweet(tweet_id=tweet_id, user_id=user_id))
            await session.commit()

    async def delete_like_tweet(self, tweet_id: int, user_id: int) -> None:
        async with self.async_session() as session:
            await session.execute(
                delete(LikeTweet).filter(
                    and_(LikeTweet.tweet_id == tweet_id, LikeTweet.user_id == user_id)
                )
            )
            await session.commit()

    async def create_follower_record(self, followed_id: int, follower_id: int) -> None:
        async with self.async_session() as session:
            session.add(Followers(followed_id=followed_id, follower_id=follower_id))
            await session.commit()

    async def delete_follower_record(self, followed_id: int, follower_id: int) -> None:
        async with self.async_session() as session:
            await session.execute(
                delete(Followers).filter(
                    and_(
                        Followers.follower_id == follower_id,
                        Followers.followed_id == followed_id,
                    )
                )
            )
            await session.commit()

    async def get_tweets(self, user_id: int) -> list[Tweet] | None:
        async with self.async_session() as session:
            follower_subquery = (
                select(Followers.followed_id)
                .where(Followers.follower_id == user_id)
                .subquery()
            )

            tweet_likes_subquery = (
                select(
                    LikeTweet.tweet_id,
                    func.count(LikeTweet.user_id).label("like_count"),
                )
                .group_by(LikeTweet.tweet_id)
                .subquery()
            )

            request_model = (
                select(Tweet)
                .join(
                    follower_subquery,
                    Tweet.user_id == follower_subquery.c.followed_id,
                    isouter=True,
                )
                .join(
                    tweet_likes_subquery,
                    Tweet.id == tweet_likes_subquery.c.tweet_id,
                    isouter=True,
                )
                .options(
                    selectinload(Tweet.user),
                    selectinload(Tweet.image),
                    selectinload(Tweet.like_by_user),
                )
                .order_by(desc(tweet_likes_subquery.c.like_count))
            )

            result = await session.execute(request_model)
            result = result.scalars().all()
            return result

    async def get_user_data(
        self, user_id: int = None, api_key: str = None
    ) -> ProfileUser:
        async with self.async_session() as session:
            request_model = select(ProfileUser)
            if api_key is None:
                request_model = request_model.where(ProfileUser.id == user_id)
            else:
                request_model = request_model.where(ProfileUser.api_key == api_key)
            request_model = request_model.options(
                joinedload(ProfileUser.followers), joinedload(ProfileUser.following)
            )
            user_info = await session.execute(request_model)
            return user_info.scalar()

    async def delete_user(self, user_id: int) -> None:
        async with self.async_session() as session:
            await session.execute(delete(ProfileUser).where(ProfileUser.id == user_id))
            await session.commit()

    async def clear_models(self) -> None:
        async with self.db.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    async def init_models(self) -> None:
        async with self.db.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


model_manager = ManagerDB(db_url=settings.db_settings.url_db)
