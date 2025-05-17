import os
import httpx
from datetime import datetime, timedelta
from app.services.cache import get_cache, set_cache
from app.services.api_client import call_news_api
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv("NEWS_API_KEY")

if not API_KEY:
    raise ValueError("❌ NEWS_API_KEY not found in .env")

BASE_URL = "https://newsapi.org/v2/everything"

# ✅ Synonym expansion
SYNONYMS = {
    "ai": ["artificial intelligence", "machine learning", "deep learning", "AI"],
    "climate": ["environment", "climate change", "global warming", "carbon emissions"],
    "sports": ["football", "soccer", "basketball", "tennis", "NBA", "FIFA"],
    "technology": ["tech news", "gadgets", "startups", "innovation", "computing"],
    "health": ["medicine", "healthcare", "mental health", "fitness", "wellness"],
    "politics": ["government", "elections", "lawmakers", "policy", "parliament"],
    "economy": ["stock market", "inflation", "recession", "GDP", "financial news"],
    "science": ["space", "research", "NASA", "experiments", "scientific discoveries"],
    "entertainment": ["movies", "celebrities", "TV shows", "Hollywood", "Netflix"],
    "education": ["schools", "universities", "online learning", "students", "academic"],
    "cybersecurity": ["data breach", "hacking", "cyber attacks", "malware", "phishing"],
    "business": ["entrepreneurship", "startups", "investments", "corporate", "mergers"],
    "travel": ["tourism", "destinations", "flights", "hotels", "vacation"],
    # Add more topics as needed
}

# 🔥 Fetch trending news
async def fetch_news(category: str = "AI"):
    print(f"🔥 Fetching HOT news for: {category}")
    today = datetime.utcnow()
    from_date = (today - timedelta(days=2)).strftime("%Y-%m-%d")

    keywords = SYNONYMS.get(category.strip().lower(), [category.strip()])
    collected_articles = []

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            for term in keywords:
                params = {
                    "q": term,
                    "language": "en",
                    "from": from_date,
                    "sortBy": "popularity",
                    "pageSize": 8,
                    "apiKey": API_KEY
                }
                response = await client.get(BASE_URL, params=params)
                response.raise_for_status()
                articles = response.json().get("articles", [])
                collected_articles.extend(articles)
    except Exception as e:
        print(f"❌ Error fetching news: {e}")
        return {"articles": []}

    return {"articles": collected_articles}


async def get_news_articles(category: str = "AI"):
    category = category.strip().lower()
    cache_key = f"news:{category}"

    # ✅ 1. Try to get from Redis cache first
    cached = get_cache(cache_key)
    if cached:
        print(f"✅ Loaded cached news for: {category}")
        return cached

    # 🔥 2. Fetch from API if not cached
    news_data = await fetch_news(category)
    raw_articles = news_data.get("articles", [])

    # ✅ 3. Keyword-based filtering (title + description)
    filtered = [
        a for a in raw_articles
        if category in (a.get("title", "") + a.get("description", "")).lower()
    ]

    # ✅ 4. Fallback if filter is empty
    articles_to_use = filtered if filtered else raw_articles

    # ✅ 5. Deduplicate by title
    seen_titles = set()
    unique_articles = []
    for a in articles_to_use:
        title = a.get("title", "")
        if title and title not in seen_titles:
            seen_titles.add(title)
            unique_articles.append(a)

    # ✅ 6. Format for frontend
    formatted = []
    for a in unique_articles:
        formatted.append({
            "title": a.get("title"),
            "summary": a.get("description"),
            "url": a.get("url"),
            "image": a.get("urlToImage"),
            "author": a.get("author"),
            "source": a.get("source", {}).get("name"),
            "published": a.get("publishedAt"),
            "content": a.get("content")
        })

    # ✅ 7. Store formatted result in Redis
    set_cache(cache_key, formatted, ttl=1800)  # 30 minutes

    return formatted
