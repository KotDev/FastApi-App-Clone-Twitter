from fastapi import APIRouter
from controllers.user_controller import router as user_router
from controllers.media_controller import router as media_router
from controllers.tweets_controller import router as tweet_router

api_router = APIRouter(prefix="/api", tags=["API"])

api_router.include_router(user_router)
api_router.include_router(media_router)
api_router.include_router(tweet_router)
