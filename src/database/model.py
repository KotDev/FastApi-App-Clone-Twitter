from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.orm import declarative_base, mapped_column, Mapped, relationship

Base = declarative_base()


class ProfileUser(Base):
    __tablename__ = "profile"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    api_key: Mapped[str] = mapped_column(String(120), nullable=False)
    tweets: Mapped[list["Tweet"]] = relationship(back_populates="user")
    like_tweets: Mapped[list["Tweet"]] = relationship(back_populates="like_by_user", secondary="like")
    followers: Mapped[list["ProfileUser"]] = relationship(
        secondary="followers",
        primaryjoin="ProfileUser.id == followers.c.user_id",
        secondaryjoin="ProfileUser.id == followers.c.follower_id",
        back_populates="following"
    )
    following: Mapped[list["ProfileUser"]] = relationship(
        secondary="followers",
        primaryjoin="ProfileUser.id == Followers.follower_id",
        secondaryjoin="ProfileUser.id == Followers.user_id",
        back_populates="followers"
    )


class Followers(Base):
    __tablename__ = "followers"
    user_id: Mapped[int] = mapped_column(ForeignKey("profile.id", ondelete="CASCADE"), primary_key=True)
    follower_id: Mapped[int] = mapped_column(ForeignKey("profile.id", ondelete="CASCADE"), primary_key=True)


class Tweet(Base):
    __tablename__ = "tweet"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("profile.id", ondelete="CASCADE"), nullable=False)
    user: Mapped["ProfileUser"] = relationship(back_populates="tweets")
    like_by_user: Mapped["ProfileUser"] = relationship(back_populates="like_tweets", secondary="like")
    image: Mapped["Image"] = relationship(back_populates="tweet")


class LikeTweet(Base):
    __tablename__ = "like"
    tweet_id: Mapped[int] = mapped_column(ForeignKey("tweet.id", ondelete="CASCADE"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("profile.id", ondelete="CASCADE"), primary_key=True)


class Image(Base):
    __tablename__ = "image"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    file_path: Mapped[str] = mapped_column(nullable=False)
    tweet_id: Mapped[int] = mapped_column(ForeignKey("tweet.id", ondelete="CASCADE"), nullable=False)
    tweet: Mapped["Tweet"] = relationship(back_populates="image")
