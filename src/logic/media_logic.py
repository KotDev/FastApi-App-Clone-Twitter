from pathlib import Path

from fastapi import Request
from src.database.schemas import ErrorSchema, MediaSchema
from src.settings.config import settings
from src.database.manager import model_manager


class MediaOperations:
    def __init__(self):
        self.setting_media = settings.media_settings
        self.error_message: str = "Error server"
        self.result: bool = True

    async def media_loading(self, request: Request):
        form = await request.form()
        file = form.get("file")
        if file is None:
            self.result = False
            self.error_message = "No file provided"
        elif not file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
            self.result = False
            self.error_message = "The file is in the wrong format"
        elif file.size > self.setting_media.max_size:
            self.result = False
            self.error_message = "The file is in the wrong format"
        if not self.result:
            return ErrorSchema(result=self.result,
                               error_type=self.setting_media.error_type,
                               error_message=self.error_message,
                               )
        file_path: Path = self.setting_media.file_path / file.filename.lower()
        with open(str(file_path), "wb") as f:
            f.write(await file.read())
        image_data: dict = {"file_path": str(file_path), "tweet_id": None}
        media_id: int = model_manager.create_image(image_data)
        return MediaSchema(result=self.result, media_id=media_id)


def get_operation_media():
    return MediaOperations()
