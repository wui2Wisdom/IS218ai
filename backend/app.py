from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import os
import httpx

app = FastAPI(title="DupeFinder API")

# CORS middleware for frontend
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


class DupeItem(BaseModel):
    title: str
    url: str
    snippet: str
    site: Optional[str] = None
    price: Optional[float] = None
    dupeScore: int
    reason: str


class DupeResponse(BaseModel):
    query: str
    items: List[DupeItem] = Field(default_factory=list)


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


# Retailer scoring weights
DUPE_SITES = {
    "amazon": 10,
    "walmart": 9,
    "target": 9,
    "etsy": 7,
    "aliexpress": 6,
    "zara": 7,
    "hm.com": 7,
    "shein": 5,
    "uniqlo": 7,
    "asos": 7,
}


def extract_site(url: str) -> Optional[str]:
    """Extract domain from URL"""
    try:
        host = url.split("//", 1)[1].split("/", 1)[0].lower()
        return host
    except Exception:
        return None


def extract_price(text: str) -> Optional[float]:
    """Extract price from text using regex"""
    import re
    m = re.search(r"\$(\d+(?:\.\d{1,2})?)", text)
    return float(m.group(1)) if m else None


def score_dupe(result: SearchResult) -> DupeItem:
    """Calculate dupe score for a search result"""
    site = extract_site(result.url) or ""
    base = 50
    bump = 0
    
    # Check if site is a recognized retailer
    for key, val in DUPE_SITES.items():
        if key in site:
            bump = max(bump, val)
    
    # Bonus for visible price
    price = extract_price(result.snippet or "")
    if price is not None:
        bump += 5
    
    score = max(0, min(100, base + bump))
    
    # Generate reason
    reason = "Recognized retailer" if bump > 0 else "General relevance"
    if price is not None:
        reason += " + visible price"
    
    return DupeItem(
        title=result.title,
        url=result.url,
        snippet=result.snippet,
        site=site or None,
        price=price,
        dupeScore=score,
        reason=reason,
    )


@app.get("/dupes", response_model=DupeResponse)
async def dupes(
    q: str = Query(..., min_length=2, max_length=256),
    max_results: int = Query(8, ge=1, le=20),
):
    """Find affordable dupes with scoring"""
    # Enhance query to focus on dupes
    compound_query = f"dupe {q} affordable alternative"
    
    try:
        raw = await tavily_search(compound_query, max_results)
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Provider error: {e}") from e
    
    normalized = normalize(raw, max_results)
    items = [score_dupe(r) for r in normalized]
    
    # Sort by dupeScore descending (highest first)
    items.sort(key=lambda x: x.dupeScore, reverse=True)
    
    return DupeResponse(query=q, items=items)
