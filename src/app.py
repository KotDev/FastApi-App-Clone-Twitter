import os

from fastapi import FastAPI
from src.database.manager import model_manager
from settings.router import api_router
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()
app.include_router(api_router)
app.mount("", StaticFiles(directory=os.path.abspath("static")), name="static")


@app.on_event("startup")
async def startup_event():
    await model_manager.init_models()


@app.on_event("shutdown")
async def shutdown_event():
    await model_manager.clear_models()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)