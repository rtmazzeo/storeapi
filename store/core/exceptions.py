class BaseException(Exception):
    """Exceção base para erros customizados."""
    
    message: str = "Internal Server Error"
    status_code: int = 500  # Código de status HTTP padrão

    def __init__(self, message: str | None = None, status_code: int | None = None) -> None:
        if message:
            self.message = message
        if status_code:
            self.status_code = status_code

        super().__init__(self.message)

    def __str__(self) -> str:
        return f"{self.status_code}: {self.message}"


class NotFound(BaseException):
    """Exceção lançada quando um recurso não é encontrado."""

    message: str = "Not Found"
    status_code: int = 404


class InsertError(BaseException):
    """Exceção lançada quando ocorre um erro ao inserir dados."""
    
    message: str = "Erro ao inserir dados"
    status_code: int = 500  # Ou 422 para "Unprocessable Entity" (dados inválidos)
