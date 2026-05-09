import requests
from app.config import settings

def run(state: dict) -> dict:
    ticker = state["ticker"]
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": ticker,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 5,
        "apiKey": settings.news_api_key
    }

    try:
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
        articles = res.json().get("articles", [])
        news = [
            {
                "title": a["title"],
                "source": a["source"]["name"],
                "published": a["publishedAt"],
                "url": a["url"]
            }
            for a in articles if a.get("title")
        ]
        print(f"[news_agent] fetched {len(news)} articles for {ticker}")
        return {"news": news}

    except Exception as e:
        print(f"[news_agent] error: {e}")
        return {"news": [], "error_msg": str(e)}