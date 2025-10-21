# DupeFinder - TDD Workflow Diagram

## 🔄 The Complete TDD Cycle

```
┌─────────────────────────────────────────────────────────────────┐
│                     TDD WORKFLOW CYCLE                          │
└─────────────────────────────────────────────────────────────────┘

    ┌──────────┐
    │  START   │
    └────┬─────┘
         │
         ▼
    ┌──────────────────────────────────────────┐
    │  1. RED: Write Failing Test              │
    │  ────────────────────────────────        │
    │  • Think: "What should this do?"         │
    │  • Write test for behavior               │
    │  • Run test → Should FAIL ❌             │
    │  • Commit: test(scope): add failing test │
    └────┬─────────────────────────────────────┘
         │
         │ Test FAILS ❌
         │
         ▼
    ┌──────────────────────────────────────────┐
    │  2. GREEN: Make Test Pass                │
    │  ───────────────────────────              │
    │  • Write MINIMAL code to pass            │
    │  • Don't worry about perfection          │
    │  • Run test → Should PASS ✅             │
    │  • Commit: feat/fix(scope): implement    │
    └────┬─────────────────────────────────────┘
         │
         │ Test PASSES ✅
         │
         ▼
    ┌──────────────────────────────────────────┐
    │  3. REFACTOR: Clean Up Code              │
    │  ──────────────────────────────           │
    │  • Improve code quality                  │
    │  • Extract functions/modules             │
    │  • Add comments/docs                     │
    │  • Run ALL tests → Still PASS ✅         │
    │  • Commit: refactor(scope): improve      │
    └────┬─────────────────────────────────────┘
         │
         │ All Tests PASS ✅
         │
         ▼
    ┌──────────────────────────────────────────┐
    │  4. REPEAT: Next Feature                 │
    │  ──────────────────────────────           │
    │  • Pick next behavior to implement       │
    │  • Go back to RED step                   │
    └────┬─────────────────────────────────────┘
         │
         └──────┐
                │
                ▼
         Back to RED


═══════════════════════════════════════════════════════════════════


## 📋 DupeFinder Phase Breakdown

┌───────────────────────────────────────────────────────────────────┐
│                         PHASE 0: SCAFFOLD                          │
│  Goal: Set up project structure and tools                         │
├───────────────────────────────────────────────────────────────────┤
│  Tasks:                                                            │
│  ☐ Create folders (backend/, frontend/, docs/)                    │
│  ☐ Install dependencies (FastAPI, pytest, httpx)                  │
│  ☐ Configure pytest.ini                                           │
│  ☐ Add TAVILY_API_KEY to .env                                     │
│  ☐ Commit: feat(scaffold): initialize project                     │
│                                                                    │
│  Time: 15-20 minutes                                              │
│  Output: ✅ Ready to write tests                                  │
└───────────────────────────────────────────────────────────────────┘
                                ↓
┌───────────────────────────────────────────────────────────────────┐
│                    PHASE 1: BACKEND /search                        │
│  Goal: Implement web search with TDD                              │
├───────────────────────────────────────────────────────────────────┤
│  1.1 RED:                                                          │
│     • Write test_healthz_ok()                                     │
│     • Write test_search_requires_api_key()                        │
│     • Write test_search_query_validation()                        │
│     • Write test_search_ok_mocks_provider()                       │
│     • Run pytest → All FAIL ❌                                    │
│     • Commit: test(backend): add failing tests                    │
│                                                                    │
│  1.2 GREEN:                                                        │
│     • Create backend/app.py                                       │
│     • Implement /healthz endpoint                                 │
│     • Implement /search with Tavily integration                   │
│     • Run pytest → All PASS ✅                                    │
│     • Commit: feat(backend): implement /search                    │
│                                                                    │
│  1.3 REFACTOR:                                                     │
│     • Extract providers/tavily.py                                 │
│     • Add LRU cache                                               │
│     • Improve error handling                                      │
│     • Run pytest → All PASS ✅                                    │
│     • Commit: refactor(backend): extract provider                 │
│                                                                    │
│  Time: 45-60 minutes                                              │
│  Output: ✅ Working /search API endpoint                          │
└───────────────────────────────────────────────────────────────────┘
                                ↓
┌───────────────────────────────────────────────────────────────────┐
│                     PHASE 2: BACKEND /dupes                        │
│  Goal: Add scoring algorithm with TDD                             │
├───────────────────────────────────────────────────────────────────┤
│  2.1 RED:                                                          │
│     • Write test_dupes_requires_query()                           │
│     • Write test_dupes_scoring()                                  │
│     • Write test_dupes_recognizes_retailers()                     │
│     • Write test_dupes_extracts_price()                           │
│     • Write test_dupes_sorts_by_score()                           │
│     • Run pytest → New tests FAIL ❌                              │
│     • Commit: test(backend): add dupes scoring tests              │
│                                                                    │
│  2.2 GREEN:                                                        │
│     • Implement score_dupe() function                             │
│     • Add extract_site() and extract_price()                      │
│     • Implement /dupes endpoint                                   │
│     • Run pytest → All PASS ✅                                    │
│     • Commit: feat(backend): implement /dupes scoring             │
│                                                                    │
│  2.3 REFACTOR:                                                     │
│     • Extract scoring to services/scoring.py                      │
│     • Add constants for retailer weights                          │
│     • Improve price regex                                         │
│     • Run pytest → All PASS ✅                                    │
│     • Commit: refactor(backend): extract scoring service          │
│                                                                    │
│  Time: 45-60 minutes                                              │
│  Output: ✅ Working /dupes API with scoring                       │
└───────────────────────────────────────────────────────────────────┘
                                ↓
┌───────────────────────────────────────────────────────────────────┐
│                      PHASE 3: FRONTEND UI                          │
│  Goal: Build mobile-first UI and connect to API                   │
├───────────────────────────────────────────────────────────────────┤
│  3.1 Create HTML Mockup:                                           │
│     • Build responsive layout with Tailwind                       │
│     • Add search bar, product grid, modal                         │
│     • Static mockup (no API yet)                                  │
│     • Commit: feat(frontend): create UI mockup                    │
│                                                                    │
│  3.2 Wire to API:                                                  │
│     • Add fetchDupes() function                                   │
│     • Implement renderProducts()                                  │
│     • Add loading and error states                               │
│     • Test: Search shows real results                             │
│     • Commit: feat(frontend): connect to /dupes API               │
│                                                                    │
│  3.3 Add Interactivity:                                            │
│     • Implement sorting (price, score)                            │
│     • Add modal with product details                              │
│     • Add "View Item" external link                              │
│     • Commit: feat(frontend): add sorting and modal               │
│                                                                    │
│  3.4 REFACTOR:                                                     │
│     • Extract helper functions                                    │
│     • Add debouncing to search                                    │
│     • Improve responsive design                                   │
│     • Commit: refactor(frontend): improve UX                      │
│                                                                    │
│  Time: 60-90 minutes                                              │
│  Output: ✅ Full-stack app working!                               │
└───────────────────────────────────────────────────────────────────┘
                                ↓
┌───────────────────────────────────────────────────────────────────┐
│                     PHASE 4: DOCUMENTATION                         │
│  Goal: Document everything for others                             │
├───────────────────────────────────────────────────────────────────┤
│  • Create docs/API.md (endpoint documentation)                     │
│  • Create docs/ARCHITECTURE.md (system design)                     │
│  • Update README.md (setup and usage)                             │
│  • Add code comments and docstrings                               │
│  • Commit: docs: add comprehensive documentation                  │
│                                                                    │
│  Time: 30-45 minutes                                              │
│  Output: ✅ Project is well-documented                            │
└───────────────────────────────────────────────────────────────────┘
                                ↓
┌───────────────────────────────────────────────────────────────────┐
│                    PHASE 5: TEST COVERAGE                          │
│  Goal: Ensure code quality with >90% coverage                     │
├───────────────────────────────────────────────────────────────────┤
│  • Run pytest --cov=backend --cov-report=html                     │
│  • Add missing tests for edge cases                               │
│  • Add integration tests                                          │
│  • Manual testing checklist                                       │
│  • Commit: test(backend): achieve 90%+ coverage                   │
│                                                                    │
│  Time: 30-45 minutes                                              │
│  Output: ✅ Production-ready code                                 │
└───────────────────────────────────────────────────────────────────┘
                                ↓
                          ┌─────────┐
                          │  DONE!  │
                          └─────────┘


═══════════════════════════════════════════════════════════════════


## 🎯 Daily Work Session Template

### Example: Working on /dupes endpoint

#### Session Start (5 min)
```bash
cd /home/thewiseone/IS218/IS218ai
source .venv/bin/activate
export TAVILY_API_KEY=$(grep TAVILY_API_KEY .env | cut -d= -f2)
git checkout -b feature/add-dupes-endpoint
```

#### RED Phase (15 min)
```bash
# 1. Write test in backend/tests/test_search.py
# Add: test_dupes_scoring_basic()

# 2. Run test - should FAIL
pytest backend/tests/test_search.py::test_dupes_scoring_basic -v
# ❌ Expected: Test fails (no /dupes endpoint)

# 3. Commit failing test
git add backend/tests/test_search.py
git commit -m "test(backend): add failing test for dupes scoring"
```

#### GREEN Phase (20 min)
```bash
# 1. Write minimal code in backend/app.py
# Add: score_dupe(), extract_price(), /dupes endpoint

# 2. Run test - should PASS
pytest backend/tests/test_search.py::test_dupes_scoring_basic -v
# ✅ Expected: Test passes

# 3. Run ALL tests - should PASS
pytest backend/tests/ -v
# ✅ Expected: All tests pass

# 4. Commit working code
git add backend/app.py
git commit -m "feat(backend): implement /dupes endpoint with scoring"
```

#### REFACTOR Phase (15 min)
```bash
# 1. Extract scoring logic to service
# Create: backend/services/scoring.py
# Move: score_dupe, extract_price, extract_site

# 2. Update app.py to import from service

# 3. Run ALL tests - should STILL PASS
pytest backend/tests/ -v
# ✅ Expected: All tests still pass

# 4. Commit refactor
git add backend/app.py backend/services/
git commit -m "refactor(backend): extract scoring logic to service module"
```

#### Manual Test (10 min)
```bash
# 1. Start server
uvicorn backend.app:app --reload --port 8000

# 2. Test in another terminal
curl "http://localhost:8000/dupes?q=sunglasses&max_results=5" | jq

# 3. Verify response looks correct
```

#### Session End (5 min)
```bash
# Push to GitHub
git push origin feature/add-dupes-endpoint

# Create PR (if ready)
# Or continue with next feature
```

**Total time: 60-70 minutes for one complete feature**


═══════════════════════════════════════════════════════════════════


## 📊 Testing Commands Reference

### Basic Testing
```bash
# Run all tests
pytest

# Run specific file
pytest backend/tests/test_search.py

# Run specific test
pytest backend/tests/test_search.py::test_healthz_ok

# Verbose output
pytest -v

# Show print statements
pytest -s
```

### Coverage Testing
```bash
# Basic coverage
pytest --cov=backend

# Coverage with missing lines
pytest --cov=backend --cov-report=term-missing

# HTML coverage report
pytest --cov=backend --cov-report=html
open htmlcov/index.html
```

### Test Markers
```bash
# Run only integration tests (if marked)
pytest -m integration

# Run only unit tests
pytest -m unit

# Skip slow tests
pytest -m "not slow"
```

### Continuous Testing
```bash
# Watch mode (requires pytest-watch)
pip install pytest-watch
ptw backend/tests/
```


═══════════════════════════════════════════════════════════════════


## 🎓 TDD Best Practices Checklist

### ✅ Before Writing Code
- [ ] Do I have a failing test for this behavior?
- [ ] Is the test clear and specific?
- [ ] Does it test ONE thing?
- [ ] Can I predict what will make it pass?

### ✅ While Writing Code
- [ ] Am I writing the MINIMAL code to pass?
- [ ] Am I avoiding premature optimization?
- [ ] Am I keeping it simple?
- [ ] Can someone else understand this?

### ✅ After Code Passes
- [ ] Do ALL tests still pass?
- [ ] Is there duplication I can remove?
- [ ] Are names clear and descriptive?
- [ ] Should I extract a function/module?
- [ ] Did I commit with a clear message?

### ✅ Before Moving On
- [ ] Is coverage maintained/improved?
- [ ] Are edge cases tested?
- [ ] Is the code documented?
- [ ] Can I demo this feature?


═══════════════════════════════════════════════════════════════════


## 🚨 Common TDD Mistakes to Avoid

### ❌ DON'T: Write code first
```python
# BAD: Writing implementation first
def search(query):
    # 100 lines of code...
    pass

# THEN writing tests
def test_search():
    assert search("test") == expected
```

### ✅ DO: Write test first
```python
# GOOD: Writing test first
def test_search_returns_results():
    result = search("sunglasses")
    assert len(result) > 0
    assert result[0].has_key("title")

# THEN write minimal implementation
def search(query):
    return [{"title": "test"}]  # Simplest thing that works
```

---

### ❌ DON'T: Test implementation details
```python
# BAD: Testing internal methods
def test_search_calls_tavily_with_correct_params():
    # This breaks when you refactor
    assert mock_tavily.called_with(query="test", depth="basic")
```

### ✅ DO: Test behavior/output
```python
# GOOD: Testing what users see
def test_search_returns_normalized_results():
    results = search("sunglasses")
    assert all(r.has_key("title") for r in results)
    assert all(r.has_key("url") for r in results)
```

---

### ❌ DON'T: Write giant tests
```python
# BAD: One test for everything
def test_entire_search_flow():
    # Tests validation
    # Tests API call
    # Tests normalization
    # Tests caching
    # Tests error handling
    # 50 lines of asserts...
```

### ✅ DO: Write focused tests
```python
# GOOD: One test per behavior
def test_search_validates_query_length():
    with pytest.raises(ValidationError):
        search("")

def test_search_calls_provider():
    result = search("valid query")
    assert mock_provider.called

def test_search_normalizes_results():
    result = search("test")
    assert isinstance(result[0], SearchResult)
```

---

### ❌ DON'T: Skip refactor step
```python
# BAD: Tests pass, move on!
def search(q):
    if not q or len(q) < 2: raise ValueError
    key = os.getenv("KEY")
    if not key: raise ValueError
    # Messy code but it works...
```

### ✅ DO: Clean up after tests pass
```python
# GOOD: Tests pass, now improve!
def search(query: str) -> SearchResponse:
    """Search for items using configured provider."""
    _validate_query(query)
    _ensure_api_key()
    return _call_provider(query)

# Helper functions make it cleaner
```


═══════════════════════════════════════════════════════════════════


## 🎯 Success Metrics

Track your progress:

```
PHASE 0: Scaffold
├─ ✅ Folders created
├─ ✅ Dependencies installed  
├─ ✅ pytest configured
└─ ✅ Environment set up
    Time: ~20 min

PHASE 1: /search
├─ ✅ Tests written (RED)
├─ ✅ Tests passing (GREEN)
├─ ✅ Code refactored (REFACTOR)
└─ ✅ Coverage: >80%
    Time: ~60 min

PHASE 2: /dupes
├─ ✅ Scoring tests (RED)
├─ ✅ Scoring works (GREEN)
├─ ✅ Service extracted (REFACTOR)
└─ ✅ Coverage: >85%
    Time: ~60 min

PHASE 3: Frontend
├─ ✅ UI mockup created
├─ ✅ API integrated
├─ ✅ Sorting/filtering works
└─ ✅ Mobile responsive
    Time: ~90 min

PHASE 4: Docs
├─ ✅ API documented
├─ ✅ Architecture documented
└─ ✅ README complete
    Time: ~45 min

PHASE 5: Quality
├─ ✅ Test coverage >90%
├─ ✅ Integration tests
└─ ✅ Manual testing done
    Time: ~45 min

TOTAL TIME: 5-6 hours (spread across multiple days)
```


═══════════════════════════════════════════════════════════════════

You've got this! 🚀 Start with Phase 0, follow the RED-GREEN-REFACTOR cycle, and build one feature at a time!
