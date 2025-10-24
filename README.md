# DupeFinder 🔍

**Discover affordable "dupes" of luxury items with AI-powered search**

DupeFinder is a full-stack web application that helps you find budget-friendly alternatives to high-end products. Built with FastAPI, vanilla JavaScript, and the Tavily search API, it uses a smart scoring algorithm to rank results by retailer reputation and price.

![Python](https://img.shields.io/badge/python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.119.1-009688)
![Test Coverage](https://img.shields.io/badge/coverage-96%25-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)

---

## 🌟 Features

- **Smart Search**: Uses Tavily API to find the best dupe alternatives across the web
- **Intelligent Scoring**: Ranks results based on:
  - Retailer reputation (Amazon, Target, Walmart, etc.)
  - Price extraction and affordability
  - Content relevance
- **Beautiful UI**: Mobile-first, responsive design with Tailwind CSS
- **Sorting Options**: Sort by dupe score, price (low/high), or alphabetically
- **Product Details**: Click any product card to see full details in a modal
- **Test-Driven Development**: 96% test coverage with pytest

---

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- [Tavily API key](https://tavily.com/) (1000 free searches/month)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/wui2Wisdom/IS218ai.git
   cd IS218ai
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   TAVILY_API_KEY=your_api_key_here
   ```
   
   ⚠️ **Important**: No spaces after the `=` sign!

5. **Run tests**
   ```bash
   pytest
   ```

---

## 🏃 Running the Application

### Start the Backend (FastAPI)

```bash
uvicorn backend.app:app --port 8000
```

The API will be available at `http://localhost:8000`

### Start the Frontend

In a new terminal:

```bash
cd frontend
python -m http.server 5173
```

Visit `http://localhost:5173` in your browser

---

## 📚 API Documentation

### Endpoints

#### `GET /healthz`
Health check endpoint

**Response:**
```json
{
  "ok": true
}
```

#### `GET /search`
Basic search using Tavily API

**Query Parameters:**
- `q` (required): Search query
- `max_results` (optional): Number of results (default: 5)

**Example:**
```bash
curl "http://localhost:8000/search?q=sunglasses&max_results=3"
```

#### `GET /dupes`
Enhanced search with dupe scoring algorithm

**Query Parameters:**
- `q` (required): Product to find dupes for
- `max_results` (optional): Number of results (default: 5)

**Example:**
```bash
curl "http://localhost:8000/dupes?q=quilted+chain+bag&max_results=10"
```

**Response:**
```json
{
  "query": "quilted chain bag",
  "items": [
    {
      "title": "Quilted Chain Shoulder Bag - Amazon",
      "url": "https://www.amazon.com/...",
      "snippet": "Classic quilted pattern with chain strap...",
      "site": "www.amazon.com",
      "price": 29.99,
      "dupeScore": 65,
      "reason": "Top retailer + Great price"
    }
  ]
}
```

### Interactive API Docs

FastAPI provides automatic interactive documentation:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## 🧮 Scoring Algorithm

Each dupe is scored on a **0-65 scale** based on three factors:

### 1. Base Score (50 points)
All results start with 50 points for relevance

### 2. Retailer Score (0-10 points)
Bonus points based on retailer reputation:
- **10 pts**: Amazon, Target
- **9 pts**: Walmart, AliExpress
- **8 pts**: eBay, Etsy
- **7 pts**: Shein, Temu
- **6 pts**: DHgate, Wish

### 3. Price Score (0-5 points)
Bonus for affordability:
- **5 pts**: Under $20
- **3 pts**: $20-$50
- **1 pt**: $50-$100

**Example Calculation:**
```
Amazon product at $18.99:
  Base:     50 points
  Retailer: +10 points (Amazon)
  Price:    +5 points (under $20)
  ─────────────────────
  Total:    65 points
```

See [SCORING_ALGORITHM_EXPLAINED.md](docs/SCORING_ALGORITHM_EXPLAINED.md) for detailed documentation.

---

## 🧪 Testing

### Run All Tests
```bash
pytest
```

### Run with Coverage Report
```bash
pytest --cov=backend --cov-report=term-missing
```

### Test Structure
```
tests/
└── test_search.py
    ├── test_healthz_ok()
    ├── test_search_requires_api_key()
    ├── test_search_query_validation()
    └── test_dupes_scoring_monkeypatched()
```

Current coverage: **96%**

---

## 📂 Project Structure

```
IS218ai/
├── backend/
│   ├── __init__.py
│   ├── app.py              # FastAPI application
│   ├── providers/
│   │   ├── __init__.py
│   │   └── tavily.py       # Tavily API integration
│   ├── services/
│   │   ├── __init__.py
│   │   └── scoring.py      # Dupe scoring logic
│   └── tests/
│       ├── __init__.py
│       └── test_search.py  # Test suite
├── frontend/
│   └── index.html          # Single-page application
├── docs/
│   ├── TDD_IMPLEMENTATION_PLAN.md
│   ├── QUICK_START_CHECKLIST.md
│   ├── TDD_WORKFLOW_DIAGRAM.md
│   ├── PROJECT_SUMMARY.md
│   ├── QUICK_REFERENCE.md
│   └── SCORING_ALGORITHM_EXPLAINED.md
├── .env                    # Environment variables (not in git)
├── .gitignore
├── pytest.ini              # Pytest configuration
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## 🛠️ Tech Stack

### Backend
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern, fast web framework
- **[Tavily API](https://tavily.com/)** - AI-powered search engine
- **[Pydantic](https://pydantic-docs.helpmanual.io/)** - Data validation
- **[httpx](https://www.python-httpx.org/)** - Async HTTP client

### Frontend
- **HTML5** - Semantic markup
- **[Tailwind CSS](https://tailwindcss.com/)** - Utility-first CSS framework
- **Vanilla JavaScript** - No framework overhead

### Testing & Development
- **[pytest](https://pytest.org/)** - Testing framework
- **[pytest-cov](https://pytest-cov.readthedocs.io/)** - Coverage reporting
- **TDD Methodology** - Test-driven development approach

---

## 🎯 Development Workflow

This project follows **Test-Driven Development (TDD)**:

1. **RED**: Write a failing test
2. **GREEN**: Write minimal code to pass
3. **REFACTOR**: Improve code quality

See [docs/TDD_WORKFLOW_DIAGRAM.md](docs/TDD_WORKFLOW_DIAGRAM.md) for the complete workflow.

---

## 📖 Documentation

- **[TDD Implementation Plan](docs/TDD_IMPLEMENTATION_PLAN.md)** - Complete development guide
- **[Quick Start Checklist](docs/QUICK_START_CHECKLIST.md)** - Setup checklist
- **[Scoring Algorithm](docs/SCORING_ALGORITHM_EXPLAINED.md)** - Deep dive on scoring
- **[Project Summary](docs/PROJECT_SUMMARY.md)** - Project overview
- **[Quick Reference](docs/QUICK_REFERENCE.md)** - Command cheat sheet

---

## 🐛 Troubleshooting

### Backend returns 401 Unauthorized
- Check that `.env` file exists and has your Tavily API key
- Ensure no spaces after the `=` sign: `TAVILY_API_KEY=your_key`
- Restart the backend after changing `.env`

### Port already in use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Kill process on port 5173
lsof -ti:5173 | xargs kill -9
```

### Tests failing
```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Run tests with verbose output
pytest -v
```

---

## 🚧 Roadmap

- [ ] Add user authentication
- [ ] Save favorite dupes
- [ ] Price tracking over time
- [ ] Browser extension
- [ ] Mobile app (React Native)
- [ ] More search providers (Google Shopping, Bing)

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Write tests for your changes
4. Ensure all tests pass: `pytest`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**wui2Wisdom**

- GitHub: [@wui2Wisdom](https://github.com/wui2Wisdom)
- Repository: [IS218ai](https://github.com/wui2Wisdom/IS218ai)

---

## 🙏 Acknowledgments

- [Tavily](https://tavily.com/) for the search API
- [FastAPI](https://fastapi.tiangolo.com/) for the amazing framework
- [Tailwind CSS](https://tailwindcss.com/) for the utility-first CSS
- The Python testing community for pytest

---

## 📊 Project Stats

- **Lines of Code**: ~1,500
- **Test Coverage**: 96%
- **Dependencies**: 8 packages
- **Development Time**: ~4 hours (following TDD)
- **API Calls**: Efficient (only 1 per search)

---

<div align="center">
  
**Happy dupe hunting! 🛍️**

If you found this project helpful, please ⭐ star it on GitHub!

</div>
