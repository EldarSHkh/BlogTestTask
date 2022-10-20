class DbError(Exception):
    def __init__(self, exc: Exception):
        self.exc = exc

    def __str__(self) -> str:
        return f"<Exception DbError message={self.exc}>. Original exception traceback:" + self.exc.__str__()
