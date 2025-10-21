# 🚀 DupeFinder - Quick Reference Card

**Print this or keep it open while coding!**

---

## 📂 Documentation Guide

| Document | Use When | Time |
|----------|----------|------|
| **README_DUPEFINDER.md** | Starting the project | 5 min read |
| **QUICK_START_CHECKLIST.md** | Want to code NOW | 30 min setup |
| **TDD_WORKFLOW_DIAGRAM.md** | Understanding TDD | 10 min read |
| **TDD_IMPLEMENTATION_PLAN.md** | Need detailed help | Reference |
| **PROJECT_SUMMARY.md** | Quick overview | 5 min read |

---

## ⚡ Essential Commands

```bash
# SETUP (Run once)
source .venv/bin/activate
pip install fastapi uvicorn httpx pydantic pytest pytest-cov
export TAVILY_API_KEY=your_key_here

# TESTING (Run constantly)
pytest backend/tests/ -v                    # Run all tests
pytest backend/tests/test_search.py -v      # Run one file
pytest --cov=backend                        # With coverage

# DEVELOPMENT (Run in separate terminals)
uvicorn backend.app:app --reload --port 8000    # Backend
python -m http.server 5173 --directory frontend # Frontend

# MANUAL TESTING
curl http://localhost:8000/healthz
curl "http://localhost:8000/search?q=test" | jq
curl "http://localhost:8000/dupes?q=sunglasses" | jq
```

---

## 🔄 TDD Cycle (Memorize This!)

```
1. RED   → Write failing test (15 min)
2. GREEN → Make it pass (30 min)
3. REFACTOR → Clean up code (15 min)
4. COMMIT → Save progress
5. REPEAT → Next feature
```

---

## 📋 Phase Checklist

```
Phase 0: Setup (20 min)
├─ [ ] Create folders
├─ [ ] Install deps
├─ [ ] Get API key
└─ [ ] Configure pytest

Phase 1: /search (60 min)
├─ [ ] Write tests (RED)
├─ [ ] Implement (GREEN)
└─ [ ] Refactor

Phase 2: /dupes (60 min)
├─ [ ] Scoring tests (RED)
├─ [ ] Implement scoring (GREEN)
└─ [ ] Extract service (REFACTOR)

Phase 3: Frontend (90 min)
├─ [ ] Create HTML
├─ [ ] Connect API
└─ [ ] Add interactivity

Phase 4: Docs (45 min)
├─ [ ] API.md
├─ [ ] ARCHITECTURE.md
└─ [ ] Update README

Phase 5: Quality (45 min)
├─ [ ] Coverage >90%
├─ [ ] Integration tests
└─ [ ] Manual testing
```

---

## 🎯 Success Criteria

**Phase 1 Done When:**
- ✅ `curl http://localhost:8000/healthz` works
- ✅ `curl http://localhost:8000/search?q=test` returns results
- ✅ All tests pass

**Phase 2 Done When:**
- ✅ `curl http://localhost:8000/dupes?q=test` returns scored results
- ✅ Results sorted by dupeScore
- ✅ All tests pass

**Phase 3 Done When:**
- ✅ Open `http://localhost:5173` shows UI
- ✅ Search returns and displays results
- ✅ Modal opens with details

---

## 💡 Git Commit Format

```bash
# Pattern: <type>(<scope>): <subject>

# Examples:
git commit -m "test(backend): add failing test for /search"
git commit -m "feat(backend): implement /search endpoint"
git commit -m "refactor(backend): extract tavily provider"
git commit -m "docs(api): document /dupes endpoint"
git commit -m "fix(frontend): handle empty search results"
```

**Types:** feat, fix, test, refactor, docs, chore

---

## 🆘 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Tests won't import | Add `__init__.py` files |
| API key missing | `export TAVILY_API_KEY=...` |
| Tests fail | Check error, that's expected in RED! |
| Server won't start | Check if port 8000 is free |
| CORS error | Added CORS middleware? |
| Coverage too low | Write more tests |

---

## 📁 File Structure Quick Ref

```
IS218ai/
├── backend/
│   ├── app.py              ← FastAPI app
│   ├── providers/
│   │   └── tavily.py       ← Search API
│   ├── services/
│   │   └── scoring.py      ← Dupe logic
│   └── tests/
│       └── test_search.py  ← Tests
├── frontend/
│   └── index.html          ← UI
└── docs/                   ← All guides
```

---

## 🎓 TDD Rules (The Law!)

1. ❌ **DON'T** write code before test
2. ✅ **DO** write smallest test that fails
3. ✅ **DO** write minimal code to pass
4. ✅ **DO** refactor after green
5. ✅ **DO** commit after each cycle

---

## ⏱️ Time Budget

```
Total: 6-8 hours over 3 days

Day 1: 2-3 hours
├─ Phase 0: 20 min
└─ Phase 1: 60 min

Day 2: 2-3 hours  
├─ Phase 2: 60 min
└─ Phase 3: 90 min

Day 3: 1-2 hours
├─ Phase 4: 45 min
└─ Phase 5: 45 min
```

---

## 🔑 Key APIs

### Endpoints You'll Build

```
GET /healthz
→ {"ok": true}

GET /search?q=query&max_results=8
→ {"query": "...", "results": [...]}

GET /dupes?q=query&max_results=8
→ {"query": "...", "items": [scored...]}
```

### Tavily API (External)

```
POST https://api.tavily.com/search
Body: {
  "api_key": "...",
  "query": "...",
  "max_results": 8
}
```

---

## 📊 Test Coverage Goals

```
Phase 1: >80%
Phase 2: >85%
Phase 5: >90%

Check with:
pytest --cov=backend --cov-report=term-missing
```

---

## 🎯 Daily Session Template

### Morning (1 hour)
```bash
1. Activate venv
2. Pull latest code
3. Pick one phase
4. Write tests (RED)
5. Run tests → FAIL
6. Commit
```

### Afternoon (1 hour)
```bash
7. Implement feature (GREEN)
8. Run tests → PASS
9. Commit
10. Refactor code
11. Run tests → STILL PASS
12. Commit
13. Push to GitHub
```

---

## 🔗 Important Links

- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **Tavily API:** https://docs.tavily.com/
- **pytest Docs:** https://docs.pytest.org/
- **Tailwind CSS:** https://tailwindcss.com/docs

---

## 💪 Motivation

**You're building:**
- ✅ Production-quality code
- ✅ Test-driven development
- ✅ Modern tech stack
- ✅ Portfolio-ready project

**Each phase completed = Level up!** 🎮

---

## 📞 Where to Look

```
Stuck on setup?
→ QUICK_START_CHECKLIST.md

Don't understand TDD?
→ TDD_WORKFLOW_DIAGRAM.md

Need implementation details?
→ TDD_IMPLEMENTATION_PLAN.md

Want quick overview?
→ PROJECT_SUMMARY.md

Ready to start?
→ README_DUPEFINDER.md
```

---

**Keep this open while coding! 🚀**

*Good luck building DupeFinder!*
