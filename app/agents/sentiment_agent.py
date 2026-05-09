import json
from groq import Groq
from app.config import settings

client = Groq(api_key=settings.groq_api_key)

def run(state: dict) -> dict:
    ticker = state["ticker"]
    news = state.get("news", [])

    if not news:
        return {"sentiment": {"score": 0.0, "label": "neutral", "reasoning": "No news available"}}

    headlines = "\n".join([f"- {a['title']}" for a in news])

    prompt = f"""You are a financial sentiment analyst.
Analyse the sentiment of these news headlines about {ticker}.

Headlines:
{headlines}

Respond ONLY with a JSON object in this exact format, no extra text:
{{
  "score": <float between -1.0 (very bearish) and 1.0 (very bullish)>,
  "label": "<one of: bearish, slightly_bearish, neutral, slightly_bullish, bullish>",
  "reasoning": "<one sentence explanation>"
}}"""

    try:
        res = client.chat.completions.create(
            model=settings.groq_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        raw = res.choices[0].message.content.strip()
        sentiment = json.loads(raw)
        print(f"[sentiment_agent] {ticker} → {sentiment['label']} (score: {sentiment['score']})")
        return {"sentiment": sentiment}

    except Exception as e:
        print(f"[sentiment_agent] error: {e}")
        return {"sentiment": {"score": 0.0, "label": "neutral", "reasoning": str(e)}}