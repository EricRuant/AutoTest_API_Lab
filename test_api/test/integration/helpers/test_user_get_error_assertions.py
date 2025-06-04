import re
from uuid import UUID
from test_api.test.integration.helpers.test_user_sql_assertions import (
    assert_response
)

# === ISO 8601 格式的正規表達式 ===
ISO = re.compile(
    r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?'
)

async def assert_response_success(response, session):
    assert response.status_code == 200
    data = response.json()

    assert "id" in data                 # 必須包含 id 欄位
    assert UUID(data["id"])            # 驗證是否為合法 UUID 格式
    uuid_obj = UUID(data["id"])
    assert uuid_obj.version == 4        # 確認 UUID 為 v4

    assert ISO.fullmatch(data["created_at"])  # 驗證時間格式
    assert "password" not in data      # 回應中不應包含密碼欄位（保密）

    user_id = data["id"]
    user_email = data["email"]
    user_username = data["username"]
    await assert_response(user_id, user_username, user_email, session)

# === 查詢不存在使用者時的 404 錯誤驗證 ===
async def assert_response_fail_404(response):
    assert response.status_code == 404  # 回傳應為 404 Not Found
    assert response.json()["detail"] == "User not found"

async def assert_response_fail_422(response, user_id):
    assert response.status_code == 422
    details = response.json().get("detail", [])[0]

    assert details["loc"] == ["path", "id"] 
    assert details["type"] == "uuid_parsing"
    assert "uuid" in details["msg"].lower()           # 錯誤訊息中應提到 uuid
    assert str(user_id) in details["input"]            # 回應中應包含原始輸入 ID