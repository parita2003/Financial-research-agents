# 🤖 Financial Research Agent

> An autonomous multi-agent AI system that researches any stock ticker in seconds —
> fetching live news, financial metrics, sentiment analysis, and generating a structured
> investment report. Built with LangGraph, Groq LLM, and FastAPI.

---

## 📸 What It Does

Give it a stock ticker like `AAPL` or `TSLA` and it:

1. 📰 Fetches the 5 latest news articles about the company
2. 📊 Pulls live financial metrics (price, P/E, EPS, revenue, market cap)
3. 🧠 Analyses sentiment of the news using an LLM (bullish / bearish score)
4. 📝 Writes a structured research report with summary, risks, and outlook
5. 💾 Saves the report to a database with a unique ID
6. 🌐 Returns everything as a clean JSON API response

**Sample output for AAPL:**
```json
{
  "ticker": "AAPL",
  "sentiment_label": "bullish",
  "sentiment_score": 0.8,
  "report_md": "# AAPL Research Report\n## Executive Summary\nApple Inc. is a technology giant..."
}
```

---

## 🏗️ System Architecture

```
POST /research?ticker=AAPL
        │
        ▼
┌─────────────────────────┐
│   FastAPI (main.py)     │  ← Entry point, handles HTTP
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  LangGraph Orchestrator │  ← State machine, runs agents in sequence
│       (graph.py)        │
└────────────┬────────────┘
             │
    ┌────────┼────────┬──────────┐
    ▼        ▼        ▼          ▼
┌───────┐ ┌──────┐ ┌─────────┐ ┌────────┐
│ News  │ │ Fin. │ │Sentiment│ │Report  │
│Agent  │ │Agent │ │ Agent   │ │Writer  │
└───┬───┘ └──┬───┘ └────┬────┘ └───┬────┘
    │        │          │          │
    ▼        ▼          ▼          ▼
NewsAPI  yfinance    Groq LLM   Groq LLM
                   (scoring)  (writing)
             │
             ▼
    ┌─────────────────┐
    │    Supabase     │  ← Stores every research run
    │   (Postgres)    │
    └─────────────────┘
```

---

## 🧩 Agent Breakdown

| Agent | File | Tool Used | What It Does |
|---|---|---|---|
| News Fetcher | `agents/news_agent.py` | NewsAPI | Fetches 5 latest articles for the ticker |
| Financials | `agents/financials_agent.py` | yfinance | Pulls price, P/E, EPS, revenue, market cap |
| Sentiment | `agents/sentiment_agent.py` | Groq LLM | Scores news sentiment from -1 (bearish) to +1 (bullish) |
| Report Writer | `agents/report_agent.py` | Groq LLM | Synthesises all data into a structured markdown report |

---

## 🛠️ Tech Stack

| Category | Technology | Why Chosen |
|---|---|---|
| **Language** | Python 3.11 | Best ecosystem for AI/ML |
| **Web Framework** | FastAPI | Fast, async, auto-generates Swagger docs |
| **AI Orchestration** | LangGraph | Production-grade state machine for multi-agent flows |
| **LLM** | Groq (llama-3.3-70b) | Free tier, fastest inference available |
| **Finance Data** | yfinance | Free, no API key needed, reliable |
| **News Data** | NewsAPI | Free tier, 100 req/day |
| **Database** | Supabase (Postgres) | Free hosted Postgres, instant setup |
| **Hosting** | Railway | Free tier, deploys directly from GitHub |
| **Data Validation** | Pydantic | Type-safe request/response models |

**100% free stack — $0 to run.**

---

## 📁 Project Structure

```
financial-research-agent/
│
├── app/
│   ├── __init__.py
│   ├── main.py               # FastAPI app — API endpoints
│   ├── graph.py              # LangGraph state machine — orchestrates agents
│   ├── config.py             # Loads env vars via pydantic-settings
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── news_agent.py         # Fetches news from NewsAPI
│   │   ├── financials_agent.py   # Pulls stock data from yfinance
│   │   ├── sentiment_agent.py    # LLM sentiment scoring via Groq
│   │   └── report_agent.py       # LLM report generation via Groq
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   └── supabase_client.py    # Supabase connection client
│   │
│   └── tools/
│       └── __init__.py           # Reserved for future tool integrations
│
├── .env                      # Local secrets (never committed to git)
├── .env.example              # Template showing required keys
├── .gitignore                # Excludes .env, venv, pycache
├── requirements.txt          # All Python dependencies
├── railway.toml              # Railway deployment config
├── Procfile                  # Fallback start command for Railway
└── README.md                 # This file
```

---

## 🚀 How to Run Locally

### Prerequisites
- Python 3.11+
- Git

### Step 1 — Clone the repo
```bash
git clone https://github.com/parita2003/Financial-research-agents.git
cd Financial-research-agents
```

### Step 2 — Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Set up environment variables
```bash
copy .env.example .env       # Windows
# cp .env.example .env       # Mac/Linux
```

Open `.env` and fill in your keys:

```env
GROQ_API_KEY=gsk_your_key_here
GROQ_MODEL=llama-3.3-70b-versatile
NEWS_API_KEY=your_newsapi_key
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key
```

### Step 5 — Set up the database
Go to your Supabase project → SQL Editor → run:

```sql
create table research_runs (
  id uuid primary key default gen_random_uuid(),
  ticker text not null,
  created_at timestamptz default now(),
  status text default 'pending',
  report_md text,
  sentiment_score float,
  sentiment_label text,
  raw_news jsonb,
  raw_financials jsonb,
  error_msg text
);
```

Also disable RLS:
```sql
alter table research_runs disable row level security;
```

### Step 6 — Start the server
```bash
python -m uvicorn app.main:app --reload
```

Server runs at: `http://localhost:8000`

---

## 🌐 API Endpoints

### `GET /`
Health check.
```json
{ "status": "ok", "message": "Financial Research Agent is running" }
```

### `POST /research?ticker=AAPL`
Run full research on a stock. Triggers all 4 agents.

**Response:**
```json
{
  "id": "uuid",
  "ticker": "AAPL",
  "report_md": "# AAPL Research Report...",
  "sentiment_label": "bullish",
  "sentiment_score": 0.8,
  "created_at": "2026-05-09T10:00:00Z"
}
```

### `GET /reports`
Returns last 20 research runs from the database.

**Interactive docs:** `http://localhost:8000/docs`

---

## 🔑 Where to Get Free API Keys

| Key | URL | Free Tier |
|---|---|---|
| `GROQ_API_KEY` | https://console.groq.com | 500 req/day |
| `NEWS_API_KEY` | https://newsapi.org/register | 100 req/day |
| `SUPABASE_URL` + `SUPABASE_ANON_KEY` | https://supabase.com | 500MB free |

---

## ☁️ Deployment (Railway)

1. Push code to GitHub
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Select this repo
4. Go to **Variables** tab → add all 5 env vars from your `.env`
5. Railway auto-deploys on every push to `main`

Live URL format: `https://your-app.up.railway.app`

---

## 💡 Key Engineering Decisions

**Why LangGraph over CrewAI?**
LangGraph gives explicit control over state transitions. Every agent input/output is typed via `TypedDict`, making it easy to debug, extend, and add retry logic. CrewAI abstracts too much for production use.

**Why Groq over OpenAI?**
Groq's free tier is generous (500 req/day) and inference is 10x faster than OpenAI on the same model size. For a demo/portfolio project, there's no reason to pay.

**Why Supabase over MongoDB Atlas?**
The data is relational (one run → many fields). Postgres is the right tool. Supabase gives a free hosted Postgres with a REST API out of the box — no ORM setup needed.

**Why sequential agents instead of parallel?**
The sentiment agent depends on news output, and the report agent depends on all three agents. True parallelism is only possible for news + financials. Sequential keeps the code simple and debuggable for a v1.

---

## 🗺️ Roadmap (Future Improvements)

- [ ] Run news + financials agents in true parallel using `asyncio.gather`
- [ ] Add a `GET /research/{ticker}` endpoint to fetch cached reports
- [ ] Add rate limiting per IP using `slowapi`
- [ ] Add a React frontend dashboard to display reports
- [ ] Support portfolio analysis (multiple tickers in one request)
- [ ] Add FinBERT as an alternative to Groq for offline sentiment analysis
- [ ] Add email/Slack notifications when sentiment crosses a threshold

---

## 👩‍💻 Author

**Parita** — [github.com/parita2003](https://github.com/parita2003)

---

## 📄 License

MIT License — free to use, modify, and distribute.