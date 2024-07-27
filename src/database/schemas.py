from typing import Optional

from pydantic import BaseModel
from pydantic.types import List


class UserCreateSchema(BaseModel):
    name: str


class UserSchemaResponse(BaseModel):
    id: int
    api_key: str


class TweetCreateSchema(BaseModel):
    tweet_data: str
    tweet_media_ids: Optional[List[int]] = []


class TweetResponseSchema(BaseModel):
    result: bool
    tweet_id: int


class LikeSchema(BaseModel):
    user_id: int
    name: str


class AuthorSchema(BaseModel):
    id: int
    name: str


class TweetSchema(BaseModel):
    id: int
    content: str
    attachments: List[str]
    author: AuthorSchema = None
    likes: List[LikeSchema] = []


class TweetsFeed(BaseModel):
    result: bool
    tweets: List[TweetSchema] = []


class UserSchema(BaseModel):
    id: int
    name: str
    followers: List[AuthorSchema] = []
    following: List[AuthorSchema] = []


class UserInfoSchema(BaseModel):
    result: bool
    user: UserSchema


class ErrorSchema(BaseModel):
    result: bool
    error_type: str
    error_message: str


class MediaSchema(BaseModel):
    result: bool
    media_id: int


class SuccessfulResponseSchema(BaseModel):
    result: bool