from fastapi import APIRouter, Depends, Request
from logic.media_logic import get_operation_media, MediaOperations
from database.schemas import MediaSchema
from fastapi.responses import FileResponse
from settings.middlewares import check_user_authorization, check_media_file

router = APIRouter(prefix="/medias", tags=["Media"])


@router.post("")
@check_user_authorization
@check_media_file
async def create_media_router(
    request: Request, operation: MediaOperations = Depends(get_operation_media)
):
    result: MediaSchema = await operation.media_loading(request)
    return result


@router.get("/static/images/{file_name}")
def serve_image(
    file_name: str, operation: MediaOperations = Depends(get_operation_media)
):
    file_path: str = operation.get_media_file(file_name=file_name)
    return FileResponse(file_path)
