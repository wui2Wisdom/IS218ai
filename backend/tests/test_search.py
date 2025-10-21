import os
import pytest
from fastapi.testclient import TestClient

# This will fail because backend/app.py doesn't exist yet!
# That's GOOD - that's TDD!


def test_healthz_ok():
    """Test 1: Health check should return 200 OK"""
    from backend.app import app
    client = TestClient(app)
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json()["ok"] is True


def test_search_requires_api_key(monkeypatch):
    """Test 2: Search without API key should fail"""
    monkeypatch.delenv("TAVILY_API_KEY", raising=False)
    # Need to reload the module to pick up the env change
    import importlib
    import backend.app as app_module
    importlib.reload(app_module)
    from backend.app import app
    client = TestClient(app)
    r = client.get("/search", params={"q": "chanel bag"})
    assert r.status_code == 500
    assert "Missing TAVILY_API_KEY" in r.text


@pytest.mark.parametrize("bad", ["", "a"])
def test_search_query_validation(bad, monkeypatch):
    """Test 3: Invalid queries should return 422"""
    monkeypatch.setenv("TAVILY_API_KEY", "fake")
    from backend.app import app
    client = TestClient(app)
    r = client.get("/search", params={"q": bad})
    assert r.status_code == 422
