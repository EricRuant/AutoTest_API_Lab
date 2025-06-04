import pytest
from pytest_html import extras

# === 自訂 HTML 測試報告的標題 ===
def pytest_html_report_title(report):
    report.title = "我的測試報告"

# === 在每一個測試的報告中加入附加說明與連結 ===
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":  # 只在 call 階段加入資料（即執行測試本體的時候）
        if not hasattr(report, "extras"):
            report.extras = []

    # 加入超連結與說明文字
    extra = getattr(report, "extras", [])
    extra.append(extras.url("http://127.0.0.1:8000/docs", name="查看文件"))
    extra.append(extras.html("測試 CRUD API 教學規格文件"))
    report.extras = extra


# 功能說明：
# 區塊	                        說明
# base_url()	                提供全專案共用的 API base URL
# pytest_html_report_title()	自訂 HTML 測試報告標題
# pytest_runtest_makereport()	自動在每個測試報告中加入提示與連結，提升可讀性


# 什麼是 sqlite:///:memory:？
# create_engine("sqlite:///:memory:")
#     它會在「記憶體中建立 SQLite 資料庫」，一旦關閉程式，就會 完全消失
#     所以它是一個「不會寫入檔案、不會殘留資料」的臨時資料庫


# 那 StaticPool 是什麼？
# poolclass=StaticPool
#     SQLite 預設一個連線關掉後，in-memory 資料庫就沒了
#     但測試過程中 Session() 每次都會產生新的連線
#     ➤ 所以你需要用 StaticPool，讓所有 session 共用一個記憶體連線！


# 什麼是 app.dependency_overrides[get_session] = override_get_session？
# 在 測試期間，把原本 app 中的 get_session() 改為 override_get_session()，也就是：
#   👇讓 FastAPI 所有 Depends(get_session) 變成：
#       Depends(override_get_session) → 回傳測試資料庫 session


# 🧠 預設情況：check_same_thread=True
# 行為	                                                          說明
# SQLite 預設只允許同一個 thread 使用連線物件	                    為了「資料安全性」與「記憶體模型一致性」
# 也就是說：建立連線的 thread 和使用連線的 thread 必須是同一個	     否則會報錯：sqlite3.ProgrammingError: SQLite objects created in a thread can only be used in that same thread.

# ⚠️ 在測試中為什麼會出錯？
#   TestClient、pytest、或 Session(engine) 可能會在不同 thread 中執行！
#       所以你會遇到報錯：SQLite object created in one thread, used in another thread

# 🔁 整體流程圖解（你這兩張圖對應）：
#     ✅ test_engine 建立 SQLite 記憶體資料庫（使用 StaticPool，共享記憶體）
#     ✅ test_session 使用 Session(test_engine) 與 DB 互動
#     ✅ client 覆寫 FastAPI 的 get_session 依賴，讓 TestClient 在測試時自動使用這個 session
#     ✅ TestClient(app) 不需要啟動伺服器就能測所有 API
#     ✅ 整個測試執行過程中，資料是「有記憶」的，直到 yield 結束

