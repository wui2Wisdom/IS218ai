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


def test_dupes_requires_query(monkeypatch):
    """Test 4: /dupes endpoint requires query parameter"""
    monkeypatch.setenv("TAVILY_API_KEY", "fake")
    from backend.app import app
    client = TestClient(app)
    r = client.get("/dupes", params={"q": ""})
    assert r.status_code == 422


def test_dupes_scoring_with_mock(monkeypatch):
    """Test 5: /dupes scores results and returns items sorted by score"""
    monkeypatch.setenv("TAVILY_API_KEY", "fake")

    class FakeResp:
        def raise_for_status(self): ...
        def json(self):
            return {"results": [
                {
                    "title": "Option A $39.99",
                    "url": "https://www.amazon.com/item",
                    "content": "Affordable dupe $39.99",
                    "source": "web"
                },
                {
                    "title": "Option B",
                    "url": "https://unknown-site.com/x",
                    "content": "No price visible",
                    "source": "web"
                }
            ]}

    class FakeClient:
        def __init__(self, *a, **k): ...
        async def __aenter__(self): return self
        async def __aexit__(self, *a): ...
        async def post(self, *a, **k): return FakeResp()

    # Import fresh and patch httpx
    import importlib
    import backend.app as appmod
    importlib.reload(appmod)
    monkeypatch.setattr(appmod.httpx, "AsyncClient", FakeClient)

    from backend.app import app
    client = TestClient(app)
    r = client.get("/dupes", params={"q": "quilted chain bag", "max_results": 5})
    
    assert r.status_code == 200
    payload = r.json()
    assert payload["query"] == "quilted chain bag"
    
    items = payload["items"]
    assert len(items) == 2
    
    # Items should be sorted by dupeScore (highest first)
    assert items[0]["dupeScore"] >= items[1]["dupeScore"]
    
    # Amazon item should have higher score
    assert "amazon.com" in items[0]["site"]
    assert items[0]["price"] == 39.99
    assert items[0]["dupeScore"] > 50
    
    # Unknown site should have lower score
    assert items[1]["price"] is None
    assert items[1]["dupeScore"] <= 50
