from dotenv import load_dotenv
import os

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase


# 🚨 非同步用的連線字串需要用 async driver，例如 aiomysql
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")

# 建立 async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# 建立 async session factory
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

# 非同步 Base 類別（提供給 models 繼承）
class Base(DeclarativeBase):
    pass

# 非同步的 session 依賴注入函式
async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

