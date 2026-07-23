"""Day 08: Flask API 测试

测试覆盖：
1. /health 返回 200
2. 未登录访问 /api/metrics 被拦截
3. 登录后 /api/metrics 返回 ok 和 metrics
4. /api/categories?category=Fashion 返回筛选结果
"""

import json
import sys
from pathlib import Path

import pytest

# 确保能找到 app
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


class TestHealth:
    """测试 /health 端点"""

    def test_health_returns_200(self, client):
        """/health 返回 200 和正确字段"""
        resp = client.get("/health")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["ok"] is True
        assert data["service"] == "day08-flask-upgrade"


class TestApiMetrics:
    """测试 /api/metrics 端点"""

    def test_metrics_requires_login(self, client):
        """未登录访问 /api/metrics 应被重定向到登录页"""
        resp = client.get("/api/metrics")
        assert resp.status_code == 302
        assert "/login" in resp.location

    def test_metrics_returns_data(self, client):
        """登录后 /api/metrics 返回 ok 和 metrics"""
        client.post("/login", data={"username": "student", "password": "day07"})
        resp = client.get("/api/metrics")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["ok"] is True
        assert "metrics" in data
        assert len(data["metrics"]) == 4
        # 验证指标字段
        for metric in data["metrics"]:
            assert "label" in metric
            assert "value" in metric
            assert "note" in metric
        # 验证第一个指标
        assert data["metrics"][0]["label"] == "总用户数"
        assert data["metrics"][0]["note"] == "人"


class TestApiCategories:
    """测试 /api/categories 端点"""

    def test_categories_all(self, client):
        """登录后 /api/categories 返回全部品类"""
        client.post("/login", data={"username": "student", "password": "day07"})
        resp = client.get("/api/categories")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["ok"] is True
        assert data["category"] == "全部"
        assert len(data["rows"]) == 5

    def test_categories_filtered(self, client):
        """登录后 /api/categories?category=Fashion 返回筛选结果"""
        client.post("/login", data={"username": "student", "password": "day07"})
        resp = client.get("/api/categories?category=Fashion")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["ok"] is True
        assert data["category"] == "Fashion"
        assert len(data["rows"]) == 1
        assert data["rows"][0]["偏好品类"] == "Fashion"


class TestAuth:
    """测试登录认证"""

    def test_login_success(self, client):
        """使用正确凭据可以登录"""
        resp = client.post(
            "/login", data={"username": "student", "password": "day07"}
        )
        assert resp.status_code == 302
        assert "/dashboard" in resp.location

    def test_login_failure(self, client):
        """使用错误密码应返回登录页"""
        resp = client.post(
            "/login", data={"username": "student", "password": "wrong"}
        )
        assert resp.status_code == 200
        # 仍然在登录页
        assert b"login" in resp.data.lower()


class TestErrorHandling:
    """测试错误处理"""

    def test_400_error_json(self, client):
        """400 错误处理程序应返回 JSON 错误结构"""
        # 测试 app 注册的 400 错误处理器
        resp = client.get("/api/metrics")  # 未登录
        assert resp.status_code == 302  # 重定向到登录

        # 测试 400 错误处理器：发送空请求到 /api/ask
        client.post("/login", data={"username": "student", "password": "day07"})
        resp = client.post("/api/ask", json={"question": ""})
        assert resp.status_code == 400
        data = resp.get_json()
        assert data["ok"] is False

    def test_404_returns_page(self, client):
        """404 应返回 HTML 页面"""
        resp = client.get("/nonexistent-page")
        assert resp.status_code == 404
        assert b"404" in resp.data
