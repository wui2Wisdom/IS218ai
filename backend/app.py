from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import os
import httpx
from bs4 import BeautifulSoup
import re

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
    image: Optional[str] = None


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
    image: Optional[str] = None


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
        "include_images": True,
    }
    
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.post("https://api.tavily.com/search", json=payload)
        r.raise_for_status()
        return r.json()


async def fetch_product_image(url: str) -> Optional[str]:
    """Scrape the actual product image from a product page - OPTIMIZED"""
    try:
        async with httpx.AsyncClient(timeout=6, follow_redirects=True) as client:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            }
            
            response = await client.get(url, headers=headers)
            
            if response.status_code != 200:
                return None
            
            soup = BeautifulSoup(response.text, 'lxml')
            text = response.text or ''
            
            # Strategy 0: JSON-LD (ld+json) - structured product data often contains images
            try:
                for script in soup.find_all('script', type='application/ld+json'):
                    try:
                        import json
                        data = json.loads(script.string or '{}')
                        # data can be a list or dict
                        if isinstance(data, list):
                            candidates = data
                        else:
                            candidates = [data]

                        for node in candidates:
                            # Look for product.image or image fields
                            if isinstance(node, dict):
                                img = node.get('image') or node.get('images')
                                if isinstance(img, str) and img.startswith('http') and not img.endswith('.svg'):
                                    print(f"✓ Found JSON-LD image: {img[:60]}")
                                    return img
                                if isinstance(img, list) and img:
                                    for iurl in img:
                                        if isinstance(iurl, str) and iurl.startswith('http') and not iurl.endswith('.svg'):
                                            print(f"✓ Found JSON-LD image (list): {iurl[:60]}")
                                            return iurl
                    except Exception:
                        continue
            except Exception:
                pass

            # Strategy 1: Open Graph image (most reliable for e-commerce)
            og_image = soup.find('meta', property='og:image')
            if og_image and og_image.get('content'):
                img_url = og_image.get('content')
                if img_url and img_url.startswith('http') and not img_url.endswith('.svg'):
                    print(f"✓ Found OG image: {img_url[:60]}")
                    return img_url
            
            # Strategy 2: Twitter card image
            twitter_image = soup.find('meta', attrs={'name': 'twitter:image'})
            if twitter_image and twitter_image.get('content'):
                img_url = twitter_image.get('content')
                if img_url and img_url.startswith('http') and not img_url.endswith('.svg'):
                    print(f"✓ Found Twitter image: {img_url[:60]}")
                    return img_url
            
            # Strategy 3: Product meta tag
            product_image = soup.find('meta', attrs={'property': 'product:image'})
            if product_image and product_image.get('content'):
                img_url = product_image.get('content')
                if img_url and img_url.startswith('http'):
                    print(f"✓ Found product meta image: {img_url[:60]}")
                    return img_url
            
            # Strategy 4: itemprop="image" (schema.org)
            itemprop_image = soup.find('img', attrs={'itemprop': 'image'})
            if itemprop_image:
                img_url = itemprop_image.get('src') or itemprop_image.get('data-src')
                if img_url:
                    img_url = normalize_url(img_url, url)
                    if img_url and img_url.startswith('http'):
                        print(f"✓ Found itemprop image: {img_url[:60]}")
                        return img_url

            # Strategy 4b: link rel=image_src
            link_img = soup.find('link', rel=re.compile(r'image_src', re.I))
            if link_img and link_img.get('href'):
                li = normalize_url(link_img.get('href'), url)
                if li and li.startswith('http') and not li.endswith('.svg'):
                    print(f"✓ Found link rel=image_src: {li[:60]}")
                    return li

            # Strategy 4c: og:image:secure_url
            og_secure = soup.find('meta', property='og:image:secure_url')
            if og_secure and og_secure.get('content'):
                osrc = og_secure.get('content')
                if osrc and osrc.startswith('http') and not osrc.endswith('.svg'):
                    print(f"✓ Found og:image:secure_url: {osrc[:60]}")
                    return osrc
            
            # Strategy 5: Common product image selectors
            selectors = [
                ('img', {'class': re.compile(r'product.*image', re.I)}),
                ('img', {'class': re.compile(r'main.*image', re.I)}),
                ('img', {'id': re.compile(r'product.*image', re.I)}),
                ('img', {'class': re.compile(r'gallery.*main', re.I)}),
            ]
            
            for tag, attrs in selectors:
                img = soup.find(tag, attrs)
                if img:
                    img_url = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
                    if img_url:
                        img_url = normalize_url(img_url, url)
                        if img_url and img_url.startswith('http') and not img_url.endswith('.svg'):
                            print(f"✓ Found selector image: {img_url[:60]}")
                            return img_url
            
            # Strategy 6: Find largest image (likely the product)
            all_images = soup.find_all('img', src=True, limit=20)
            best_img = None
            best_score = 0
            
            for img in all_images:
                src = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
                if not src:
                    continue
                
                # Skip obvious non-product images
                src_lower = src.lower()
                if any(skip in src_lower for skip in ['logo', 'icon', 'sprite', 'avatar', 'placeholder', 'blank']):
                    continue
                
                if src.endswith('.svg'):
                    continue
                
                # Normalize URL
                src = normalize_url(src, url)
                if not src or not src.startswith('http'):
                    continue

                # If srcset exists, prefer the largest candidate from it
                srcset = img.get('srcset') or img.get('data-srcset')
                if srcset:
                    try:
                        candidate = pick_largest_from_srcset(srcset, base=url)
                        if candidate:
                            candidate = normalize_url(candidate, url)
                            if candidate and candidate.startswith('http') and not candidate.endswith('.svg'):
                                print(f"✓ Found srcset candidate: {candidate[:60]}")
                                return candidate
                    except Exception:
                        pass
                
                # Score based on dimensions and URL hints
                score = 0
                width = img.get('width', '')
                height = img.get('height', '')
                
                if width and width.isdigit():
                    score += int(width)
                if height and height.isdigit():
                    score += int(height)
                
                # Boost for product-related keywords
                if re.search(r'(product|main|hero|large|full|detail)', src_lower):
                    score += 500
                
                if score > best_score:
                    best_score = score
                    best_img = src
            
            if best_img:
                print(f"✓ Found best image (score {best_score}): {best_img[:60]}")
                return best_img
            
            print(f"✗ No image found for {url[:50]}")
            return None
                
    except Exception as e:
        print(f"Error scraping {url[:50]}: {str(e)[:50]}")
        return None


def normalize_url(img_url: str, base_url: str) -> str:
    """Convert relative URLs to absolute"""
    if img_url.startswith('http'):
        return img_url
    elif img_url.startswith('//'):
        return 'https:' + img_url
    elif img_url.startswith('/'):
        from urllib.parse import urlparse
        parsed = urlparse(base_url)
        return f"{parsed.scheme}://{parsed.netloc}{img_url}"
    return img_url


def pick_largest_from_srcset(srcset: str, base: str = '') -> Optional[str]:
    """Parse a srcset string and return the URL with the largest width descriptor.

    Example: 'a.jpg 400w, b.jpg 800w' -> returns b.jpg
    """
    try:
        candidates = []
        parts = [p.strip() for p in srcset.split(',') if p.strip()]
        for p in parts:
            tokens = p.split()
            if not tokens:
                continue
            url = tokens[0]
            desc = tokens[1] if len(tokens) > 1 else ''
            width = 0
            if desc.endswith('w'):
                try:
                    width = int(desc[:-1])
                except Exception:
                    width = 0
            elif desc.endswith('x'):
                try:
                    # scale 'x' descriptors to an approximate width by multiplier
                    width = int(float(desc[:-1]) * 1000)
                except Exception:
                    width = 0
            candidates.append((width, url))

        if not candidates:
            return None
        # pick largest
        candidates.sort(key=lambda x: x[0], reverse=True)
        chosen = candidates[0][1]
        # Normalize if needed
        if chosen.startswith('//'):
            return 'https:' + chosen
        if chosen.startswith('/') and base:
            return normalize_url(chosen, base)
        return chosen
    except Exception:
        return None


def normalize(results_json, max_results: int) -> List[SearchResult]:
    """Normalize Tavily results to our format, filtering out excluded sites and non-shopping content"""
    out: List[SearchResult] = []
    images = results_json.get("images") or []
    
    images_fallback = results_json.get("images") or []
    for idx, item in enumerate(results_json.get("results") or []):
        if len(out) >= max_results:
            break
            
        url = item.get("url") or ""
        title = item.get("title") or "Untitled"
        snippet = item.get("content") or item.get("snippet") or ""
        site = extract_site(url)
        
        # Skip excluded sites (YouTube, TikTok, blogs, etc.)
        if site and any(excluded in site for excluded in EXCLUDED_SITES):
            continue
            
        # Skip content that contains non-shopping keywords
        content_text = f"{title} {snippet}".lower()
        if any(keyword in content_text for keyword in EXCLUDED_CONTENT_KEYWORDS):
            continue
            
        # Only include results that seem to be from shopping sites
        if not is_shopping_content(title, snippet, site):
            continue
        
        # Use Tavily's image as fallback - we'll fetch real ones in the dupes endpoint
        image_url = images[idx] if idx < len(images) else None
            
        out.append(
            SearchResult(
                title=title,
                url=url,
                snippet=snippet,
                source=item.get("source"),
                published_at=item.get("published") or None,
                image=image_url,
            )
        )
    return out


async def normalize_with_images(results_json, max_results: int) -> List[SearchResult]:
    """Normalize Tavily results - Focus on CLOTHING and FASHION items only, parallel image fetch"""
    out: List[SearchResult] = []
    # Tavily can provide an images array alongside results; use as initial fallbacks
    images_fallback = results_json.get("images") or []
    
    # Clothing/fashion keywords that MUST be present
    clothing_keywords = {
        'dress', 'shirt', 'pants', 'jeans', 'jacket', 'coat', 'sweater', 'hoodie',
        'shorts', 'skirt', 'top', 'blouse', 'cardigan', 'blazer', 'suit',
        'shoes', 'sneakers', 'boots', 'heels', 'sandals', 'flats',
        'bag', 'handbag', 'purse', 'backpack', 'tote', 'clutch', 'wallet',
        'sunglasses', 'glasses', 'hat', 'cap', 'beanie', 'scarf',
        'jewelry', 'necklace', 'bracelet', 'earrings', 'ring', 'watch',
        'belt', 'tie', 'gloves', 'socks', 'underwear', 'bra', 'lingerie',
        'swimsuit', 'bikini', 'swimwear', 'activewear', 'leggings', 'sports bra',
        'fashion', 'clothing', 'apparel', 'outfit', 'wear', 'style', 't-shirt',
        'polo', 'tank', 'vest', 'parka', 'trench', 'denim', 'chinos'
    }
    
    for idx, item in enumerate(results_json.get("results") or []):
        if len(out) >= max_results:
            break
            
        url = item.get("url") or ""
        title = item.get("title") or "Untitled"
        snippet = item.get("content") or item.get("snippet") or ""
        site = extract_site(url)
        
        # Skip excluded sites
        if site and any(excluded in site.lower() for excluded in EXCLUDED_SITES):
            continue
        
        # Skip blog/article URLs
        url_lower = url.lower()
        if '/blog/' in url_lower or '/article/' in url_lower or '/news/' in url_lower or '/guide/' in url_lower:
            continue
        
        # CLOTHING FILTER: Must have at least one clothing keyword
        content_text = f"{title} {snippet}".lower()
        has_clothing_keyword = any(keyword in content_text for keyword in clothing_keywords)
        
        if not has_clothing_keyword:
            continue
        
        # Use tavily-provided image as initial fallback if available
        initial_image = images_fallback[idx] if idx < len(images_fallback) else None

        out.append(
            SearchResult(
                title=title,
                url=url,
                snippet=snippet,
                source=item.get("source"),
                published_at=item.get("published") or None,
                image=initial_image,
            )
        )
    
    # Only fetch images for the items we'll actually use (in parallel, with timeout)
    if out and len(out) > 0:
        print(f"Fetching images for {min(len(out), max_results)} items in parallel...")
        import asyncio
        
        # Limit to max_results to save time
        items_to_fetch = out[:max_results]

        # Only fetch images for items that don't already have a valid image
        indices_to_fetch = [i for i, it in enumerate(items_to_fetch) if not it.image or not str(it.image).startswith('http')]

        async def fetch_with_fallback(url):
            try:
                img = await asyncio.wait_for(fetch_product_image(url), timeout=5.0)
                return img if img else None
            except asyncio.TimeoutError:
                print(f"Image fetch timeout for {url[:50]}")
                return None
            except Exception as e:
                print(f"Image fetch error: {e}")
                return None

        # Prepare tasks in the same order as indices_to_fetch
        tasks = [fetch_with_fallback(items_to_fetch[i].url) for i in indices_to_fetch]
        results = []
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)

        # Assign fetched images back to corresponding items
        for idx_pos, i in enumerate(indices_to_fetch):
            img = results[idx_pos] if idx_pos < len(results) else None
            if isinstance(img, str) and img:
                items_to_fetch[i].image = img
            else:
                # keep existing or use placeholder
                if not items_to_fetch[i].image:
                    items_to_fetch[i].image = "https://placehold.co/400x500/f3f4f6/9ca3af?text=No+Image"
    
    print(f"Filtered down to {len(out)} clothing/fashion results")
    return out


def is_shopping_content(title: str, snippet: str, site: str) -> bool:
    """Check if content appears to be from a shopping/retail context - STRICT filtering"""
    if not title or not snippet:
        return False
        
    content_text = f"{title} {snippet} {site}".lower()
    
    # Strong shopping indicators
    strong_shopping_keywords = {
        "buy", "shop", "cart", "checkout", "purchase", "add to cart",
        "buy now", "shop now", "add to bag", "in stock", "out of stock",
        "free shipping", "free delivery", "order now"
    }
    
    # Moderate shopping indicators
    moderate_shopping_keywords = {
        "price", "$", "sale", "discount", "deal", "offer",
        "clearance", "promo", "coupon", "shipping", "delivery",
        "store", "retailer", "available", "colors", "sizes"
    }
    
    # Count strong vs moderate signals
    strong_count = sum(1 for keyword in strong_shopping_keywords if keyword in content_text)
    moderate_count = sum(1 for keyword in moderate_shopping_keywords if keyword in content_text)
    
    # Known shopping domains get priority
    known_shopping_sites = {
        "amazon", "walmart", "target", "ebay", "etsy", "aliexpress",
        "shein", "alibaba", "temu", "dhgate", "wish", "asos",
        "zara", "hm.com", "h&m", "uniqlo", "forever21", "boohoo",
        "fashionnova", "prettylittlething", "missguided",
        "zaful", "romwe", "yesstyle", "lightinthebox",
        "nordstrom", "macys", "kohls", "jcpenney", "dillards",
        "saks", "bloomingdales", "neiman", "shopbop",
        "revolve", "nasty gal", "urban outfitters", "anthropologie",
        "free people", "lulus", "showpo", "tobi"
    }
    
    is_known_retailer = site and any(retailer in site.lower() for retailer in known_shopping_sites)
    
    # Less strict requirements to get more results:
    # Known retailer = automatic pass
    # OR at least 1 strong signal + 1 moderate signal
    # OR at least 2 moderate signals with price
    # OR at least 3 moderate signals
    if is_known_retailer:
        return True
    elif strong_count >= 1 and moderate_count >= 1:
        return True
    elif moderate_count >= 2 and '$' in content_text:
        return True
    elif moderate_count >= 3:
        return True
    
    return False


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


# Retailer scoring weights - focused on affordable clothing brands
DUPE_SITES = {
    "alibaba": 8,
    "aliexpress": 8,
    "shein": 9,
    "romwe": 8,
    "temu": 7,
    "dhgate": 6,
    "wish": 5,
    "zaful": 7,
    "rosegal": 6,
    "fashionnova": 7,
    "prettylittlething": 7,
    "boohoo": 7,
    "missguided": 7,
    "amazon": 9,
    "walmart": 8,
    "target": 8,
    "hm.com": 7,
    "zara": 7,
    "forever21": 7,
    "uniqlo": 7,
    "asos": 8,
    "yesstyle": 6,
    "lightinthebox": 6,
}

# Sites to exclude from results
EXCLUDED_SITES = {
    "youtube", "youtu.be", "tiktok", "instagram", "facebook", 
    "pinterest", "reddit", "twitter", "x.com", "vimeo",
    "dailymotion", "twitch", "snapchat", "linkedin",
    # Blog and article sites
    "medium", "wordpress", "blogspot", "tumblr", "wix",
    "squarespace", "weebly", "hubspot", "ghost.org",
    # News and article sites  
    "cnn", "bbc", "nytimes", "washingtonpost", "forbes",
    "buzzfeed", "huffpost", "vogue", "elle", "cosmopolitan",
    "harpersbazaar", "glamour", "allure", "marieclaire",
    "gq", "esquire", "menshealth", "womenshealth",
    # Tech/review sites
    "cnet", "techcrunch", "theverge", "engadget", "wired",
    "gizmodo", "mashable", "lifehacker", "digitaltrends",
    # Review and comparison sites (not shopping)
    "yelp", "tripadvisor", "glassdoor", "indeed",
    # Financial/advice sites
    "nerdwallet", "moneycrashers", "thebalance", "investopedia",
    "wisebread", "thepennyhoarder", "clark", "consumerreports",
    "dollarsprout", "moneysavingexpert", "frugalwoods", "millennial-money",
    # Wiki and reference sites
    "wikipedia", "wikihow", "fandom", "quora",
    # General content sites
    "about.com", "ehow", "wikimedia", "archive.org",
    # Lifestyle/blog sites
    "refinery29", "whowhatwear", "popsugar", "byrdie",
    "mydomaine", "thespruce", "apartmenttherapy",
    "soniabegonia", "fashionblogger", "styleblog",
    # Dupe/comparison blogs (articles, not shops)
    "amazingdupes", "dupes.com", "finddupes", "dupesfinder"
}

# Words that indicate non-shopping content
EXCLUDED_CONTENT_KEYWORDS = {
    "how to", "tutorial", "guide", "review", "article", 
    "blog", "news", "video", "watch", "subscribe",
    "diy", "makeup tutorial", "fashion week", "runway",
    "celebrity style", "red carpet", "interview",
    "tips", "advice", "inspiration", "trend report",
    "influencer", "sponsored", "partnership", "collaboration",
    "opinion", "editorial", "story", "feature",
    "best of", "top 10", "roundup", "listicle",
    "what to know", "everything you need", "complete guide",
    "how i", "my experience", "i tried", "testing",
    "comparison guide", "versus", "alternatives to consider"
}

# Article-specific URL patterns to exclude
ARTICLE_URL_PATTERNS = {
    "/blog/", "/article/", "/news/", "/post/", "/story/",
    "/review/", "/guide/", "/tips/", "/advice/", "/editorial/",
    "/magazine/", "/journal/", "/press/", "/media/"
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


def score_dupe(result: SearchResult, avg_price: Optional[float] = None, max_price: Optional[float] = None) -> DupeItem:
    """Calculate dupe score for a search result based on price savings and retailer quality"""
    site = extract_site(result.url) or ""
    base = 50
    bump = 0
    
    # Check if site is a recognized retailer
    retailer_score = 0
    for key, val in DUPE_SITES.items():
        if key in site:
            retailer_score = max(retailer_score, val)
            bump += retailer_score
    
    # Extract price
    price = extract_price(result.snippet or "")
    
    # Calculate savings score
    savings_bonus = 0
    savings_percent = 0
    if price is not None and max_price is not None and max_price > 0:
        # Calculate percentage savings vs highest price
        savings_percent = ((max_price - price) / max_price) * 100
        
        # Big bonus for significant savings
        if savings_percent >= 70:
            savings_bonus = 30  # 70%+ off = huge bonus
        elif savings_percent >= 50:
            savings_bonus = 25  # 50-70% off
        elif savings_percent >= 30:
            savings_bonus = 20  # 30-50% off
        elif savings_percent >= 20:
            savings_bonus = 15  # 20-30% off
        elif savings_percent >= 10:
            savings_bonus = 10  # 10-20% off
        
        bump += savings_bonus
        
        # Small bonus just for having a price
        bump += 5
    elif price is not None:
        # Has price but no comparison - small bonus
        bump += 5
    
    score = max(0, min(100, base + bump))
    
    # Generate detailed reason
    reasons = []
    if retailer_score > 0:
        if retailer_score >= 8:
            reasons.append("Top-rated retailer")
        else:
            reasons.append("Trusted retailer")
    
    if price is not None:
        if savings_percent >= 50:
            reasons.append(f"💰 {savings_percent:.0f}% cheaper!")
        elif savings_percent >= 20:
            reasons.append(f"Save {savings_percent:.0f}%")
        elif savings_percent > 0:
            reasons.append("Lower price")
        reasons.append(f"${price:.2f}")
    
    reason = " • ".join(reasons) if reasons else "Affordable option"
    
    # If no image was scraped, use a category-appropriate placeholder
    image_url = result.image
    if not image_url or not image_url.startswith('http'):
        # Use a simple colored placeholder
        image_url = "https://placehold.co/400x500/e5e7eb/6b7280?text=Product+Image"
    
    return DupeItem(
        title=result.title,
        url=result.url,
        snippet=result.snippet,
        site=site or None,
        price=price,
        dupeScore=score,
        reason=reason,
        image=image_url,
    )


@app.get("/dupes", response_model=DupeResponse)
async def dupes(
    q: str = Query(..., min_length=2, max_length=256),
    max_results: int = Query(16, ge=1, le=30),
):
    """Find affordable CLOTHING/FASHION dupes - focuses on cheaper alternatives"""
    # Enhanced query for clothing/fashion shopping with affordable focus
    compound_query = f"{q} clothing fashion buy cheap affordable dupe alternative"
    
    try:
        # Get MORE results (5x) since we're filtering for clothing specifically
        initial_results = min(max_results * 5, 50)
        print(f"Fetching {initial_results} initial results for query: {q}")
        raw = await tavily_search(compound_query, initial_results)  
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Provider error: {e}") from e
    
    # Filter for clothing/fashion and fetch images in parallel
    normalized = await normalize_with_images(raw, max_results * 2)
    
    print(f"After filtering, got {len(normalized)} clothing/fashion results")
    
    # Extract prices for comparison
    prices = [extract_price(r.snippet or "") for r in normalized]
    prices_with_values = [p for p in prices if p is not None]
    
    # Calculate price statistics
    avg_price = sum(prices_with_values) / len(prices_with_values) if prices_with_values else None
    max_price = max(prices_with_values) if prices_with_values else None
    min_price = min(prices_with_values) if prices_with_values else None
    
    print(f"Price analysis: min=${min_price}, max=${max_price}, avg=${avg_price}")
    
    # Score each item with price comparison
    items = [score_dupe(r, avg_price, max_price) for r in normalized]
    
    # Sort by score descending (best first)
    items.sort(key=lambda x: x.dupeScore, reverse=True)
    
    # Return all items up to max_results - prioritize cheaper ones if prices exist
    if prices_with_values:
        # Separate items with and without prices
        items_with_price = [item for item in items if item.price is not None]
        items_without_price = [item for item in items if item.price is None]
        
        # Sort items with price by actual price (cheapest first) within same score
        items_with_price.sort(key=lambda x: (x.price if x.price else 999999))
        
        # Combine: priced items first, then unpriced
        final_items = items_with_price + items_without_price
    else:
        # No prices found, just return by score
        final_items = items
    
    # Limit to requested results
    final_items = final_items[:max_results]
    
    print(f"Returning {len(final_items)} affordable clothing/fashion results")
    
    return DupeResponse(query=q, items=final_items)
