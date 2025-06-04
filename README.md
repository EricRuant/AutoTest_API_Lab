# 專案名稱: AutoTest_API_Lab

## 1️⃣ 專案簡介

此專案是一個使用 **FastAPI + SQLAlchemy + Pydantic** 展示建立基礎 CRUD API 的專案。配合 **httpx + pytest** 啟用內建與實際伺服器的自動化測試，並展示 **pytest-html** 產生測試報告與 **GitHub Actions CI** 整合。

---

## 2️⃣ 專案功能

* [x] FastAPI RESTful API CRUD (創建、查詢、更新、刪除)
* [x] 資料驗證與錯誤處理
* [x] bcrypt 加密密碼
* [x] 內建 SQLite 資料庫做為測試環境
* [x] pytest + httpx 單元與整合測試
* [x] pytest-html 產生 HTML 測試報告
* [x] GitHub Actions 自動化 CI 測試

---

## 3️⃣ 專案目的
本專案為自學 FastAPI + SQLAlchemy + Pytest 測試流程的練習，涵蓋以下內容：

- 路由與 CRUD 操作實作
- SQLAlchemy ORM 非同步資料庫操作
- 使用 bcrypt 加密密碼欄位
- 使用 httpx + pytest 建立整合測試
- 自動產生 pytest-html 測試報告
- 使用 GitHub Actions 整合自動化測試流程

---

## 4️⃣ 環境需求

* Python 3.11+
* FastAPI
* SQLAlchemy
* Pydantic
* MySQL / SQLite (測試)
* httpx (測試)
* pytest (測試)

---

## 5️⃣ 安裝與執行

```bash
# 下載專案
git clone https://github.com/EricRuant/AutoTest_API_Lab.git

# 進入專案目錄
cd AutoTest_API_Lab

# 安裝依賴
pip install -r requirements.txt
```

環境變數設定
- 請將 `.env.example` 改為 `.env`

啟動 FastAPI 伺服器
```bash
uvicorn api.api_main:app --reload
```

伺服器啟動後，開啟瀏覽器並前往：
- API Docs: http://127.0.0.1:8000/docs

---

## 6️⃣ API 端點測試方式

### 端點列表

* `POST   /users/` - 創建使用者
* `GET    /users/{id}` - 查詢指定 ID 
* `PATCH  /users/{id}` - 部分更新
* `PUT    /users/{id}` - 整個更新
* `DELETE /users/{id}` - 刪除使用者

### 執行測試 + 產生 HTML + 測試覆蓋率（coverage）報告

```bash
# 啟動測試專用伺服器
uvicorn test_app.test_main:app --reload

# 執行測試
pytest --cov=api --cov-report=term --cov-report=html --html=report.html
```

### 測試覆蓋情境
-  GET 所有資料（成功）
- POST 新增資料（成功與重複錯誤）
- PUT 修改資料（成功與資料不存在）
- DELETE 刪除（成功與資料不存在）
- 資料驗證錯誤（缺欄位、自定義驗證錯誤）

---

## 7️⃣ 未來改進項目

* [ ] JWT 認證 / 認證安全性
* [ ] /me 取得當前登入用戶 API
* [ ] Admin/普通用戶親和認證權限
* [ ] Middleware: 總統 log 、request\_id 追蹤
* [ ] 圖片上傳與服務器儲存
* [ ] 詳細錯誤確認與自訂錯誤導向

---

## 8️⃣ 參考資源

* [FastAPI Docs](https://fastapi.tiangolo.com/)
* [httpx Docs](https://www.python-httpx.org/)
* [pytest](https://docs.pytest.org/en/stable/)
* [pytest-asyncio](https://github.com/pytest-dev/pytest-asyncio)
* [pytest-html](https://pypi.org/project/pytest-html/)
* [GitHub Actions Docs](https://docs.github.com/en/actions)

---

