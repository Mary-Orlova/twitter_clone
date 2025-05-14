"""
Роут FastAPI для работы с медиафайлами (картинками).
"""

from pathlib import Path
from typing import Union

import aiofiles
from fastapi import APIRouter, Depends, Header, Response, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..exeptions import BackendExeption
from ..media.media_services import check_file, post_image
from ..media.schemas import MediaOutSchema
from ..schemas_overal import ErrorSchema

router = APIRouter(prefix="/medias", tags=["Medias"])

# Папка для сохранения файлов
# OUT_PATH = (Path(__file__).parent / "media_files").absolute()
# PREFIX_NAME = "/static/media_files/"
OUT_PATH = Path("/usr/src/app/media/media_files") # Абсолютный путь внутри контейнера
PREFIX_NAME = "/media_files/"


@router.post(
    "/",
    summary="Загрузка изображений для твита пользователя",
    response_description="Результат загрузки изображения",
    response_model=Union[MediaOutSchema, ErrorSchema],
    status_code=200,
)
async def post_image_handler(
    response: Response,
    file: UploadFile,
    api_key: str = Header(),
    session: AsyncSession = Depends(get_session),
) -> Union[MediaOutSchema, ErrorSchema]:
    """
    Метод загрузки изображения для пользователя.

    :param response: Ответ сервера.
    :param file: Загружаемый файл.
    :param api_key: Ключ API.
    :param session: Асинхронная сессия.
    :return: Результат загрузки или ошибка.
    """
    try:
        # Проверка файла на поддерживаемый формат
        check_file(file)

        filename = file.filename

        # Проверка на наличие папки и создание при необходимости
        OUT_PATH.mkdir(parents=True, exist_ok=True)
        path = OUT_PATH / filename

        # Асинхронная запись файла
        async with aiofiles.open(path, mode="wb") as some_file:
            await some_file.write(await file.read())

        name_for_db = f"{PREFIX_NAME}{filename}"

        # Сохранение информации о файле в базе данных
        return await post_image(session=session, image_name=name_for_db)
    except BackendExeption as error:
        response.status_code = 400
        return error
