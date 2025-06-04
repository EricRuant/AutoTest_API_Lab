from test_api.test.unit.helpers.test_user_sql_assertions import (
    assert_response_delete
)

# 成功回應驗證（HTTP 204 No Content）
async def assert_response_success(response, user_id, session):
    assert response.status_code == 204                
    assert response.content == b""                    
    await assert_response_delete(user_id, session)
    

# UUID 格式錯誤時應回傳 422 Unprocessable Entity
async def assert_response_fail_422(response, user_id):
    assert response.status_code == 422

    details = response.json().get("detail", [])[0]

    assert details, "沒有回傳錯誤細節"
    assert details["loc"] == ["path", "id"]
    assert details["type"] == "uuid_parsing"
    assert "uuid" in details["msg"].lower()
    assert str(user_id) in details["input"]

# 查無使用者資料，應回傳 404 Not Found
async def assert_response_fail_404(response):
    assert response.status_code == 404

    assert response.json()["detail"] == "User not found"
