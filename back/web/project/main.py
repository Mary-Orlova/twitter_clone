from pathlib import Path

import uvicorn
from fastapi import APIRouter, FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from logging_config import setup_custom_logger

logger = setup_custom_logger(__name__)


app = FastAPI(
    title="Микросервис блогинга API",
    description="API для управления микросервисом блогинга",
    version="1.0.0",
)

static_path = Path(__file__).parent.parent.parent / "dist" / "static"

# Проверка пути
# logger.info(f"Фактический путь: {static_path.absolute()} | Существует: {static_path.exists()}")

# Монтируем статику
app.mount("/static", StaticFiles(directory=str(static_path), html=True), name="static")
app.mount("/css", StaticFiles(directory=str(static_path) + "/css"), name="css")
app.mount("/js", StaticFiles(directory=str(static_path) + "/js"), name="js")

api_router = APIRouter()


# Стартовая страница корня проекта
@api_router.get("/")
async def root():
    return FileResponse(static_path / "index.html")


@api_router.get("/users/me")
async def about_me():
    return {
        "result": "true",
        "user": {
            "id": "int",
            "name": "str",
            "followers": [{"id": "int", "name": "str"}],
            "following": [{"id": "int", "name": "str"}],
        },
    }


@app.get("/api/test")
def test1():
    return {"id": 1, "name": "Mary"}


app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    logger.info("Запуск осуществлен")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
