# test_api/test/unit/assertions.py
import re
from test_api.test.integration.helpers.test_user_sql_assertions import (
    assert_response_delete
)

# ✅ 建立正規表達式，驗證 ISO 8601 格式（目前未使用）
ISO = re.compile(
    r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?"
)

# ====================================================
# ✅ 成功回應驗證（HTTP 204 No Content）
# ====================================================
async def assert_response_success(response, user_id, session):
    assert response.status_code == 204                # 確保狀態碼為 204
    assert response.content == b""                    # 回應內容應為空（符合 204 定義）
    await assert_response_delete(user_id, session)
    

# ====================================================
# ✅ UUID 格式錯誤時應回傳 422 Unprocessable Entity
# ====================================================
async def assert_response_fail_422(response, user_id):
    assert response.status_code == 422

    # 提取錯誤資訊中的第一個 detail（FastAPI 對 ValidationError 的格式）
    details = response.json().get("detail", [])[0]

    # 驗證 detail 是否有值
    assert details, "沒有回傳錯誤細節"

    # 應該是 path 中的 id 欄位錯誤
    assert details["loc"] == ["path", "id"]

    # FastAPI 對 UUID 格式錯誤的 type 命名為 uuid_parsing
    assert details["type"] == "uuid_parsing"

    # 錯誤訊息應提及 uuid 字樣
    assert "uuid" in details["msg"].lower()

    # 原始輸入值應該出現在錯誤訊息中
    assert str(user_id) in details["input"]

# ====================================================
# ✅ 查無使用者資料，應回傳 404 Not Found
# ====================================================
async def assert_response_fail_404(response):
    assert response.status_code == 404

    # FastAPI 預設使用 "detail" 字段傳送錯誤資訊
    assert response.json()["detail"] == "User not found"
