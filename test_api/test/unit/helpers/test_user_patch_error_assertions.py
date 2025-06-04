import re
from uuid import UUID
from test_api.test.unit.helpers.test_user_sql_assertions import (
    assert_response
)

# === 正規表達式：驗證 ISO 8601 時間格式 ===
ISO = re.compile(
    r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?'
)

# === 成功更新使用者的驗證函式 ===
async def assert_response_success(response, session):
    assert response.status_code == 200  # 成功應回傳 200 OK
    data = response.json()

    assert "id" in data
    assert UUID(data["id"])           # 驗證 UUID 格式正確
    uuid_obj = UUID(data["id"])
    assert uuid_obj.version == 4       # 應為 UUIDv4

    assert ISO.fullmatch(data["created_at"])  # 檢查時間格式
    assert "password" not in data      # 不應回傳密碼

    user_id = data["id"]
    user_email = data["email"]
    user_username = data["username"]
    await assert_response(user_id, user_username, user_email, session)

async def assert_response_repeat_success(response, user_id):
    assert response.status_code == 200
    print(response.json())
    assert response.json()["message"] == "No changes detected"
    assert response.json()["data"]["id"] == user_id

# === 查無使用者（404 Not Found） ===
async def assert_response_fail_404(response):
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


# === 欄位格式錯誤（422 Unprocessable Entity） ===
async def assert_response_fail_422(response, expected_error_key):
    assert response.status_code == 422
    details = response.json().get("detail", [])

    assert details, "No error details returned"  # 確保有錯誤內容

    # 將預期欄位轉為 set 格式處理
    if isinstance(expected_error_key, str):
        expected_error_key = {expected_error_key}
    elif isinstance(expected_error_key, list):
        expected_error_key = set(expected_error_key)
    else:
        raise TypeError("expected_error_key must be str or list[str]")

    # 從錯誤資訊中擷取實際出錯欄位名稱
    actual_keys = {d["loc"][-1] for d in details}

    # 驗證是否每個預期錯誤欄位都有出現
    assert expected_error_key.issubset(actual_keys), f"Expected keys {expected_error_key} not found in {actual_keys}"

# === 查無使用者（403 Forbidden） ===
async def assert_response_fail_403(response, expected_error_key):
    assert response.status_code == 403
    assert response.json()["detail"] == f"Field '{expected_error_key}' is not allowed to be updated"

# === 白名單 (400 Bad Request) ===
async def assert_response_fail_400(response, expected_error_key):
    assert response.status_code == 400
    assert response.json()["detail"] == f"Field '{expected_error_key}' cannot be updated"


# === 附加說明 ===
# assert UUID(data["id"]): 用來驗證該字串是否為合法 UUID
# loc[-1]: 是為了從錯誤位置列表中取得最終欄位名稱（例如 ["body", "username"] 取 "username"）

# assert UUID(data["id"]) 是用來 檢查 data["id"] 是否為一個合法的 UUID 字串。
# from uuid import UUID
# 這個 UUID() 是 Python 標準函式庫 uuid 裡的一個類別。你可以用它來：
#   將字串轉換成 UUID 物件
#   驗證該字串格式是否符合 UUID 標準（如 UUID4）

# 🔒 assert UUID(data["id"]) 的含義：
#   這是一個 斷言（assert）。
#   如果 data["id"] 不是合法 UUID，UUID(data["id"]) 就會丟出 ValueError，導致測試失敗。
#   如果是合法 UUID，則斷言會通過，測試繼續。

# ❓為什麼是 ["loc"][-1]？
# ✅ 使用 [-1] 的意義：
# 取法	    取到的值	     適用情境
# loc[0]	"body"	        來源位置
# loc[1]	"password"	    一般欄位錯誤
# loc[-1]	最終錯誤欄位名	 ✅最常用、通用做法