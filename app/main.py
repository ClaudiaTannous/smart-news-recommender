from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.api.routes import router
from app.services.fetch_data import get_news_articles

import os
from dotenv import load_dotenv
load_dotenv()  # 🔑 Load NEWS_API_KEY from .env

# ✅ Initialize FastAPI
app = FastAPI(title="Smart News Recommender API")

# ✅ Mount static folder for custom CSS
app.mount("/static", StaticFiles(directory="static"), name="static")

# ✅ Set up Jinja2 templates folder
templates = Jinja2Templates(directory="templates")

# ✅ Include your JSON API routes (e.g., /recommend-news)
app.include_router(router)

# ✅ Redirect root to the pretty HTML news page
@app.get("/")
def root():
    return RedirectResponse(url="/recommend-news-page?category=technology")

# ✅ HTML news page with full article info
@app.get("/recommend-news-page")
async def pretty_news_page(request: Request, category: str = "technology"):
    articles = await get_news_articles(category)

    # Handle error (like API key missing or API failure)
    if isinstance(articles, dict) and "error" in articles:
        return templates.TemplateResponse("news.html", {
            "request": request,
            "articles": [],
            "query": category,
            "error": articles["error"]
        })

    return templates.TemplateResponse("news.html", {
        "request": request,
        "articles": articles,
        "query": category,
        "error": None
    })
