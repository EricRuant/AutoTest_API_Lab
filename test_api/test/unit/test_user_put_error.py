import pytest
from test_api.clients.api_httpx_unit import async_response_put  
from test_api.test.unit.helpers.test_user_patch_error_assertions import (
    assert_response_success,        # 驗證成功更新
    assert_response_fail_404,       # 驗證查無此 ID
    assert_response_fail_422,       # 驗證欄位格式錯誤（長度不足）
    assert_response_repeat_success  # 驗證重複更新
)

pytestmark = pytest.mark.asyncio()

# 多筆測試資料（想測哪個欄位重複）
# ✅ 測試成功案例資料
success_data = [
    pytest.param({"username": "new_eric", "email": "new_eric@example.com", "password": "newpassword123"}, id="whole"),
    pytest.param({"username": "eric", "email": "new_eric@example.com", "password": "newpassword123"}, id="no put username"),
    pytest.param({"username": "new_eric", "email": "eric@example.com", "password": "newpassword123"}, id="no put email"),
    pytest.param({"username": "new_eric", "email": "new_eric@example.com", "password": "password123"}, id="no put password"),
]

# 測試重複使用者資料
repeat_success_data = [
    {"username": "eric", "email": "eric@example.com", "password": "abc123456"},
    {"username": "eric", "email": "eric@example.com", "password": "abc123456"},
    {"username": "eric", "email": "eric@example.com", "password": "abc123456"},
]

# 測試：成功更新使用者（狀態碼 200）
@pytest.mark.parametrize("user_data", success_data)
async def test_success_user_id(default_user, user_data, test_session, client):
    user_id = default_user["id"]
    response = await async_response_put(user_id, user_data, client)
    await assert_response_success(response, test_session)

# 測試：更新重複使用者（狀態碼 200）
@pytest.mark.parametrize("user_data", repeat_success_data)
async def test_success_repeat_user_id(default_user, user_data, client):
    user_id = default_user["id"]
    response = await async_response_put(user_id, user_data, client)
    await assert_response_repeat_success(response, user_id)

# 測試：不存在的 ID，應回傳 404
@pytest.mark.parametrize("user_id", [
    "e1f47c61-8045-490b-b5f6-fda27f0e9b94",
    "e1f47c61-8045-490b-b5f6-fda27f0e9b96",
    "e1f47c61-8045-490b-b5f6-fda27f0e9b97",
    "e1f47c61-8045-490b-b5f6-fda27f0e9b98",
    "e1f47c61-8045-490b-b5f6-fda27f0e9b99",
])
async def test_404_user_id(default_user, user_id, client):
    response = await async_response_put(user_id, {"username": "new_eric", "email": "new_eric@example.com", "password": "newpassword123"}, client)
    await assert_response_fail_404(response)

# 測試：欄位長度不足（422 Unprocessable Entity）
@pytest.mark.parametrize("username_password, expected_error_key", [
    ({"username": "new_eric", "email": "new_eric@example.com", "password": "1"}, "password"),
    ({"username": "1", "email": "new_eric@example.com", "password": "newpassword123"}, "username"),
    ({"username": "new_eric", "email": "error-email", "password": "newpassword123"}, "email"),
    ({"username": "1", "email": "new_eric@example.com", "password": "n"}, ["username", "password"]),
])
async def test_update_user_fail_422_due_to_short_fields(default_user, username_password, expected_error_key, client):
    user_id = default_user["id"]
    response = await async_response_put(user_id, username_password, client)
    await assert_response_fail_422(response, expected_error_key)

# 測試：嘗試修改 id（預期 422 錯誤）
@pytest.mark.parametrize("id, expected_error_key", [
    ({"id": "2b62a045-b93b-4986-9754-a65443488e96"}, ["username", "password", "email", "id"]),
    ({"id": "2b62a045-b93b-4986-9754-a65443488e95"}, ["username", "password", "email", "id"]),
    ({"id": "2b62a045-b93b-4986-9754-a65443488e94"}, ["username", "password", "email", "id"]),
    ({"id": "2b62a045-b93b-4986-9754-a65443488e93"}, ["username", "password", "email", "id"]),
])
async def test_put_fail_422_due_to_id_field(default_user, id, expected_error_key, client):
    user_id = default_user["id"]
    response = await async_response_put(user_id, id, client)
    await assert_response_fail_422(response, expected_error_key)