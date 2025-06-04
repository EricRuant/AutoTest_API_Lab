import re
from uuid import UUID
from test_api.test.unit.helpers.test_user_sql_assertions import (
    assert_response, assert_response_delete
)

# ISO 8601 格式驗證：用來驗證 created_at 欄位格式
ISO = re.compile(
    r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?'
)

# 驗證使用者建立成功的回應內容
async def assert_post_success(response, session):
    assert response.status_code == 201 
    data = response.json()

    assert "id" in data                         
    assert UUID(data["id"])                   
    assert UUID(data["id"]).version == 4      

    assert data["username"] == "eric", "username should be 'eric'"
    assert data["email"] == "eric@example.com", "email should be 'eric@example.com'"
    assert ISO.fullmatch(data["created_at"])  
    assert "password" not in data              

    user_id = data["id"]
    user_username = data["username"]
    user_email = data["email"]
    await assert_response(user_id, user_username, user_email, session)

# 成功更新使用者的驗證函式
async def assert_update_success(response, session):
    assert response.status_code == 200  
    data = response.json()

    assert "id" in data
    assert UUID(data["id"])          
    uuid_obj = UUID(data["id"])
    assert uuid_obj.version == 4       

    assert ISO.fullmatch(data["created_at"])  
    assert "password" not in data      

    user_id = data["id"]
    user_username = data["username"]
    user_email = data["email"]
    await assert_response(user_id, user_username, user_email, session)

async def assert_get_success(response, session):
    assert response.status_code == 200
    data = response.json()

    assert "id" in data                 
    assert UUID(data["id"])           
    uuid_obj = UUID(data["id"])
    assert uuid_obj.version == 4        

    assert ISO.fullmatch(data["created_at"])  
    assert "password" not in data    

    user_id = data["id"]
    user_username = data["username"]
    user_email = data["email"]
    await assert_response(user_id, user_username, user_email, session)

# 成功回應驗證（HTTP 204 No Content）
async def assert_delete_success(response, user_id, session):
    assert response.status_code == 204                
    assert response.content == b""                    

    await assert_response_delete(user_id, session)