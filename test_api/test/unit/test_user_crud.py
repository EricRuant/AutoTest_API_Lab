import pytest_asyncio
import pytest
from test_api.clients.api_httpx_unit import (
    async_response_post, async_response_patch, async_response_put, async_response_delete, async_response_get
)
from test_api.test.unit.helpers.test_user_crud_assertions import (
    assert_post_success, assert_update_success, assert_delete_success, assert_get_success
)

@pytest_asyncio.fixture
async def success_user_id():
    return {
        "username": "eric",
        "email": "eric@example.com",
        "password": "123456"
    }

@pytest_asyncio.fixture
async def success_user_patch():
    return {
        "username": "new_eric",
        "password": "123456"
    }

@pytest_asyncio.fixture
async def success_user_put():
    return {
        "username": "new_eric",
        "email": "new_eric@example.com",
        "password": "new_123456"
    }

@pytest.mark.asyncio
async def test_success_user_id(success_user_id, success_user_patch, success_user_put, test_session, client):
    # 建立使用者
    response = await async_response_post(success_user_id, client)
    await assert_post_success(response, test_session)

    user_id = response.json()["id"]

    # PATCH 更新使用者部分欄位
    response = await async_response_patch(user_id, success_user_patch, client)
    await assert_update_success(response, test_session)

    # PUT 覆蓋使用者欄位
    response = await async_response_put(user_id, success_user_put, client)
    await assert_update_success(response, test_session)

    # GET 取得更新後的使用者
    response = await async_response_get(user_id, client)
    await assert_get_success(response, test_session)

    # DELETE 使用者
    response = await async_response_delete(user_id, client)
    await assert_delete_success(response, user_id, test_session)