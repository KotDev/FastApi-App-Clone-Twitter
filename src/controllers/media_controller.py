from fastapi import APIRouter, Depends, Request
from logic.media_logic import get_operation_media, MediaOperations
from database.schemas import MediaSchema
from settings.middlewares import check_user_authorization

router = APIRouter(prefix="/medias", tags=["Media"])


@router.post("")
@check_user_authorization()
async def create_media_router(request: Request,
                              operation: MediaOperations = Depends(get_operation_media)):
    result: MediaSchema = await operation.media_loading(request)
    return result
