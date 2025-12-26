from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from config import settings


engine = create_async_engine(
    settings.DATABASE_URL(is_async=True), 
    echo=False
) 

async_session = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=True
)
