import pytest_asyncio
from httpx import AsyncClient
from test_app.db.test_session import engine
from sqlalchemy.ext.asyncio import AsyncSession

# 匯入 asyncio 模組與系統平台判斷
import asyncio
import sys

# ==========================================
# ✅ Windows 專用：指定事件迴圈，避免 asyncmy 出錯
# ==========================================
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

@pytest_asyncio.fixture
async def client():
    async with AsyncClient(base_url="http://127.0.0.1:8000") as client:
        yield client

@pytest_asyncio.fixture(scope="function")
async def get_test_session():
    async with AsyncSession(engine) as session:
        yield session  # ✅ yield 出去給測試用
        # 測試完後自動關閉 session
# 每次測試前提供一個獨立 session。
# 測試後自動釋放，不會造成資源洩漏。
# ✅ 配合 engine（來自測試資料庫）自動管理連線。

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

    # 測試後清除該使用者
    try:
        res = await client.delete(f"/users/{user['id']}")
        assert res.status_code in [200, 204, 404], f"刪除預設使用者失敗：{res.status_code} {res.text}"
    except Exception as e:
        print(f"⚠️ 無法刪除 default_user：{e}")