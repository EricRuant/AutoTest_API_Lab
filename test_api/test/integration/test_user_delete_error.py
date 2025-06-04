import pytest
from test_api.clients.api_httpx_integration import async_response_delete
from test_api.test.integration.helpers.test_user_delete_error_assertions import (
    assert_response_success,
    assert_response_fail_422,
    assert_response_fail_404
)

pytestmark = pytest.mark.asyncio()

# 測試用不存在的 UUID（格式正確但 DB 中查無此人）
not_found_ids = [
    "1a1c548b-fc30-49ab-9fd9-14f780ab8911",
    "1a1c548b-fc30-49ab-9fd9-14f780ab8912",
    "1a1c548b-fc30-49ab-9fd9-14f780ab8914",
]

# 測試用錯誤格式的 UUID（會導致 422）
malformed_ids = ["1", "12", "123", "1-2", "1-2-3"]

async def test_success_user_id(default_user, get_test_session):
    """
    ✅ 測試成功刪除一位存在的使用者 → 應回傳 204
    """
    user_id = default_user["id"]
    response = await async_response_delete(user_id)
    await assert_response_success(response, user_id, get_test_session)

@pytest.mark.parametrize("not_found_id", not_found_ids)
async def test_404_user_id(not_found_id):
    """
    ✅ 測試合法 UUID 但不存在 → 應回傳 404
    """
    response = await async_response_delete(not_found_id)
    await assert_response_fail_404(response)

@pytest.mark.parametrize("malformed_id", malformed_ids)
async def test_422_user_id(malformed_id):
    """
    ✅ 測試 UUID 格式錯誤 → 應回傳 422
    """
    response = await async_response_delete(malformed_id)
    await assert_response_fail_422(response, malformed_id)