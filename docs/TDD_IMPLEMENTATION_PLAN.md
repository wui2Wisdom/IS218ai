# DupeFinder - TDD Implementation Plan

## Project Overview
**DupeFinder** is a mobile-first web app that discovers affordable "dupes" (alternatives) of luxury items using web search APIs.

### Tech Stack
- **Backend**: FastAPI + Tavily API (web search)
- **Frontend**: HTML + Tailwind CSS + Vanilla JS
- **Testing**: pytest with TDD approach
- **Environment**: Python 3.x with `.venv`

---

## Current State Analysis
Your workspace has:
- ✅ `.venv` (active virtual environment)
- ✅ `.env` file (has OPENAI_API_KEY, need to add TAVILY_API_KEY)
- ✅ `requirements.txt` (needs FastAPI dependencies)
- ✅ `pytest.ini` (needs configuration update)
- ✅ Basic `src/` and `tests/` folders
- ❌ Need to create `backend/` and `frontend/` structure
- ❌ Need to add documentation

---

## Phase 0: Scaffold Repository and Tooling

### Step 0.1: Restructure Project Folders
**Goal**: Create proper separation between backend and frontend

```bash
# Create folder structure
mkdir -p backend/tests
mkdir -p backend/providers
mkdir -p frontend
mkdir -p docs
```

**Expected Structure**:
```
IS218ai/
├── .env                    # Environment variables
├── .venv/                  # Virtual environment (exists)
├── pytest.ini             # Pytest configuration
├── requirements.txt       # Python dependencies
├── backend/
│   ├── app.py            # FastAPI application
│   ├── providers/
│   │   └── __init__.py
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_search.py
│   └── requirements.txt   # Backend-specific dependencies
├── frontend/
│   └── index.html        # Single-page app
├── docs/
│   ├── API.md
│   ├── ARCHITECTURE.md
│   └── TDD_PLAN.md
└── README.md
```

**Atomic Commit**: `feat(scaffold): initialize backend, frontend, docs structure`

### Step 0.2: Update Environment Configuration
**Action**: Add TAVILY_API_KEY to `.env`

```bash
# Add to .env file
TAVILY_API_KEY=your_tavily_api_key_here
```

**How to get Tavily API Key**:
1. Visit https://tavily.com
2. Sign up for free account
3. Get API key from dashboard
4. Add to `.env` file

**Atomic Commit**: `chore(env): add TAVILY_API_KEY configuration`

### Step 0.3: Install Backend Dependencies
**Action**: Update requirements and install packages

```bash
# Activate virtual environment
source .venv/bin/activate

# Create backend/requirements.txt with:
# fastapi==0.115.0
# uvicorn[standard]==0.30.6
# httpx==0.27.2
# pydantic==2.9.2
# pytest==8.3.3
# pytest-cov==5.0.0

# Install dependencies
pip install -r backend/requirements.txt

# Update root requirements.txt to include all dependencies
pip freeze > requirements.txt
```

**Atomic Commit**: `chore(deps): install FastAPI, httpx, pytest, and testing dependencies`

### Step 0.4: Update pytest.ini
**Action**: Configure pytest for backend tests

```ini
[pytest]
addopts = -q --cov=backend --cov-report=term-missing
testpaths = backend/tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

**Atomic Commit**: `chore(test): configure pytest for backend testing with coverage`

---

## Phase 1: Backend TDD for /search Endpoint

### Step 1.1: RED - Write Failing Tests
**Goal**: Define expected behavior through tests BEFORE implementation

**Action**: Create `backend/tests/test_search.py`

Tests to write:
1. ✅ `test_healthz_ok()` - Health check endpoint returns 200
2. ✅ `test_search_requires_api_key()` - Missing API key returns 500
3. ✅ `test_search_query_validation()` - Invalid queries return 422
4. ✅ `test_search_ok_mocks_provider()` - Successful search with mocked Tavily
5. ✅ `test_search_caps_max_results()` - Respects max_results parameter

**Run tests** (should FAIL):
```bash
source .venv/bin/activate
export TAVILY_API_KEY=test_key
pytest backend/tests/test_search.py -v
```

**Expected**: All tests should fail because `backend/app.py` doesn't exist yet.

**Atomic Commit**: `test(backend): add failing tests for /healthz and /search endpoints`

### Step 1.2: GREEN - Minimal Implementation
**Goal**: Make tests pass with simplest possible code

**Action**: Create `backend/app.py`

Implement:
1. ✅ FastAPI app initialization
2. ✅ CORS middleware for frontend
3. ✅ `/healthz` endpoint
4. ✅ `/search` endpoint with:
   - Query validation (min 2 chars, max 256)
   - API key check
   - Tavily API integration
   - Result normalization to standard format

**Run tests** (should PASS):
```bash
pytest backend/tests/test_search.py -v
```

**Test manually**:
```bash
# Terminal 1: Start server
uvicorn backend.app:app --reload --port 8000

# Terminal 2: Test endpoints
curl http://localhost:8000/healthz
curl "http://localhost:8000/search?q=chanel+bag&max_results=3"
```

**Atomic Commit**: `feat(backend): implement /healthz and /search endpoints with Tavily integration`

### Step 1.3: REFACTOR - Clean Up Code
**Goal**: Improve code quality without changing behavior

**Actions**:
1. Extract Tavily provider to `backend/providers/tavily.py`
2. Add simple LRU cache for repeated queries
3. Improve error messages and logging
4. Add type hints and docstrings

**Run tests** (should still PASS):
```bash
pytest backend/tests/test_search.py -v
```

**Atomic Commits**:
- `refactor(backend): extract Tavily provider to separate module`
- `refactor(backend): add LRU cache for search results`
- `refactor(backend): improve error handling and messages`

---

## Phase 2: Backend TDD for /dupes Endpoint

### Step 2.1: RED - Write Tests for Scoring Logic
**Goal**: Define dupe scoring behavior

**Action**: Add tests to `backend/tests/test_search.py`

Tests to write:
1. ✅ `test_dupes_requires_query()` - Query validation
2. ✅ `test_dupes_mocks_provider_produces_scored_items()` - Scoring logic
3. ✅ `test_dupes_limits_results()` - Respects max_results
4. ✅ `test_dupes_recognizes_known_retailers()` - Amazon, Target, etc.
5. ✅ `test_dupes_extracts_price_from_snippet()` - Price detection
6. ✅ `test_dupes_sorts_by_score()` - Highest scores first

**Run tests** (should FAIL):
```bash
pytest backend/tests/test_search.py::test_dupes -v
```

**Atomic Commit**: `test(backend): add failing tests for /dupes scoring and ranking`

### Step 2.2: GREEN - Implement Scoring
**Goal**: Make dupe tests pass

**Action**: Add to `backend/app.py`

Implement:
1. ✅ `DUPE_SITES` dictionary with retailer scores
2. ✅ `extract_site()` function - Parse domain from URL
3. ✅ `extract_price()` function - Extract $XX.XX from text
4. ✅ `score_dupe()` function - Calculate dupeScore (0-100)
5. ✅ `/dupes` endpoint that:
   - Appends "dupe affordable alternative" to query
   - Calls Tavily search
   - Scores each result
   - Sorts by dupeScore descending
   - Returns DupeResponse model

**Run tests** (should PASS):
```bash
pytest backend/tests/ -v
```

**Test manually**:
```bash
curl "http://localhost:8000/dupes?q=quilted+chain+bag&max_results=5"
```

**Atomic Commit**: `feat(backend): implement /dupes endpoint with scoring algorithm`

### Step 2.3: REFACTOR - Extract Scoring Service
**Goal**: Make scoring logic reusable and testable

**Action**: Create `backend/services/scoring.py`

Move scoring logic to dedicated module:
- Retailer recognition
- Price extraction with regex
- Score calculation with weights
- Reason generation

**Atomic Commits**:
- `refactor(backend): extract scoring logic to services module`
- `test(backend): add unit tests for scoring utilities`

---

## Phase 3: Frontend Integration

### Step 3.1: Create HTML Mockup
**Goal**: Build mobile-first UI with Tailwind

**Action**: Create `frontend/index.html`

Components:
1. ✅ Header with logo and tagline
2. ✅ Search bar with placeholder
3. ✅ Sort dropdown (Price, Score, Newest)
4. ✅ Product grid (responsive 2-col mobile, 3-4 col desktop)
5. ✅ Product cards with image, title, price, score
6. ✅ Modal for product details
7. ✅ "Similar Finds" section in modal

**Test**: Open in browser, verify responsive design

**Atomic Commit**: `feat(frontend): create mobile-first UI mockup with Tailwind`

### Step 3.2: Wire Search to /dupes API
**Goal**: Connect UI to backend

**Action**: Add JavaScript to `index.html`

Implement:
1. ✅ `fetchDupes(query)` - Call backend API
2. ✅ `renderProducts(list)` - Generate card HTML
3. ✅ `openModal(id)` - Show product details
4. ✅ Search input handler - Trigger on Enter/change
5. ✅ Loading states - Show "Searching..." message
6. ✅ Error handling - Display friendly error messages

**Test**:
```bash
# Start backend
uvicorn backend.app:app --reload --port 8000

# Open frontend (use simple server)
python -m http.server 5173 --directory frontend
```

Visit: http://localhost:5173
Search: "quilted chain bag"

**Atomic Commit**: `feat(frontend): connect search to /dupes API with loading states`

### Step 3.3: Implement Sorting and Filtering
**Goal**: Make UI interactive

**Action**: Add sorting logic

Features:
1. ✅ Sort by price ascending/descending
2. ✅ Sort by popularity (dupeScore)
3. ✅ Sort by newest (reverse order)
4. ✅ Client-side search filter in results

**Atomic Commit**: `feat(frontend): add sorting and client-side filtering`

### Step 3.4: Polish Modal Experience
**Goal**: Enhance product details view

**Action**: Improve modal content

Features:
1. ✅ High-res product image
2. ✅ Full title and description
3. ✅ Price and retailer info
4. ✅ "Why this is a dupe" explanation
5. ✅ "View Item" external link button
6. ✅ Close button and click-outside-to-close

**Atomic Commit**: `feat(frontend): enhance modal with details and external links`

### Step 3.5: REFACTOR - Extract Helper Functions
**Goal**: Clean up JavaScript code

**Action**: Organize code into modules

Extract:
- `parsePrice(text)` - Price string to float
- `formatPrice(num)` - Float to $XX.XX
- `truncate(text, len)` - String truncation
- `debounce(fn, delay)` - Search debouncing

**Atomic Commit**: `refactor(frontend): extract utility functions and improve code organization`

---

## Phase 4: Documentation and Polish

### Step 4.1: Create API Documentation
**Action**: Create `docs/API.md`

Document:
- Base URL
- Authentication (API key)
- Endpoints:
  - `GET /healthz`
  - `GET /search?q=...&max_results=...`
  - `GET /dupes?q=...&max_results=...`
- Request/response examples
- Error codes and messages

**Atomic Commit**: `docs(api): add comprehensive API documentation`

### Step 4.2: Create Architecture Documentation
**Action**: Create `docs/ARCHITECTURE.md`

Document:
- System overview diagram
- Backend architecture (FastAPI + Tavily)
- Frontend architecture (vanilla JS)
- Data flow
- Scoring algorithm explanation
- Deployment considerations

**Atomic Commit**: `docs(architecture): document system design and data flow`

### Step 4.3: Update Main README
**Action**: Update `README.md`

Include:
- Project description
- Features list
- Setup instructions
- Running locally
- Testing instructions
- Environment variables
- Contributing guidelines

**Atomic Commit**: `docs(readme): add comprehensive project documentation`

---

## Phase 5: Testing and Quality Assurance

### Step 5.1: Achieve Test Coverage
**Goal**: Get backend test coverage to 90%+

**Action**: Add missing tests
```bash
pytest --cov=backend --cov-report=html
# Open htmlcov/index.html to see coverage report
```

**Atomic Commit**: `test(backend): improve test coverage to 90%+`

### Step 5.2: Add Integration Tests
**Goal**: Test full API flows

**Action**: Create `backend/tests/test_integration.py`

Tests:
- End-to-end search flow
- End-to-end dupes flow
- Error handling across layers

**Atomic Commit**: `test(backend): add integration tests for complete flows`

### Step 5.3: Manual Testing Checklist
**Action**: Test all user flows

- [ ] Search returns results
- [ ] Empty search shows guidance
- [ ] Sorting works correctly
- [ ] Modal opens/closes properly
- [ ] External links work
- [ ] Mobile responsive design
- [ ] Error messages display
- [ ] Loading states show

---

## Daily TDD Workflow

### The Red-Green-Refactor Cycle
```
1. RED: Write failing test
   └─> Think: "What should this do?"
   
2. GREEN: Make test pass
   └─> Write minimal code to pass test
   
3. REFACTOR: Clean up code
   └─> Improve without breaking tests
   
4. COMMIT: Save progress
   └─> One atomic commit per behavior
```

### Example Session
```bash
# 1. Start with failing test
git checkout -b feature/add-price-filter

# Edit backend/tests/test_search.py
# Add test_dupes_filters_by_max_price()

pytest backend/tests/test_search.py::test_dupes_filters_by_max_price -v
# ❌ FAILS (expected)

# 2. Make it pass
# Edit backend/app.py
# Add max_price parameter and filtering logic

pytest backend/tests/test_search.py::test_dupes_filters_by_max_price -v
# ✅ PASSES

# 3. Run all tests
pytest backend/tests/ -v
# ✅ ALL PASS

# 4. Commit
git add backend/tests/test_search.py backend/app.py
git commit -m "feat(backend): add max_price filter to /dupes endpoint"

# 5. Push
git push origin feature/add-price-filter
```

---

## Git Commit Message Format

### Convention
```
<type>(<scope>): <subject>

<body> (optional)
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `test`: Add/modify tests
- `refactor`: Code change without feature/fix
- `docs`: Documentation only
- `chore`: Build/tooling changes

### Scopes
- `backend`: Backend code
- `frontend`: Frontend code
- `test`: Test code
- `deps`: Dependencies
- `env`: Environment configuration

### Examples
```
feat(backend): implement /search endpoint with Tavily integration
test(backend): add tests for query validation
refactor(backend): extract scoring logic to service module
docs(api): document /dupes endpoint parameters
chore(deps): upgrade FastAPI to 0.115.0
```

---

## Quick Reference Commands

### Backend Development
```bash
# Activate environment
source .venv/bin/activate

# Set API key
export TAVILY_API_KEY=your_key_here

# Run tests
pytest backend/tests/ -v

# Run with coverage
pytest --cov=backend --cov-report=term-missing

# Start server
uvicorn backend.app:app --reload --port 8000

# Test endpoint
curl "http://localhost:8000/dupes?q=sunglasses&max_results=5"
```

### Frontend Development
```bash
# Serve frontend
python -m http.server 5173 --directory frontend

# Or use VS Code Live Server extension
```

### Full Stack Testing
```bash
# Terminal 1: Backend
source .venv/bin/activate
export TAVILY_API_KEY=your_key_here
uvicorn backend.app:app --reload --port 8000

# Terminal 2: Frontend
python -m http.server 5173 --directory frontend

# Browser: http://localhost:5173
```

---

## Success Criteria

### Phase 0 ✅
- [ ] Folder structure created
- [ ] Dependencies installed
- [ ] Environment configured
- [ ] pytest runs successfully

### Phase 1 ✅
- [ ] `/healthz` endpoint working
- [ ] `/search` endpoint working
- [ ] All tests passing
- [ ] Test coverage > 80%

### Phase 2 ✅
- [ ] `/dupes` endpoint working
- [ ] Scoring algorithm implemented
- [ ] Results sorted by score
- [ ] All tests passing

### Phase 3 ✅
- [ ] Frontend displays search results
- [ ] Modal shows product details
- [ ] Sorting/filtering works
- [ ] Mobile responsive

### Phase 4 ✅
- [ ] API documentation complete
- [ ] Architecture documented
- [ ] README comprehensive

### Phase 5 ✅
- [ ] Test coverage > 90%
- [ ] Integration tests passing
- [ ] Manual testing complete
- [ ] Ready for deployment

---

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'fastapi'`
```bash
# Solution: Install dependencies
source .venv/bin/activate
pip install -r backend/requirements.txt
```

**Issue**: `Missing TAVILY_API_KEY`
```bash
# Solution: Export environment variable
export TAVILY_API_KEY=your_key_here

# Or add to .env and load it
source .env
```

**Issue**: CORS errors in browser
```python
# Solution: Add CORS middleware in backend/app.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Issue**: Tests fail with import errors
```bash
# Solution: Add __init__.py files
touch backend/__init__.py
touch backend/tests/__init__.py
touch backend/providers/__init__.py
```

---

## Next Steps After Completion

1. **Deploy Backend**: Use Render, Railway, or Fly.io
2. **Deploy Frontend**: Use Netlify, Vercel, or GitHub Pages
3. **Add Features**:
   - User accounts and saved searches
   - Price tracking and alerts
   - Social sharing
   - Product comparisons
4. **Optimize**:
   - Add Redis caching
   - Implement rate limiting
   - Add request queuing
5. **Monitor**:
   - Add logging with Sentry
   - Track API usage
   - Monitor performance

---

Good luck building DupeFinder! 🚀
