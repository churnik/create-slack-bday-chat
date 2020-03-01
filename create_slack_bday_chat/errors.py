from loguru import logger

__all__ = ["BaseAppException", "WrongNumberOfArgumentsException"]


class BaseAppException(Exception):
    def __init__(self, message: str = "") -> None:
        super().__init__(message)
        self.message = message
        logger.trace("Exception '{}' was raised. {}.", self.__class__.__name__, self.message)

    @property
    def error_code(self) -> int:
        raise NotImplementedError(
            "Error code should be implemented. Choose one from "
            "https://wiki.math.bio/x/AgBkAw#id-СозданиеиописаниеRESTAPI-Окодахошибок"
        )

    def to_dict(self) -> dict:
        raise NotImplementedError("`to_dict` is not implemented.")


class WrongNumberOfArgumentsException(BaseAppException):
    @property
    def error_code(self) -> int:
        return 200

    def to_dict(self) -> dict:
        return {"response_type": "in_channel", "text": "Wrong number of arguments"}


class UnauthorizedException(BaseAppException):
    @property
    def error_code(self) -> int:
        return 400

    def to_dict(self) -> dict:
        return {"error": "Unauthorized"}
