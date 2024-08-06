import os

from fastapi import FastAPI, Request
from starlette.responses import HTMLResponse

from database.manager import model_manager
from settings.router import api_router
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()
app.include_router(api_router)


@app.on_event("startup")
async def startup_event():
    await model_manager.init_models()
    await model_manager.clear_models()
    await model_manager.create_test_user()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
