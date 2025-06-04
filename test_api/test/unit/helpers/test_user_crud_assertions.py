import re
from uuid import UUID
from test_api.test.unit.helpers.test_user_sql_assertions import (
    assert_response, assert_response_delete
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
async def assert_post_success(response, session):
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

# === 成功更新使用者的驗證函式 ===
async def assert_update_success(response, session):
    assert response.status_code == 200  # 成功應回傳 200 OK
    data = response.json()

    assert "id" in data
    assert UUID(data["id"])           # 驗證 UUID 格式正確
    uuid_obj = UUID(data["id"])
    assert uuid_obj.version == 4       # 應為 UUIDv4

    assert ISO.fullmatch(data["created_at"])  # 檢查時間格式
    assert "password" not in data      # 不應回傳密碼

    user_id = data["id"]
    user_username = data["username"]
    user_email = data["email"]
    await assert_response(user_id, user_username, user_email, session)

async def assert_get_success(response, session):
    assert response.status_code == 200
    data = response.json()

    assert "id" in data                 # 必須包含 id 欄位
    assert UUID(data["id"])            # 驗證是否為合法 UUID 格式
    uuid_obj = UUID(data["id"])
    assert uuid_obj.version == 4        # 確認 UUID 為 v4

    assert ISO.fullmatch(data["created_at"])  # 驗證時間格式
    assert "password" not in data      # 回應中不應包含密碼欄位（保密）

    user_id = data["id"]
    user_username = data["username"]
    user_email = data["email"]
    await assert_response(user_id, user_username, user_email, session)

# ====================================================
# ✅ 成功回應驗證（HTTP 204 No Content）
# ====================================================
async def assert_delete_success(response, user_id, session):
    assert response.status_code == 204                # 確保狀態碼為 204
    assert response.content == b""                    # 回應內容應為空（符合 204 定義）

    await assert_response_delete(user_id, session)