import pathlib

from pydantic import BaseSettings, PostgresDsn, validator

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent


class DbSettings(BaseSettings):
    test: bool
    test_pg_dsn: PostgresDsn
    pg_dsn: PostgresDsn

    @validator("pg_dsn")
    def set_pg_dsn(cls, v, values):
        if values["test"] is True:
            v = values["test_pg_dsn"]
            return v
        return v

    class Config:
        env_file = '.env.dev'
        env_file_encoding = 'utf-8'
