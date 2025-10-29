"""Contains database configurations"""

from decouple import config
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

# Create Async Engine
engine = create_async_engine(url=config("DB_URL"), echo=True, future=True)

# Create the Sessionmaker
Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:  # type: ignore
    """Provides an asynchronous SQLModel session."""
    async with Session() as session:
        yield session


async def init_db() -> None:
    """ "Initialize the database"""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
