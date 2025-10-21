# 🎯 DupeFinder - Project Summary at a Glance

## What You're Building

**DupeFinder** = A web app that finds affordable alternatives (dupes) to luxury items

```
┌─────────────────────────────────────────────────────────┐
│                    USER EXPERIENCE                      │
├─────────────────────────────────────────────────────────┤
│  1. User types: "quilted chain bag"                    │
│  2. App searches the web via Tavily API                │
│  3. Results get scored (Amazon=10, Unknown=5, etc.)    │
│  4. Display cards sorted by dupe score                 │
│  5. Click card → See details + "Why it's a dupe"       │
│  6. Click "View Item" → Go to retailer site            │
└─────────────────────────────────────────────────────────┘
```

---

## Tech Stack

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   FRONTEND   │────→│   BACKEND    │────→│  TAVILY API  │
├──────────────┤     ├──────────────┤     ├──────────────┤
│  HTML        │     │  FastAPI     │     │  Web Search  │
│  Tailwind    │     │  Python 3.x  │     │  Provider    │
│  JavaScript  │     │  httpx       │     │              │
│  Fetch API   │     │  pydantic    │     │              │
└──────────────┘     └──────────────┘     └──────────────┘
       ↓                    ↓
┌──────────────┐     ┌──────────────┐
│    USER      │     │    pytest    │
│   Browser    │     │   Testing    │
└──────────────┘     └──────────────┘
```

---

## Project Timeline

```
┌──────────────────────────────────────────────────────────┐
│  DAY 1 (2-3 hours)                                       │
├──────────────────────────────────────────────────────────┤
│  Morning:                                                │
│    ☐ Phase 0: Setup (20 min)                            │
│    ☐ Phase 1: Build /search API (60 min)                │
│                                                          │
│  Afternoon:                                              │
│    ☐ Manual testing                                     │
│    ☐ Fix any issues                                     │
│                                                          │
│  ✅ Deliverable: Working search API                     │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│  DAY 2 (2-3 hours)                                       │
├──────────────────────────────────────────────────────────┤
│  Morning:                                                │
│    ☐ Phase 2: Build /dupes with scoring (60 min)        │
│                                                          │
│  Afternoon:                                              │
│    ☐ Phase 3: Build frontend UI (90 min)                │
│                                                          │
│  ✅ Deliverable: Full-stack working app                 │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│  DAY 3 (1-2 hours)                                       │
├──────────────────────────────────────────────────────────┤
│  Morning:                                                │
│    ☐ Phase 4: Write docs (45 min)                       │
│    ☐ Phase 5: Improve tests (45 min)                    │
│                                                          │
│  ✅ Deliverable: Production-ready app                   │
└──────────────────────────────────────────────────────────┘
```

---

## The TDD Process (Your Daily Workflow)

```
┌─────────────────────────────────────────────────────┐
│              PICK A FEATURE                         │
│  Example: "Add /search endpoint"                    │
└───────────────────┬─────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│  🔴 RED: Write Failing Test (15 min)                │
├─────────────────────────────────────────────────────┤
│  def test_search_returns_results():                 │
│      response = client.get("/search?q=test")        │
│      assert response.status_code == 200             │
│      assert len(response.json()["results"]) > 0     │
│                                                     │
│  Run: pytest → ❌ FAILS (no endpoint yet)           │
│  Commit: "test(backend): add failing test"          │
└───────────────────┬─────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│  🟢 GREEN: Make Test Pass (30 min)                  │
├─────────────────────────────────────────────────────┤
│  @app.get("/search")                                │
│  def search(q: str):                                │
│      results = call_tavily(q)                       │
│      return {"results": results}                    │
│                                                     │
│  Run: pytest → ✅ PASSES                            │
│  Commit: "feat(backend): implement /search"         │
└───────────────────┬─────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│  🔵 REFACTOR: Clean Up (15 min)                     │
├─────────────────────────────────────────────────────┤
│  • Extract call_tavily() to providers/tavily.py     │
│  • Add type hints and docstrings                    │
│  • Improve error handling                           │
│                                                     │
│  Run: pytest → ✅ STILL PASSES                      │
│  Commit: "refactor(backend): extract provider"      │
└───────────────────┬─────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│              NEXT FEATURE                           │
│  Go back to RED and repeat!                         │
└─────────────────────────────────────────────────────┘

Total time per feature: 60 minutes
Features to build: ~8
Total project time: ~8 hours (spread over 3 days)
```

---

## File Structure (What You'll Create)

```
IS218ai/
│
├── 📄 .env                          # Your API keys
│   TAVILY_API_KEY=tvly-xxxxx
│   OPENAI_API_KEY=sk-xxxxx
│
├── 📂 backend/                      # Backend API (Python)
│   ├── app.py                      # ← Main FastAPI app (Phase 1 & 2)
│   ├── providers/
│   │   └── tavily.py               # ← Tavily integration (Phase 1)
│   ├── services/
│   │   └── scoring.py              # ← Dupe scoring logic (Phase 2)
│   └── tests/
│       ├── test_search.py          # ← Tests (Phase 1 & 2)
│       └── test_integration.py     # ← Integration tests (Phase 5)
│
├── 📂 frontend/                     # Frontend UI (HTML/JS)
│   └── index.html                  # ← Single-page app (Phase 3)
│
├── 📂 docs/                         # Documentation
│   ├── README_DUPEFINDER.md        # ← START HERE!
│   ├── QUICK_START_CHECKLIST.md    # ← Quick start guide
│   ├── TDD_IMPLEMENTATION_PLAN.md  # ← Detailed guide
│   ├── TDD_WORKFLOW_DIAGRAM.md     # ← Visual guide
│   ├── PROJECT_SUMMARY.md          # ← This file!
│   ├── API.md                      # ← API docs (Phase 4)
│   └── ARCHITECTURE.md             # ← System design (Phase 4)
│
├── pytest.ini                       # Pytest configuration
└── requirements.txt                 # Python dependencies
```

---

## Key Endpoints You'll Build

### Backend API (`http://localhost:8000`)

```
GET /healthz
├─ Returns: {"ok": true}
├─ Purpose: Health check
└─ Phase: 1

GET /search?q=query&max_results=8
├─ Returns: {"query": "...", "results": [...]}
├─ Purpose: Raw web search results
└─ Phase: 1

GET /dupes?q=query&max_results=8
├─ Returns: {"query": "...", "items": [scored results]}
├─ Purpose: Scored dupe results with prices
└─ Phase: 2
```

### Example Response

```json
GET /dupes?q=sunglasses

{
  "query": "sunglasses",
  "items": [
    {
      "title": "Retro Square Sunglasses - $24.99",
      "url": "https://amazon.com/...",
      "snippet": "Affordable alternative to designer shades. Only $24.99!",
      "site": "amazon.com",
      "price": 24.99,
      "dupeScore": 95,
      "reason": "Recognized retailer + visible price"
    },
    {
      "title": "Classic Aviator Sunglasses",
      "url": "https://unknown-site.com/...",
      "snippet": "Great quality sunglasses at low prices",
      "site": "unknown-site.com",
      "price": null,
      "dupeScore": 50,
      "reason": "General relevance"
    }
  ]
}
```

---

## Testing Strategy

### Unit Tests (Phase 1 & 2)
```python
# Test individual functions
test_healthz_ok()
test_search_validates_query()
test_search_calls_provider()
test_dupes_scores_correctly()
test_dupes_extracts_price()
```

### Integration Tests (Phase 5)
```python
# Test full flows
test_search_to_dupes_flow()
test_error_handling_across_layers()
```

### Manual Testing (Phase 3 & 5)
```bash
# Test with browser
1. Search for "quilted chain bag"
2. Verify results appear
3. Click a card → Modal opens
4. Click "View Item" → External site opens
5. Test on mobile size (F12 → Device toolbar)
```

### Coverage Goal
```bash
pytest --cov=backend --cov-report=term-missing

# Target: >90% coverage
```

---

## Git Workflow

### Branch Strategy
```bash
main                    # Production-ready code
├── feature/scaffold    # Phase 0
├── feature/search      # Phase 1
├── feature/dupes       # Phase 2
├── feature/frontend    # Phase 3
└── feature/docs        # Phase 4
```

### Commit Pattern
```bash
# For each feature, you'll make 3+ commits:

git commit -m "test(backend): add failing test for /search"     # RED
git commit -m "feat(backend): implement /search endpoint"       # GREEN  
git commit -m "refactor(backend): extract tavily provider"      # REFACTOR

# Then repeat for next feature
```

---

## Environment Setup

### Prerequisites
```bash
✅ Python 3.8+ installed
✅ .venv created and activated
✅ VS Code (recommended)
✅ Git configured
```

### API Keys Needed
```bash
1. Tavily API Key (FREE)
   ├─ Sign up: https://tavily.com
   ├─ Free tier: 1000 searches/month
   └─ Add to .env: TAVILY_API_KEY=tvly-xxxxx

2. OpenAI API Key (OPTIONAL - already have)
   └─ Only needed if you add AI features later
```

---

## Quick Commands Reference

### Development
```bash
# Activate environment
source .venv/bin/activate

# Set API key
export TAVILY_API_KEY=$(grep TAVILY_API_KEY .env | cut -d= -f2)

# Run tests
pytest backend/tests/ -v

# Run tests with coverage
pytest --cov=backend --cov-report=term-missing

# Start backend server
uvicorn backend.app:app --reload --port 8000

# Start frontend server
python -m http.server 5173 --directory frontend

# Run both (2 terminals needed)
# Terminal 1: uvicorn backend.app:app --reload --port 8000
# Terminal 2: python -m http.server 5173 --directory frontend
```

### Testing Endpoints
```bash
# Health check
curl http://localhost:8000/healthz

# Search
curl "http://localhost:8000/search?q=sunglasses&max_results=3" | jq

# Dupes
curl "http://localhost:8000/dupes?q=quilted+chain+bag&max_results=5" | jq

# Frontend
open http://localhost:5173
```

---

## Success Checklist

### Phase 0: Setup ✅
- [ ] Created `backend/`, `frontend/`, `docs/` folders
- [ ] Installed FastAPI, pytest, httpx, pydantic
- [ ] Added TAVILY_API_KEY to .env
- [ ] `pytest` runs without errors

### Phase 1: Search API ✅
- [ ] Tests written and failing
- [ ] Tests now passing
- [ ] `curl http://localhost:8000/search?q=test` returns results
- [ ] Coverage >80%

### Phase 2: Dupes API ✅
- [ ] Scoring tests written and passing
- [ ] `curl http://localhost:8000/dupes?q=test` returns scored results
- [ ] Results include dupeScore and reason
- [ ] Coverage >85%

### Phase 3: Frontend ✅
- [ ] HTML mockup created with Tailwind
- [ ] Search bar triggers API call
- [ ] Results display in grid
- [ ] Modal shows product details
- [ ] Mobile responsive

### Phase 4: Documentation ✅
- [ ] `docs/API.md` complete
- [ ] `docs/ARCHITECTURE.md` complete
- [ ] README.md updated

### Phase 5: Quality ✅
- [ ] Test coverage >90%
- [ ] Integration tests passing
- [ ] Manual testing complete
- [ ] No known bugs

---

## Common Questions

**Q: How long will this take?**
A: 6-8 hours total, spread over 2-3 days. Each phase is 30-90 minutes.

**Q: What if I get stuck?**
A: Check the documentation:
- Quick help: QUICK_START_CHECKLIST.md
- Visual guide: TDD_WORKFLOW_DIAGRAM.md
- Deep dive: TDD_IMPLEMENTATION_PLAN.md

**Q: Do I need to know FastAPI?**
A: No! The code is provided. You'll learn by doing.

**Q: What if tests fail?**
A: That's good! In TDD, tests SHOULD fail first (RED), then you make them pass (GREEN).

**Q: Can I skip the tests?**
A: Please don't! The tests are what make TDD work. They're your safety net.

**Q: What's the hardest part?**
A: Phase 3 (frontend) takes longest but is most rewarding. You'll see your app come to life!

**Q: Can I deploy this?**
A: Yes! After Phase 5, you can deploy to:
- Backend: Render, Railway, Fly.io
- Frontend: Netlify, Vercel, GitHub Pages

---

## Next Steps

### Right Now:
1. ✅ Open `README_DUPEFINDER.md` (start here guide)
2. ✅ Choose your learning path
3. ✅ Get Tavily API key
4. ✅ Begin Phase 0 setup

### Today:
- Complete Phase 0 + Phase 1
- Test your /search endpoint
- Celebrate! 🎉

### Tomorrow:
- Complete Phase 2 + Phase 3
- See your full-stack app work
- Show it to someone!

### Day 3:
- Complete Phase 4 + Phase 5
- Achieve 90%+ coverage
- Deploy (optional)
- Add to portfolio!

---

## Resources

### Your Documentation
- 📖 README_DUPEFINDER.md - Start here
- ⚡ QUICK_START_CHECKLIST.md - Quick actions
- 🔄 TDD_WORKFLOW_DIAGRAM.md - Visual guide
- 📚 TDD_IMPLEMENTATION_PLAN.md - Complete reference
- 📊 PROJECT_SUMMARY.md - This file

### External Docs
- FastAPI: https://fastapi.tiangolo.com/
- Tavily: https://docs.tavily.com/
- pytest: https://docs.pytest.org/
- Tailwind: https://tailwindcss.com/

---

## 🎯 Your Mission

Build a production-quality web application using professional software engineering practices:

✅ Test-Driven Development
✅ Clean architecture
✅ Modern tech stack
✅ >90% test coverage
✅ Comprehensive documentation
✅ Portfolio-ready project

**You've got this! Let's build DupeFinder! 🚀**

---

*Last updated: October 20, 2025*
*Project: DupeFinder - Find affordable dupes of luxury items*
*Author: IS218 Student*
