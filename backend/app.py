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
