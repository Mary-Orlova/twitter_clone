class BackendExeption(Exception):
    """
    Кастомное исключение для обработки ошибок в бизнес-логике.

    :param error_type: Тип ошибки
    :param error_message: Описание ошибки для пользователя
    """

    def __init__(
        self,
        error_type: str,
        error_message: str,
        status_code: int = 404,
        *args,
        **kwargs,
    ):
        super().__init__(*args)
        self.result = False
        self.error_type = error_type
        self.error_message = error_message
        self.status_code = status_code

    def __repr__(self) -> str:
        """
        Возвращает строковое представление ошибки
        """
        return (
            f"BackendExeption(result={self.result}, "
            f"error_type='{self.error_type}', "
            f"error_message='{self.error_message}')"
        )

    def __str__(self) -> str:
        """
        Возвращает строку для вывода пользователю
        """
        return f"[{self.error_type}] {self.error_message}"

    def to_dict(self) -> dict:
        """
        Возвращает ошибку в виде словаря
        """
        return {
            "result": self.result,
            "error_type": self.error_type,
            "error_message": self.error_message,
        }
