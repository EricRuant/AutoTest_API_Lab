# test_app/test_session.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# ✅ 非同步測試用的連線字串
DATABASE_URL = "sqlite+aiosqlite:///./test.db"  # 可改為 :memory:

# ✅ 建立 async engine
engine = create_async_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=True
)

# ✅ 建立 async session factory
async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# ✅ 非同步 session 依賴
async def get_test_session():
    async with async_session_maker() as session:
        yield session