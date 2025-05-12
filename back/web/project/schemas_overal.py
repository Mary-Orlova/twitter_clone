from pydantic import BaseModel


class ErrorSchema(BaseModel):
    """
    Схема ошибки для ответа API.

    :param result: Флаг неуспешного выполнения операции (по умолчанию False).
    :param error_type: Тип ошибки.
    :param error_message: Сообщение об ошибке.
    """

    result: bool = False
    error_type: str
    error_message: str

    class Config:
        from_attributes = True


class OnlyResult(BaseModel):
    """
    Схема для ответа с булевым результатом.

    :param result: Флаг выполнения операции.
    """

    result: bool
