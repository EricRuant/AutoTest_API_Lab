import pytest_asyncio
from api.api_main import app

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

import asyncio
import sys

from httpx import AsyncClient

from api.api_main import app 
from api.db.session import Base, get_session  

# ✅ 建立 async SQLite 測試引擎
DATABASE_URL = "sqlite+aiosqlite:///:memory:"
test_engine = create_async_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False
)

# ✅ 建立 async session factory
TestSessionLocal = async_sessionmaker(bind=test_engine, expire_on_commit=False)

# ==========================================
# ✅ Windows 專用：指定事件迴圈，避免 asyncmy 出錯
# ✅ 為解決 Windows 下 asyncio 相關套件相容問題
# ==========================================
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# ✅ 建立測試用資料表
@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_test_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# 提供測試用的 async session
@pytest_asyncio.fixture
async def test_session():
    async with TestSessionLocal() as session:
        yield session

# httpx 測試客戶端（非同步、FastAPI 綁定、覆蓋依賴）
@pytest_asyncio.fixture
async def client(test_session):
    async def override_get_session():
        yield test_session
    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c

# fixture：預設使用者（建立與清理）
@pytest_asyncio.fixture(scope="function")
async def default_user(client):
    user_data = {
        "username": "eric",
        "email": "eric@example.com",
        "password": "abc123456"
    }

    # 嘗試刪除相同 email 的舊資料（如果 API 支援的話）
    try:
        res = await client.post(f"/users/", json=user_data)
        assert res.status_code == 201, res.text
        user = res.json()
    except Exception as e:
        raise RuntimeError(f"建立 default_user 發生錯誤：{e}")

    yield user 

    # 測試結束後刪除該使用者（清理資源）
    try:
        res = await client.delete(f"/users/{user['id']}")
        assert res.status_code in [200, 204, 404], f"刪除預設使用者失敗：{res.status_code} {res.text}"
    except Exception as e:
        print(f"⚠️ 無法刪除 default_user：{e}")
