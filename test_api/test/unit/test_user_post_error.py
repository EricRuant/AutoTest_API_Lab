# httpx + pytest

# 匯入 pytest 與封裝過的 TestClient 測試工具函式
import pytest
import pytest_asyncio  
from test_api.clients.api_httpx_unit import async_response_post, async_response_delete

# 匯入斷言模組，檢查回傳資料正確性與錯誤碼
from test_api.test.unit.helpers.test_user_post_error_assertions import (
    assert_response_success,            # 成功建立回應驗證
    assert_response_fail_400_email,     # 重複資料錯誤驗證
    assert_response_fail_400_username,  # 重複資料錯誤驗證
    assert_response_fail_422            # 欄位格式錯誤驗證
)

pytestmark = pytest.mark.asyncio()

# =======================
# 成功測試資料（註冊用）
# =======================
@pytest_asyncio.fixture
async def success_user_id():
    return {
        "username": "eric",
        "email": "eric@example.com",
        "password": "123456"
    }

# =======================
# 重複測試資料組合（用來測試 username/email 重複情況）
# =======================
duplicate_test_cases_email = [
    {"username": "eric1", "email": "eric@example.com"},
    {"username": "eric2", "email": "eric@example.com"},
    {"username": "eric3", "email": "eric@example.com"},
]

duplicate_test_cases_username = [
    {"username": "eric", "email": "eric1@example.com"},
    {"username": "eric", "email": "eric2@example.com"},
    {"username": "eric", "email": "eric3@example.com"},
]

# =======================
# 欄位驗證失敗測試資料
# =======================
invalid_users = [
    pytest.param({"username": "eric", "email": "test1@example.com", "password": "123"}, "password", id="password 長度不足"),
    pytest.param({"username": "e", "email": "test1@example.com", "password": "123456"}, "username", id="username 長度不足"),
    pytest.param({"username": "eric", "email": "not-an-email", "password": "123456"}, "email", id="不合法 email 格式"),
]

# =======================
# 測試：成功建立使用者
# =======================
async def test_success_user_id(success_user_id, test_session, client):
    response = await async_response_post(success_user_id, client)
    await assert_response_success(response, test_session)

    user_id = response.json()["id"]
    await async_response_delete(user_id, client)

# =======================
# 測試：重複 email 時回傳 400
# =======================
@pytest.mark.parametrize("user_data", duplicate_test_cases_email)
async def test_400_user_id_email(default_user, user_data, client):
    data = user_data.copy()
    data["password"] = "12345678"  # 確保通過密碼驗證
    response = await async_response_post(data, client)
    await assert_response_fail_400_email(response)

# =======================
# 測試：重複 username 時回傳 400
# =======================
@pytest.mark.parametrize("user_data", duplicate_test_cases_username)
async def test_400_user_id_username(default_user, user_data, client):
    data = user_data.copy()
    data["password"] = "12345678"  # 確保通過密碼驗證
    response = await async_response_post(data, client)
    await assert_response_fail_400_username(response)

# =======================
# 測試：欄位格式錯誤，應回傳 422
# =======================
@pytest.mark.parametrize("user_from, error_msg", invalid_users)
async def test_422_user_id(user_from, error_msg, client):
    response = await async_response_post(user_from, client)
    await assert_response_fail_422(response, error_msg)