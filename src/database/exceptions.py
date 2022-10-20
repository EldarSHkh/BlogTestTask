class DbError(Exception):
    def __init__(self, exc: Exception):
        self.exc = exc

    def __str__(self) -> str:
        return f"<Exception {self} message={self.exc}>. Original exception traceback:" + self.exc.__str__()
