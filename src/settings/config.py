from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent / "src"


class DBSettings(BaseModel):
    url_db: str = "postgresql+asyncpg://root:root@localhost:5434/tweet_api"


class MediaSettings(BaseModel):
    file_path: Path = BASE_DIR / "static" / "images"
    max_size: int = 5 * 1024 * 1024
    error_type: str = "UploadFileError"


class TweetTypeError(BaseModel):
    post_error: str = "TweetPostError"
    get_error: str = "TweetGetError"
    delete_error: str = "TweetDeleteError"


class TweetSettings(BaseModel):
    error_type: TweetTypeError = TweetTypeError()


class UserSettings(BaseModel):
    error_type: str = "UserError"

class Settings(BaseSettings):
    user_settings: UserSettings = UserSettings()
    media_settings: MediaSettings = MediaSettings()
    tweet_settings: TweetSettings = TweetSettings()
    db_settings: DBSettings = DBSettings()


settings = Settings()