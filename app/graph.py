# from typing import TypedDict
# from langgraph.graph import StateGraph, END
# from app.agents import news_agent, financials_agent, sentiment_agent, report_agent

# class ResearchState(TypedDict):
#     ticker: str
#     news: list
#     financials: dict
#     sentiment: dict
#     report_md: str
#     error_msg: str

# def build_graph():
#     g = StateGraph(ResearchState)

#     g.add_node("fetch_news",        news_agent.run)
#     g.add_node("fetch_financials",  financials_agent.run)
#     g.add_node("analyse_sentiment", sentiment_agent.run)
#     g.add_node("write_report",      report_agent.run)

#     # Flow: news → sentiment → report
#     #       financials --------→ report
#     g.set_entry_point("fetch_news")
#     g.add_edge("fetch_news",        "fetch_financials")
#     g.add_edge("fetch_financials",  "analyse_sentiment")
#     g.add_edge("analyse_sentiment", "write_report")
#     g.add_edge("write_report",      END)

#     return g.compile()

# research_graph = build_graph()


from typing import TypedDict
from langgraph.graph import StateGraph, END
from app.agents import news_agent, financials_agent, sentiment_agent, report_agent


class ResearchState(TypedDict):
    ticker: str
    news: list
    financials: dict
    sentiment: dict
    report_md: str
    error_msg: str


def safe_news(state: ResearchState) -> dict:
    try:
        return news_agent.run(state)
    except Exception as e:
        print(f"[graph] news_agent failed: {e}")
        return {"news": [], "error_msg": str(e)}


def safe_financials(state: ResearchState) -> dict:
    try:
        return financials_agent.run(state)
    except Exception as e:
        print(f"[graph] financials_agent failed: {e}")
        return {"financials": {"ticker": state["ticker"], "error": str(e)}}


def safe_sentiment(state: ResearchState) -> dict:
    try:
        return sentiment_agent.run(state)
    except Exception as e:
        print(f"[graph] sentiment_agent failed: {e}")
        return {"sentiment": {"score": 0.0, "label": "neutral", "reasoning": str(e)}}


def safe_report(state: ResearchState) -> dict:
    try:
        return report_agent.run(state)
    except Exception as e:
        print(f"[graph] report_agent failed: {e}")
        return {"report_md": f"# {state['ticker']} Research Report\n\nError generating report: {str(e)}"}


def build_graph():
    g = StateGraph(ResearchState)

    # Register all nodes with safe wrappers
    g.add_node("fetch_news",        safe_news)
    g.add_node("fetch_financials",  safe_financials)
    g.add_node("analyse_sentiment", safe_sentiment)
    g.add_node("write_report",      safe_report)

    # Flow:
    # fetch_news → fetch_financials → analyse_sentiment → write_report → END
    g.set_entry_point("fetch_news")
    g.add_edge("fetch_news",        "fetch_financials")
    g.add_edge("fetch_financials",  "analyse_sentiment")
    g.add_edge("analyse_sentiment", "write_report")
    g.add_edge("write_report",      END)

    return g.compile()


# Singleton — imported by main.py
research_graph = build_graph()