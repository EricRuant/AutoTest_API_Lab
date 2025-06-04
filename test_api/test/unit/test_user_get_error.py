import pytest
from test_api.clients.api_httpx_unit import async_response_get
from test_api.test.unit.helpers.test_user_get_error_assertions import (
    assert_response_success,
    assert_response_fail_404,
    assert_response_fail_422
)

pytestmark = pytest.mark.asyncio()

async def test_success_user_id(default_user, test_session, client):
    """
    ✅ 測試成功查詢一筆存在的使用者資料，應回傳 200 OK
    """
    user_id = default_user["id"]
    response = await async_response_get(user_id, client)
    await assert_response_success(response, test_session)

@pytest.mark.parametrize("not_found_id", [
    "e1f47c61-8045-490b-b5f6-fda27f0e9b94",
    "e1f47c61-8045-490b-b5f6-fda27f0e9b96",
    "e1f47c61-8045-490b-b5f6-fda27f0e9b97",
])
async def test_404_user_id(not_found_id, client):
    """
    ✅ 測試合法 UUID 但查無資料，應回傳 404
    """
    response = await async_response_get(not_found_id, client)
    await assert_response_fail_404(response)

@pytest.mark.parametrize("invalid_id", ["1", "12", "1-2", "not-a-uuid"])
async def test_422_user_id(invalid_id, client):
    """
    ✅ 測試 UUID 格式錯誤，應回傳 422
    """
    response = await async_response_get(invalid_id, client)
    await assert_response_fail_422(response, invalid_id)