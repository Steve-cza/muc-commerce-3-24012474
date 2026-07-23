"""
Day 07 Flask 自动化测试 (拓展C)
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ==================== 登录测试 ====================
class TestLogin:
    def test_index_shows_login(self, client):
        resp = client.get("/")
        assert resp.status_code == 200
        html = resp.data.decode("utf-8", errors="ignore")
        assert "登录" in html or "login" in html.lower()

    def test_correct_login(self, client):
        resp = client.post("/login", data={"username": "student", "password": "day07"}, follow_redirects=False)
        assert resp.status_code in [302, 200]

    def test_wrong_password(self, client):
        resp = client.post("/login", data={"username": "student", "password": "wrong"}, follow_redirects=False)
        assert resp.status_code == 401

    def test_unauthorized_dashboard(self, client):
        resp = client.get("/dashboard", follow_redirects=False)
        assert resp.status_code in [302, 401]


# ==================== 看板测试 ====================
class TestDashboard:
    def test_dashboard_after_login(self, client):
        client.post("/login", data={"username": "student", "password": "day07"})
        resp = client.get("/dashboard")
        assert resp.status_code == 200
        html = resp.data.decode("utf-8", errors="ignore")
        assert "指标" in html or "Metric" in html or "Dashboard" in html


# ==================== 问答测试 ====================
class TestQA:
    def _login(self, client):
        client.post("/login", data={"username": "student", "password": "day07"})

    def test_ask_total_users(self, client):
        self._login(client)
        resp = client.post("/api/ask", json={"question": "系统中有多少用户？"})
        assert resp.status_code == 200
        data = resp.get_json()
        assert "answer" in data and len(data["answer"]) > 0

    def test_ask_churn_rate(self, client):
        self._login(client)
        resp = client.post("/api/ask", json={"question": "总体流失率是多少？"})
        assert resp.status_code == 200
        data = resp.get_json()
        assert "%" in data["answer"]

    def test_ask_top_category(self, client):
        self._login(client)
        resp = client.post("/api/ask", json={"question": "哪个品类用户最多？"})
        assert resp.status_code == 200
        data = resp.get_json()
        assert "answer" in data

    def test_ask_lifecycle_risk(self, client):
        self._login(client)
        resp = client.post("/api/ask", json={"question": "哪个阶段风险最高？"})
        assert resp.status_code == 200
        data = resp.get_json()
        assert "answer" in data

    def test_ask_avg_orders(self, client):
        self._login(client)
        resp = client.post("/api/ask", json={"question": "平均订单数是多少？"})
        assert resp.status_code == 200
        data = resp.get_json()
        assert "answer" in data

    def test_unsupported_question(self, client):
        self._login(client)
        resp = client.post("/api/ask", json={"question": "今天天气怎么样？"})
        assert resp.status_code == 200
        data = resp.get_json()
        assert "不支持" in data["answer"] or "抱歉" in data["answer"]


# ==================== 筛选与下载测试 ====================
class TestFilterAndDownload:
    def _login(self, client):
        client.post("/login", data={"username": "student", "password": "day07"})

    def test_filter_all(self, client):
        self._login(client)
        resp = client.get("/dashboard?category=all")
        assert resp.status_code == 200

    def test_filter_fashion(self, client):
        self._login(client)
        resp = client.get("/dashboard?category=Fashion")
        assert resp.status_code == 200

    def test_download_csv(self, client):
        self._login(client)
        resp = client.get("/download?category=all")
        assert resp.status_code == 200
        assert "csv" in resp.content_type


# ==================== 生命周期详情页测试 ====================
class TestSegments:
    def _login(self, client):
        client.post("/login", data={"username": "student", "password": "day07"})

    def test_segments_page(self, client):
        self._login(client)
        resp = client.get("/segments")
        assert resp.status_code == 200


# ==================== 退出登录测试 ====================
class TestLogout:
    def test_logout_clears_session(self, client):
        client.post("/login", data={"username": "student", "password": "day07"})
        resp = client.get("/logout", follow_redirects=True)
        assert resp.status_code == 200
