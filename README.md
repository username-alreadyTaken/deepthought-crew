# 🧠 MarketMind AI — Autonomous Market Research Agents

A Streamlit app that runs 5 AI agents in sequence to generate end-to-end market research for any idea.

## Quickstart

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=<key>...
streamlit run market_research_app.py
```

## Agents

| Agent | What it does |
|---|---|
| 📈 Trend Researcher | Emerging trends, keywords, sentiment, news signals |
| 🏢 Competitor Analyst | Competitor profiles, feature matrix, pricing landscape |
| 💬 Customer Voice | Pain points, customer language, what users love/hate |
| 🎯 Opportunity Finder | White spaces, strategic opportunities, MVP recommendations |
| 📋 Executive Summary | Synthesized summary with TL;DR |

## Advanced Options
- Target segment, geography, market size estimate
- Custom hypothesis / unique angle
- Toggle individual agents on/off
- Download full report as `.md`

## Tech Stack
- **Frontend**: Streamlit + custom CSS (Syne + DM Mono fonts, dark theme)
- **LLM**: Claude claude-sonnet-4-20250514 via Anthropic API (streaming)
- **Architecture**: Sequential multi-agent pipeline with context passing
