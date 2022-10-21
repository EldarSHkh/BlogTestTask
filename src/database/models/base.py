from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class DatabaseComponents:
    def __init__(self, connection_uri: str, **engine_kwargs) -> None:
        self.__engine_kwargs = engine_kwargs or {}
        self.engine = create_async_engine(url=connection_uri, **self.__engine_kwargs)
        self.sessionmaker = sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
        )
