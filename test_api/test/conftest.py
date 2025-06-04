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

    if report.when == "call":  
        if not hasattr(report, "extras"):
            report.extras = []

    # 加入超連結與說明文字
    extra = getattr(report, "extras", [])
    extra.append(extras.url("http://127.0.0.1:8000/docs", name="查看文件"))
    extra.append(extras.html("測試 CRUD API 教學規格文件"))
    report.extras = extra
