from fastapi import APIRouter, Query
from typing import List
from app.services.fetch_data import get_news_articles
from app.models.news import NewsArticle

router = APIRouter()

@router.get("/recommend-news", response_model=List[NewsArticle])
def recommend_news(query: str = Query("AI")):
    return get_news_articles(query)
