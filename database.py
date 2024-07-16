from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker


class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 5435
    DB_USER: str = "postgres"
    DB_PASS: str = "postgres"
    DB_NAME: str = "app"


settings = Settings()

DATABASE_URL = (f'postgresql+psycopg2://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/'
                f'{settings.DB_NAME}')

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_session():
    return SessionLocal()


DATABASE_URL = (f'postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/'
                f'{settings.DB_NAME}')

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()


async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session
