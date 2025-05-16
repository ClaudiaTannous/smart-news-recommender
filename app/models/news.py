from pydantic import BaseModel

class NewsArticle(BaseModel):
    title: str
    summary: str
    url: str
    source: str
