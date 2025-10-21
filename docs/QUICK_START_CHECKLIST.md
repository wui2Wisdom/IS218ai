# DupeFinder - Quick Start Checklist

## ⚡ Start Here - First 30 Minutes

### ✅ Step 1: Environment Setup (5 min)
```bash
# You're already using .venv ✓
source .venv/bin/activate

# Get Tavily API Key (free)
# 1. Go to https://tavily.com
# 2. Sign up (free tier: 1000 searches/month)
# 3. Copy your API key
```

Add to your `.env` file:
```bash
echo "TAVILY_API_KEY=tvly-your_key_here" >> .env
```

### ✅ Step 2: Create Folder Structure (2 min)
```bash
cd /home/thewiseone/IS218/IS218ai

# Create all needed folders
mkdir -p backend/tests backend/providers frontend docs

# Create __init__.py files for Python imports
touch backend/__init__.py
touch backend/tests/__init__.py
touch backend/providers/__init__.py
```

### ✅ Step 3: Install Dependencies (3 min)
```bash
# Create backend requirements
cat > backend/requirements.txt << 'EOF'
fastapi==0.115.0
uvicorn[standard]==0.30.6
httpx==0.27.2
pydantic==2.9.2
pytest==8.3.3
pytest-cov==5.0.0
EOF

# Install everything
pip install -r backend/requirements.txt

# Update root requirements (optional)
pip freeze > requirements.txt
```

### ✅ Step 4: Update pytest.ini (1 min)
```bash
cat > pytest.ini << 'EOF'
[pytest]
addopts = -q --cov=backend --cov-report=term-missing
testpaths = backend/tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
EOF
```

### ✅ Step 5: First Commit (2 min)
```bash
git add backend/ docs/ pytest.ini .env
git commit -m "feat(scaffold): initialize backend, frontend, docs structure"
```

---

## 🔴 Phase 1: Write Your First Failing Test (RED)

### Create backend/tests/test_search.py (10 min)
Copy this code to start with failing tests:

```python
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
```

### Run Tests - They Should FAIL ❌
```bash
export TAVILY_API_KEY=test_key
pytest backend/tests/test_search.py -v
```

**Expected output**: `ModuleNotFoundError: No module named 'backend.app'`

✅ **This is GOOD!** You're doing TDD correctly!

### Commit Your Tests
```bash
git add backend/tests/test_search.py
git commit -m "test(backend): add failing tests for /healthz and /search"
```

---

## 🟢 Phase 2: Make Tests Pass (GREEN)

### Create backend/app.py (15 min)
Now write the MINIMAL code to make tests pass:

```python
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import os
import httpx

app = FastAPI(title="DupeFinder API")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

class SearchResult(BaseModel):
    title: str
    url: str
    snippet: str
    source: Optional[str] = None
    published_at: Optional[str] = None

class SearchResponse(BaseModel):
    query: str
    results: List[SearchResult] = Field(default_factory=list)

@app.get("/healthz")
def healthz():
    """Health check endpoint"""
    return {"ok": True}

async def tavily_search(query: str, max_results: int):
    """Call Tavily API"""
    if not TAVILY_API_KEY:
        raise HTTPException(status_code=500, detail="Missing TAVILY_API_KEY")
    
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "search_depth": "basic",
        "max_results": max_results,
        "include_answer": False,
        "include_images": False,
    }
    
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.post("https://api.tavily.com/search", json=payload)
        r.raise_for_status()
        return r.json()

def normalize(results_json, max_results: int) -> List[SearchResult]:
    """Normalize Tavily results to our format"""
    out: List[SearchResult] = []
    for item in (results_json.get("results") or [])[:max_results]:
        out.append(
            SearchResult(
                title=item.get("title") or "Untitled",
                url=item.get("url") or "",
                snippet=item.get("content") or item.get("snippet") or "",
                source=item.get("source"),
                published_at=item.get("published") or None,
            )
        )
    return out

@app.get("/search", response_model=SearchResponse)
async def search(
    q: str = Query(..., min_length=2, max_length=256),
    max_results: int = Query(8, ge=1, le=20),
):
    """Search for items using Tavily"""
    try:
        raw = await tavily_search(q, max_results)
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Provider error: {e}") from e
    
    return SearchResponse(query=q, results=normalize(raw, max_results))
```

### Run Tests - They Should PASS ✅
```bash
export TAVILY_API_KEY=your_real_key_here
pytest backend/tests/test_search.py -v
```

**Expected**: All tests GREEN! ✅

### Test Manually
```bash
# Terminal 1: Start server
uvicorn backend.app:app --reload --port 8000

# Terminal 2: Test it
curl http://localhost:8000/healthz
curl "http://localhost:8000/search?q=chanel+bag&max_results=3"
```

### Commit Working Code
```bash
git add backend/app.py
git commit -m "feat(backend): implement /healthz and /search endpoints"
```

---

## 🎯 You Just Did TDD! Here's What You Accomplished:

1. ✅ **RED**: Wrote failing tests first
2. ✅ **GREEN**: Made tests pass with minimal code
3. ✅ **REFACTOR**: (Next step - extract provider module)
4. ✅ **COMMIT**: Atomic commits for each step

---

## 📋 What's Next? (Choose Your Path)

### Option A: Continue with Backend (/dupes endpoint)
```bash
# Add scoring tests (RED)
# Implement scoring (GREEN)
# See: TDD_IMPLEMENTATION_PLAN.md Phase 2
```

### Option B: Build Frontend Now
```bash
# Create frontend/index.html
# Wire to API
# See: TDD_IMPLEMENTATION_PLAN.md Phase 3
```

### Option C: Refactor Backend
```bash
# Extract providers/tavily.py
# Add caching
# See: TDD_IMPLEMENTATION_PLAN.md Phase 1.3
```

---

## 🆘 Troubleshooting

### Tests won't import backend.app
```bash
# Make sure __init__.py files exist
touch backend/__init__.py
touch backend/tests/__init__.py

# Run from project root
cd /home/thewiseone/IS218/IS218ai
pytest backend/tests/
```

### TAVILY_API_KEY not found
```bash
# Load from .env
source .venv/bin/activate
export $(grep -v '^#' .env | xargs)

# Or set directly
export TAVILY_API_KEY=tvly-your_key_here
```

### uvicorn command not found
```bash
# Make sure venv is activated
source .venv/bin/activate

# Reinstall if needed
pip install uvicorn[standard]
```

---

## 📊 Progress Tracker

Track your progress through the phases:

- [ ] **Phase 0**: Scaffold complete ← YOU ARE HERE
- [ ] **Phase 1**: /search endpoint working
- [ ] **Phase 2**: /dupes endpoint with scoring
- [ ] **Phase 3**: Frontend connected to API
- [ ] **Phase 4**: Documentation complete
- [ ] **Phase 5**: Tests at 90%+ coverage

---

## 🎓 TDD Mantras

Remember these while building:

1. **Red → Green → Refactor** - Always in that order
2. **Test first** - No production code without a failing test
3. **Minimal code** - Write just enough to pass the test
4. **One change at a time** - Small, atomic commits
5. **Tests are documentation** - They show how code should work

---

## 🚀 Ready to Start?

Run these commands in order:

```bash
cd /home/thewiseone/IS218/IS218ai
source .venv/bin/activate
mkdir -p backend/tests backend/providers frontend docs
pip install -r backend/requirements.txt
export TAVILY_API_KEY=your_key_here

# You're ready! Start with Phase 1 (RED)
```

Good luck! 🎉
