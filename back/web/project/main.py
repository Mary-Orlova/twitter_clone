from pathlib import Path

import uvicorn
from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import FileResponse
from project.exeptions import BackendExeption
from project.logging_config import setup_custom_logger
from project.media.routes import router as media_router
from project.tweets.routes import router as tweets_router
from project.users.routes import router as users_router
from starlette.responses import JSONResponse

logger = setup_custom_logger(__name__)


app = FastAPI(
    title="Микросервис блогинга API",
    description="API для управления микросервисом блогинга",
    version="1.0.0",
)

static_path = Path(__file__).parent.parent.parent / "dist" / "static"

# Проверка пути
logger.info(
    f"Фактический путь: {static_path.absolute()} | Существует: {static_path.exists()}"
)

# Монтируем статику без докера
# app.mount("/static", StaticFiles(directory=str(static_path), html=True), name="static")
# app.mount("/css", StaticFiles(directory=str(static_path) + "/css"), name="css")
# app.mount("/js", StaticFiles(directory=str(static_path) + "/js"), name="js")

api_router = APIRouter()


# Стартовая страница корня проекта
@api_router.get(
    "/",
    summary="Стартовая страница",
    response_description="Возвращает статическую стартовую страницу",
)
async def root():
    """
    Возвращает статическую стартовую страницу проекта.

    - Для работы с API используйте документацию по адресу /docs (Swagger UI).
    - Для подробной информации обратитесь к README.
    """

    return FileResponse(static_path / "index.html")


@api_router.get(
    "/test", summary="Тест api/test", response_description="Возвращает id и name"
)
async def test1():
    return {"id": 1, "name": "Mary"}


@app.exception_handler(BackendExeption)
async def backend_exception_handler(request: Request, exc: BackendExeption):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict(),
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )


# Подключение роутера медиа к основному роутеру
api_router.include_router(media_router)

# Подключение роутера пользователей к основному роутеру
api_router.include_router(users_router)

# Подключение роутера твитов к основному роутеру
api_router.include_router(tweets_router)

# Подключаем основной роутер к приложению
app.include_router(api_router, prefix="/api")


if __name__ == "__main__":
    logger.info("Запуск осуществлен")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
