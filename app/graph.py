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

def build_graph():
    g = StateGraph(ResearchState)

    g.add_node("fetch_news",        news_agent.run)
    g.add_node("fetch_financials",  financials_agent.run)
    g.add_node("analyse_sentiment", sentiment_agent.run)
    g.add_node("write_report",      report_agent.run)

    # Flow: news → sentiment → report
    #       financials --------→ report
    g.set_entry_point("fetch_news")
    g.add_edge("fetch_news",        "fetch_financials")
    g.add_edge("fetch_financials",  "analyse_sentiment")
    g.add_edge("analyse_sentiment", "write_report")
    g.add_edge("write_report",      END)

    return g.compile()

research_graph = build_graph()