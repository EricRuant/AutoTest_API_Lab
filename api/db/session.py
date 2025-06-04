# api/db/session.py

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase


# 🚨 非同步用的連線字串需要用 async driver，例如 aiomysql
DATABASE_URL = "mysql+aiomysql://myuser:zxcv123@localhost:3306/my_database"

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


# ✅ 重點說明：
# 元件	                    解釋
# create_async_engine	    使用 aiomysql 作為非同步驅動
# async_sessionmaker	    建立非同步 Session 工廠（取代舊的 Session）
# @asynccontextmanager	    用來實現 async with 的 yield session
# Base(DeclarativeBase)	    提供給 models 繼承使用，等下 models.py 會改用這個


# IDE 顯示 AsyncSession 有黃色底線或波浪線標示，通常是因為「型別提示工具」（像是 Pyright、Pylance、mypy 等）的一個限制或推論誤判。
# 🟡 為何會顯示錯誤提示？
# 原因一：yield + async def 搭配 -> AsyncSession 有時不被靜態分析器完全理解
# FastAPI 會自動辨識 async generator 並處理 yield 出來的值，但某些型別檢查工具會誤以為你是 回傳一個 async generator，所以它希望你註明型別是：
# from collections.abc import AsyncGenerator
# async def get_session() -> AsyncGenerator[AsyncSession, None]:
#     ...
# 但這樣其實沒必要，FastAPI 可以正確處理你原本的寫法。