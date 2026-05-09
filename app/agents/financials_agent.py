import yfinance as yf
from app.config import settings

def run(state: dict) -> dict:
    ticker = state["ticker"]

    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        financials = {
            "ticker": ticker,
            "company_name": info.get("longName", "N/A"),
            "sector": info.get("sector", "N/A"),
            "market_cap": info.get("marketCap", "N/A"),
            "current_price": info.get("currentPrice", "N/A"),
            "pe_ratio": info.get("trailingPE", "N/A"),
            "eps": info.get("trailingEps", "N/A"),
            "52w_high": info.get("fiftyTwoWeekHigh", "N/A"),
            "52w_low": info.get("fiftyTwoWeekLow", "N/A"),
            "revenue": info.get("totalRevenue", "N/A"),
            "profit_margin": info.get("profitMargins", "N/A"),
            "analyst_rating": info.get("recommendationKey", "N/A"),
        }

        print(f"[financials_agent] fetched data for {ticker}: {financials['company_name']}")
        return {"financials": financials}

    except Exception as e:
        print(f"[financials_agent] error: {e}")
        return {"financials": {}, "error_msg": str(e)}