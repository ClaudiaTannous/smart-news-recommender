import os
import httpx
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv("NEWS_API_KEY")

if not API_KEY:
    raise ValueError("❌ NEWS_API_KEY not found in .env")

BASE_URL = "https://newsapi.org/v2/everything"

# 🔥 Fetch HOTTEST news
async def fetch_news(category: str = "AI"):
    print(f"🔥 Fetching HOT news for: {category}")

    # Only get articles from last 2 days
    today = datetime.utcnow()
    from_date = (today - timedelta(days=2)).strftime("%Y-%m-%d")

    params = {
        "q": category,
        "language": "en",
        "from": from_date,
        "sortBy": "popularity",   # 🔥 Trending news
        "pageSize": 8,
        "apiKey": API_KEY
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(BASE_URL, params=params)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        print(f"❌ Error fetching news: {e}")
        return {"articles": []}

# 🔄 Format for display
async def get_news_articles(category: str = "AI"):
    news_data = await fetch_news(category)
    articles = news_data.get("articles", [])

    formatted = []
    for a in articles:
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
    return formatted
