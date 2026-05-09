from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from app.graph import research_graph
from app.db.supabase_client import get_client

app = FastAPI(
    title="Financial Research Agent",
    description="Multi-agent AI system for stock research",
    version="1.0.0"
)

class ResearchResponse(BaseModel):
    id: str
    ticker: str
    report_md: str
    sentiment_label: str
    sentiment_score: float
    created_at: str

@app.get("/")
def root():
    return {"status": "ok", "message": "Financial Research Agent is running"}

@app.post("/research", response_model=ResearchResponse)
def run_research(ticker: str):
    ticker = ticker.upper().strip()

    try:
        # Run the agent graph
        result = research_graph.invoke({
            "ticker": ticker,
            "news": [],
            "financials": {},
            "sentiment": {},
            "report_md": "",
            "error_msg": ""
        })

        # Save to Supabase
        db = get_client()
        row = db.table("research_runs").insert({
            "ticker": ticker,
            "status": "done",
            "report_md": result["report_md"],
            "sentiment_score": result["sentiment"].get("score", 0.0),
            "sentiment_label": result["sentiment"].get("label", "neutral"),
            "raw_news": result["news"],
            "raw_financials": result["financials"],
        }).execute()

        saved = row.data[0]
        return ResearchResponse(
            id=saved["id"],
            ticker=saved["ticker"],
            report_md=saved["report_md"],
            sentiment_label=saved["sentiment_label"],
            sentiment_score=saved["sentiment_score"],
            created_at=saved["created_at"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/reports")
def list_reports():
    db = get_client()
    res = db.table("research_runs")\
        .select("id, ticker, sentiment_label, sentiment_score, created_at")\
        .order("created_at", desc=True)\
        .limit(20)\
        .execute()
    return res.data