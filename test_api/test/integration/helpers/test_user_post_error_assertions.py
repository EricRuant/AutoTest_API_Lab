import re
from uuid import UUID
from test_api.test.integration.helpers.test_user_sql_assertions import (
    assert_response
)

# =======================
# ISO 8601 格式驗證：用來驗證 created_at 欄位格式
# =======================
ISO = re.compile(
    r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?'
)

# =======================
# 驗證使用者建立成功的回應內容
# =======================
async def assert_response_success(response, session):
    assert response.status_code == 201  # HTTP 201 Created
    data = response.json()

    assert "id" in data                         # 檢查是否包含 id
    assert UUID(data["id"])                    # 驗證為合法 UUID
    assert UUID(data["id"]).version == 4       # UUID 版本為 v4

    assert data["username"] == "eric", "username should be 'eric'"
    assert data["email"] == "eric@example.com", "email should be 'eric@example.com'"
    assert ISO.fullmatch(data["created_at"])   # 驗證時間格式
    assert "password" not in data              # 不應回傳密碼欄位

    user_id = data["id"]
    user_username = data["username"]
    user_email = data["email"]
    await assert_response(user_id, user_username, user_email, session)

# =======================
# 驗證重複資料時應回傳 400 錯誤
# =======================
async def assert_response_fail_400_email(response):
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

# =======================
# 驗證重複資料時應回傳 400 錯誤
# =======================
async def assert_response_fail_400_username(response):
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"

# =======================
# 驗證欄位格式錯誤時應回傳 422，並檢查錯誤欄位與錯誤類型
# =======================
async def assert_response_fail_422(response, error_msg):
    assert response.status_code == 422
    details = response.json().get("detail", [])
    assert details, "No error details returned"

    # 預期錯誤欄位轉為 set，支援單欄位或多欄位錯誤
    if isinstance(error_msg, str):
        error_msg = {error_msg}
    elif isinstance(error_msg, list):
        error_msg = set(error_msg)
    else:
        raise TypeError("expected_error_key must be str or list[str]")

    # 擷取實際錯誤欄位名稱
    actual_keys = {d["loc"][-1] for d in details}
    assert error_msg.issubset(actual_keys), f"Expected keys {error_msg} not found in {actual_keys}"

    # 檢查欄位名稱對應的錯誤類型
    expected = {
        "username": "string_too_short",
        "password": "string_too_short",
        "email": "value_error",
    }
    for d in details:
        field = d["loc"][-1]
        error_type = d["type"]
        assert expected[field] == error_type, f"欄位 {field} 的 type 應為 {expected[field]}，實際為 {error_type}"

# ✅ 這些斷言函式可重複用於各類 FastAPI 測試中，增加一致性與可讀性