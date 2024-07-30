import uuid
from pathlib import Path
import os

from fastapi import Request, HTTPException
from database.schemas import ErrorSchema, MediaSchema
from settings.config import settings
from database.manager import model_manager


class MediaOperations:
    def __init__(self):
        self.setting_media = settings.media_settings
        self.error_message: str = "Error server"
        self.result: bool = True

    async def media_loading(self, request: Request):
        form = await request.form()
        file = form.get("file")
        file_name = f"{uuid.uuid4()}_{file.filename.lower()}"
        file_path: Path = self.setting_media.file_path / file_name.lower()
        with open(str(file_path), "wb") as f:
            f.write(await file.read())
        image_data: dict = {"file_path": f"static/images/{file_name}", "tweet_id": None}
        media_id: int = await model_manager.create_image(image_data)
        return MediaSchema(result=self.result, media_id=media_id)

    def get_media_file(self, file_name: str) -> str:
        file_location: str = str(self.setting_media.file_path / file_name)
        if os.path.exists(file_location):
            return file_location
        error_detail: ErrorSchema = ErrorSchema(
            result=False,
            error_type=self.setting_media.error_type,
            error_message="File is not Fount",
        )
        raise HTTPException(status_code=404, detail=error_detail)


def get_operation_media():
    return MediaOperations()
