import secrets
import string
from database.manager import model_manager
from database.schemas import (
    UserCreateSchema,
    UserSchemaResponse,
    SuccessfulResponseSchema,
    UserInfoSchema,
    AuthorSchema,
    UserSchema,
)
from settings.config import settings
from .decorators.decorators_user_logic import check_user


class UserOperations:
    def __init__(self):
        self.settings_user = settings.user_settings

    def _generate_api_key(self) -> str:
        characters = string.ascii_letters + string.digits + string.punctuation
        return "".join(secrets.choice(characters) for _ in range(120))

    async def create_user(
        self, user_schema_create: UserCreateSchema
    ) -> UserSchemaResponse:
        api_key = self._generate_api_key()
        user_data = {"name": user_schema_create.name, "api_key": api_key}
        user = await model_manager.create_user(user_data)
        return UserSchemaResponse(id=user.id, api_key=user.api_key)

    async def get_me(self, api_key: str) -> UserInfoSchema:
        me_info = await model_manager.get_user_data(api_key=api_key)
        schema = UserSchema(
            id=me_info.id,
            name=me_info.name,
            following=[
                AuthorSchema(id=follower.id, name=follower.name)
                for follower in me_info.followers
            ],
            followers=[
                AuthorSchema(id=follower.id, name=follower.name)
                for follower in me_info.following
            ],
        )
        return UserInfoSchema(result=True, user=schema)

    @check_user
    async def add_follow(
        self, user_id: int, follower_id: int
    ) -> SuccessfulResponseSchema:
        await model_manager.create_follower_record(user_id, follower_id)
        return SuccessfulResponseSchema(result=True)

    @check_user
    async def delete_follow(
        self, user_id: int, follower_id: int
    ) -> SuccessfulResponseSchema:
        await model_manager.delete_follower_record(
            followed_id=user_id, follower_id=follower_id
        )
        return SuccessfulResponseSchema(result=True)

    @check_user
    async def get_user(self, user_id: int) -> UserInfoSchema:
        user = await model_manager.get_user_data(user_id=user_id)
        schema = UserSchema(
            id=user.id,
            name=user.name,
            following=[
                AuthorSchema(id=followed.id, name=followed.name)
                for followed in user.followers
            ],
            followers=[
                AuthorSchema(id=follower.id, name=follower.name)
                for follower in user.following
            ],
        )
        return UserInfoSchema(result=True, user=schema)

    @check_user
    async def delete_profile(self, user_id: int) -> SuccessfulResponseSchema:
        await model_manager.delete_user(user_id)
        return SuccessfulResponseSchema(result=True)


def get_user_operations() -> UserOperations:
    return UserOperations()
