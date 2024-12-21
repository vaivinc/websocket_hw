from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow"
    )

    DEBUG: bool = False
    HOST: str = "localhost"
    PORT: str = "8000"

    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_NAME: str = "temp"

    SECRET_KEY: str = "secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MIN: int = 1

    def pg_dsn(self):
        return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
                f"@localhost:5432/{self.DB_NAME}")

    def sqlite_dsn(self):
        return f"sqlite:///./{self.DB_NAME}.db"


settings_app = Settings()

DATABASE_URL = settings_app.pg_dsn()

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(bind=engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


async def get_session():
    async with async_session() as sess:
        yield sess