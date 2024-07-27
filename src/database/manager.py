from .db import DB
from .model import ProfileUser, Image, Followers, Tweet, LikeTweet, Base
from sqlalchemy import update, select, delete, and_, desc, func
from sqlalchemy.orm import joinedload
from src.settings.config import settings


class ManagerDB:
    def __init__(self, db_url: str) -> None:
        self.db = DB(db_url)
        self.async_session = self.db.async_session

    async def create_user(self, user_data: dict) -> ProfileUser:
        async with self.async_session() as session:
            new_user: ProfileUser = ProfileUser(**user_data)
            print(new_user)
            session.add(new_user)
            await session.commit()
            user: ProfileUser = new_user
            return user

    async def get_user(self, api_key: str) -> ProfileUser | None:
        async with self.async_session() as session:
            user = await session.execute(select(ProfileUser).where(ProfileUser.api_key == api_key))
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
            await session.execute(update(Image).filter(Image.id == image_id).values(tweet_id=tweet_id))
            await session.commit()

    async def delete_tweet(self, tweet_id: int):
        async with self.async_session() as session:
            await session.execute(delete(Tweet).filter(Tweet.id == tweet_id))
            await session.commit()

    async def get_tweet_user(self, tweet_id: int, user_id: int) -> Tweet | None:
        async with self.async_session() as session:
            request_model = select(Tweet).options(joinedload(Tweet.user)).filter(
                and_(Tweet.user_id == user_id, Tweet.id == tweet_id))
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
            session.commit()

    async def delete_like_tweet(self, tweet_id: int, user_id: int) -> None:
        async with self.async_session() as session:
            await session.execute(
                delete(LikeTweet).filter(and_(LikeTweet.tweet_id == tweet_id, LikeTweet.user_id == user_id)))
            await session.commit()

    async def create_follower_record(self, user_id: int, follower_id: int) -> None:
        async with self.async_session() as session:
            session.add(Followers(user_id=user_id, follower_id=follower_id))
            await session.commit()

    async def delete_follower_record(self, user_id: int, follower_id: int) -> None:
        async with self.async_session() as session:
            await session.execute(
                delete(Followers).filter(and_(Followers.follower_id == follower_id, Followers.user_id == user_id)))
            await session.commit()

    async def check_user_for_id(self, user_id) -> ProfileUser | None:
        async with self.async_session() as session:
            user = await session.execute(select(ProfileUser).where(ProfileUser.id == user_id))
            return user.scalar_one_or_none()

    async def get_tweets(self, user_id: int) -> list[Tweet] | None:
        async with self.async_session() as session:
            # Подзапрос для получения ID пользователей, которых фоловит текущий пользователь
            follower_request_model = select(Followers.follower_id).filter(Followers.user_id == user_id).subquery()

            # Подзапрос для подсчета количества лайков для каждого твита
            tweet_likes_subquery = select(
                LikeTweet.tweet_id,
                func.count(LikeTweet.user_id).label('like_count')
            ).group_by(LikeTweet.tweet_id).subquery()

            # Основной запрос
            request_model = select(Tweet).select_from(
                Tweet
            ).join(follower_request_model, Tweet.user_id == follower_request_model.c.follower_id).outerjoin(
                tweet_likes_subquery, Tweet.id == tweet_likes_subquery.c.tweet_id).options(
                joinedload(Tweet.user),
                joinedload(Tweet.image),
                joinedload(Tweet.like_by_user)
            ).order_by(desc(tweet_likes_subquery.c.like_count))

            # Выполнение запроса
            result = await session.execute(request_model)
            return result.scalars().all()

    async def get_me_data(self, api_key: str) -> ProfileUser:
        async with self.async_session() as session:
            request_model = select(ProfileUser).where(ProfileUser.api_key == api_key).options(
                joinedload(ProfileUser.followers), joinedload(ProfileUser.following))
            me_info = await session.execute(request_model)
            return me_info.scalar()

    async def get_user_data(self, user_id: int) -> ProfileUser:
        async with self.async_session() as session:
            request_model = select(ProfileUser).where(ProfileUser.id == user_id).options(
                joinedload(ProfileUser.followers), joinedload(ProfileUser.following))
            user_info = await session.execute(request_model)
            return user_info.scalar()

    async def clear_models(self):
        async with self.db.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    async def init_models(self):
        async with self.db.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


model_manager = ManagerDB(db_url=settings.db_settings.url_db)
