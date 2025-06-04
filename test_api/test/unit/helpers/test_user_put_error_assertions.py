import re
from uuid import UUID

from test_api.test.unit.helpers.test_user_sql_assertions import (
    assert_response
)

# 正規表達式：驗證 ISO 8601 時間格式
ISO = re.compile(
    r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?'
)

# 成功更新使用者的驗證函式
async def assert_response_success(response, session):
    assert response.status_code == 200  
    data = response.json()

    assert "id" in data
    assert UUID(data["id"])           
    uuid_obj = UUID(data["id"])
    assert uuid_obj.version == 4       

    assert ISO.fullmatch(data["created_at"])  
    assert "password" not in data      

    user_id = data["id"]
    user_email = data["email"]
    user_username = data["username"]
    await assert_response(user_id, user_username, user_email, session)

async def assert_response_repeat_success(response, user_id):
    assert response.status_code == 200
    assert response.json()["message"] == "No changes detected"
    assert response.json()["data"]["id"] == user_id


# 查無使用者（404 Not Found）
async def assert_response_fail_404(response):
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


# 欄位格式錯誤（422 Unprocessable Entity）
async def assert_response_fail_422(response, expected_error_key):
    assert response.status_code == 422
    details = response.json().get("detail", [])

    assert details, "No error details returned"  

    if isinstance(expected_error_key, str):
        expected_error_key = {expected_error_key}
    elif isinstance(expected_error_key, list):
        expected_error_key = set(expected_error_key)
    else:
        raise TypeError("expected_error_key must be str or list[str]")

    actual_keys = {d["loc"][-1] for d in details}

    assert expected_error_key.issubset(actual_keys), f"Expected keys {expected_error_key} not found in {actual_keys}"
