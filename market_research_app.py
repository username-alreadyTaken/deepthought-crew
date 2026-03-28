import streamlit as st
import anthropic
import json
import time
from datetime import datetime

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MarketMind AI · Autonomous Research",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&display=swap');

  :root {
    --bg: #0a0d14;
    --surface: #111520;
    --surface2: #181d2e;
    --border: #1e2540;
    --accent: #4f8cff;
    --accent2: #a78bfa;
    --accent3: #34d399;
    --accent4: #fb923c;
    --accent5: #f472b6;
    --text: #e2e8f0;
    --muted: #64748b;
    --code: #94a3b8;
  }

  html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: var(--bg) !important;
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
  }

  [data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
  }

  h1, h2, h3, h4 {
    font-family: 'Syne', sans-serif !important;
  }

  .block-container { padding-top: 1.5rem !important; }

  /* Header */
  .mm-header {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 2rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid var(--border);
  }
  .mm-logo {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -1px;
  }
  .mm-tagline {
    font-size: 0.85rem;
    color: var(--muted);
    font-family: 'DM Mono', monospace;
  }

  /* Agent Cards */
  .agent-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
  }
  .agent-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
  }
  .agent-trend::before   { background: linear-gradient(90deg, var(--accent), #60a5fa); }
  .agent-comp::before    { background: linear-gradient(90deg, var(--accent2), #c084fc); }
  .agent-voice::before   { background: linear-gradient(90deg, var(--accent3), #6ee7b7); }
  .agent-opp::before     { background: linear-gradient(90deg, var(--accent4), #fbbf24); }
  .agent-exec::before    { background: linear-gradient(90deg, var(--accent5), var(--accent)); }

  .agent-title {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 0.75rem;
  }
  .agent-badge {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    padding: 3px 10px;
    border-radius: 99px;
    font-weight: 500;
    letter-spacing: 0.5px;
  }
  .badge-trend  { background: rgba(79,140,255,0.15); color: var(--accent); }
  .badge-comp   { background: rgba(167,139,250,0.15); color: var(--accent2); }
  .badge-voice  { background: rgba(52,211,153,0.15);  color: var(--accent3); }
  .badge-opp    { background: rgba(251,146,60,0.15);  color: var(--accent4); }
  .badge-exec   { background: rgba(244,114,182,0.15); color: var(--accent5); }

  .agent-content {
    font-size: 0.9rem;
    line-height: 1.7;
    color: var(--text);
  }
  .agent-content p { margin-bottom: 0.6rem; }
  .agent-content ul { margin: 0.4rem 0 0.8rem 1.2rem; }
  .agent-content li { margin-bottom: 0.35rem; }
  .agent-content strong { color: white; }
  .agent-content h3, .agent-content h4 {
    color: white;
    margin-top: 1rem;
    margin-bottom: 0.4rem;
  }

  /* Status pill */
  .status-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    padding: 4px 12px;
    border-radius: 99px;
    margin-bottom: 1rem;
  }
  .status-running { background: rgba(79,140,255,0.12); color: var(--accent); border: 1px solid rgba(79,140,255,0.3); }
  .status-done    { background: rgba(52,211,153,0.12); color: var(--accent3); border: 1px solid rgba(52,211,153,0.3); }
  .status-wait    { background: rgba(100,116,139,0.12); color: var(--muted); border: 1px solid rgba(100,116,139,0.3); }

  /* Sidebar inputs */
  [data-testid="stTextInput"] input,
  [data-testid="stTextArea"] textarea,
  [data-testid="stSelectbox"] select {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
  }

  /* Buttons */
  [data-testid="stButton"] button {
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 0.6rem 1.5rem !important;
    transition: opacity 0.2s ease !important;
    width: 100%;
  }
  [data-testid="stButton"] button:hover { opacity: 0.88 !important; }

  /* Param tags */
  .param-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 0.5rem;
    margin-bottom: 1rem;
  }
  .param-tag {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 4px 12px;
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    color: var(--muted);
  }
  .param-tag span { color: var(--text); }

  /* Empty state */
  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 5rem 2rem;
    text-align: center;
    color: var(--muted);
  }
  .empty-icon { font-size: 3.5rem; margin-bottom: 1rem; opacity: 0.5; }
  .empty-title { font-family: 'Syne', sans-serif; font-size: 1.4rem; color: var(--text); margin-bottom: 0.5rem; }
  .empty-sub   { font-size: 0.9rem; max-width: 380px; line-height: 1.6; }

  /* Progress bar override */
  [data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, var(--accent), var(--accent2)) !important;
  }

  /* Expander */
  [data-testid="stExpander"] {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
  }

  /* Metric */
  [data-testid="metric-container"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 1rem !important;
  }

  /* Divider */
  hr { border-color: var(--border) !important; }

  /* Scrollbar */
  ::-webkit-scrollbar { width: 6px; }
  ::-webkit-scrollbar-track { background: var(--bg); }
  ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Anthropic Client ──────────────────────────────────────────────────────────
@st.cache_resource
def get_client():
    return anthropic.Anthropic()

# ── Agent Prompts ─────────────────────────────────────────────────────────────

def trend_prompt(idea, params):
    extra = f"""
- Target Segment: {params.get('segment', 'General market')}
- Geography: {params.get('geography', 'Global')}
- Timeframe: {params.get('timeframe', 'Current')}
""" if params else ""
    return f"""You are a Trend Researcher Agent specializing in market intelligence.

Idea/Product: {idea}
{extra}

Perform a comprehensive trend analysis. Structure your response with these sections:

## 📈 Emerging Trends
List 4-6 key trends relevant to this idea (growth signals, technology shifts, consumer behavior changes).
For each trend give: trend name, brief description, estimated growth indicator (e.g. +X% YoY or rising/declining).

## 🔥 Trending Keywords & Topics
List the top search and discussion keywords. Mention where they trend (Reddit communities, Twitter/X, news outlets).

## 📰 Recent News Signals
Summarize 3-5 hypothetical but realistic recent news headlines/events that would affect this market.

## 🌊 Sentiment Overview
Overall sentiment in the market: positive / mixed / negative. Why?

## ⚡ Trend Summary
One paragraph synthesizing the most important trend insights for this idea.

Be specific, data-driven in style, and actionable. Format with markdown headers and bullet points."""


def competitor_prompt(idea, params):
    extra = f"""
- Target Segment: {params.get('segment', 'General market')}
- Geography: {params.get('geography', 'Global')}
- Market Size Estimate: {params.get('market_size', 'Unknown')}
""" if params else ""
    return f"""You are a Competitor Analyst Agent specializing in competitive intelligence.

Idea/Product: {idea}
{extra}

Analyze the competitive landscape. Structure your response:

## 🏢 Key Competitors (5–7 players)
For each competitor provide a mini-profile:
- **Name** | Type (startup/enterprise/SaaS) | Est. pricing
- Core features (2-3 bullets)
- Strength & Weakness (1 each)
- Target customer

## 📊 Feature Comparison Matrix
Create a text-based comparison table of 5 key features across the top 3-4 competitors.

## 💰 Pricing Landscape
Overview of how competitors are priced: free tiers, freemium, subscription ranges, enterprise deals.

## 🎯 Competitive Positioning Map
Describe where each competitor sits on two axes: (1) Price: Low→High and (2) Automation: Manual→Fully Automated.

## 🔍 Competitive Summary
One paragraph on the overall competitive landscape: crowded? fragmented? dominated by one player?

Be specific with realistic company names and data. Use markdown formatting."""


def voice_prompt(idea, params):
    extra = f"""
- Target Segment: {params.get('segment', 'General market')}
- Geography: {params.get('geography', 'Global')}
""" if params else ""
    return f"""You are a Customer Voice Analyst Agent specializing in qualitative research and NLP.

Idea/Product: {idea}
{extra}

Synthesize what real customers say about this space. Structure your response:

## 😤 Top Pain Points (ranked by frequency)
List 5-7 pain points with:
- Pain point name
- Customer language quote (realistic verbatim style, like from Reddit/Twitter/reviews)
- Intensity: 🔴 High / 🟡 Medium / 🟢 Low
- Source context (e.g. "r/entrepreneur", "G2 reviews", "Twitter")

## 💬 Customer Language & Vocabulary
What exact words/phrases do customers use? This is gold for messaging.
List 8-10 key phrases from real user discussions.

## 🌟 What Customers Love (about existing solutions)
3-5 things customers praise in current solutions.

## 🚩 What Customers Hate
3-5 recurring frustrations with current solutions (the "jobs not being done").

## 👥 Customer Segments Observed
2-3 distinct customer sub-segments based on their complaints/needs. Brief profile for each.

## 💡 Voice Summary
One paragraph synthesizing the key customer insights for building this product.

Write in a realistic, grounded style. Quote customer language authentically."""


def opportunity_prompt(idea, params, trend_out, comp_out, voice_out):
    extra = f"""
- Target Segment: {params.get('segment', 'General market')}
- Geography: {params.get('geography', 'Global')}
- Market Size Estimate: {params.get('market_size', 'Unknown')}
- Unique Angle: {params.get('unique_angle', 'None specified')}
""" if params else ""
    return f"""You are an Opportunity Finder Agent. You synthesize competitive intelligence, trend data, and customer voice to find market white spaces.

Idea/Product: {idea}
{extra}

--- TREND RESEARCH OUTPUT ---
{trend_out}

--- COMPETITOR ANALYSIS OUTPUT ---
{comp_out}

--- CUSTOMER VOICE OUTPUT ---
{voice_out}
---

Now identify high-value opportunities. Structure your response:

## 🎯 Market Gaps (White Spaces)
List 3-5 specific unmet needs or underserved segments. For each:
- Gap description
- Evidence (from trends + competitor analysis + customer voice)
- Opportunity size: Large / Medium / Niche

## 🚀 Top Strategic Opportunities (Ranked)
Rank the top 3 opportunities with:
1. Opportunity name
2. Why now (timing signal)
3. Who wins (ideal customer profile)
4. Winning feature/approach
5. Risk level: Low / Medium / High

## ⚡ Differentiation Angles
3 ways to build a defensible position vs. existing players.

## 💰 Business Model Recommendations
2-3 recommended monetization approaches with rationale.

## 📐 MVP Recommendations
What the first version of this product should focus on (3-5 prioritized features).

## 🧭 Strategic Summary
One compelling paragraph: the single most exciting opportunity in this space and why your idea can win.

Be bold, specific, and actionable."""


def exec_summary_prompt(idea, params, trend_out, comp_out, voice_out, opp_out):
    return f"""You are a Senior Market Research Strategist. Synthesize all agent findings into a crisp executive summary.

Idea: {idea}

Write a structured executive summary (400-500 words) with:

## Executive Summary

**The Opportunity** (2-3 sentences on market size + timing)

**Market Landscape** (2-3 sentences on competition)

**Customer Insights** (2-3 sentences on key pain points)

**Our Edge** (2-3 sentences on differentiation opportunity)

**Recommended Action** (2-3 sentences: what to build, who to target, how to win)

**Risk Factors** (3 bullets)

**Key Metrics to Track** (3 bullets)

Then append:
## TL;DR
One sentence that captures the entire opportunity.

Use professional language. Be direct and decisive."""


# ── Run Agent with streaming ──────────────────────────────────────────────────
def run_agent_streaming(prompt, placeholder):
    client = get_client()
    full_text = ""
    with client.messages.stream(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        for text in stream.text_stream:
            full_text += text
            placeholder.markdown(full_text + "▌")
    placeholder.markdown(full_text)
    return full_text


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 0.5rem 0 1.5rem;">
      <div style="font-family:'Syne',sans-serif; font-size:1.4rem; font-weight:800;
                  background:linear-gradient(135deg,#4f8cff,#a78bfa);
                  -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
        🧠 MarketMind AI
      </div>
      <div style="font-family:'DM Mono',monospace; font-size:0.7rem; color:#64748b; margin-top:2px;">
        Autonomous Research Agents
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Your Idea")
    idea = st.text_area(
        "Describe your product / idea",
        placeholder="e.g. An AI-powered tool that automates market research for early-stage startups using multi-agent workflows...",
        height=120,
        label_visibility="collapsed",
    )

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # Advanced options
    with st.expander("⚙️ Advanced Parameters", expanded=False):
        segment = st.text_input("Target Segment", placeholder="e.g. B2B SaaS, SMBs, Gen Z consumers")
        geography = st.selectbox("Geography", ["Global", "North America", "Europe", "Asia-Pacific", "India", "Other"])
        market_size = st.text_input("Estimated Market Size", placeholder="e.g. $5B TAM")
        timeframe = st.selectbox("Trend Timeframe", ["Current (2025–2026)", "12 months", "3 years", "5 years"])
        unique_angle = st.text_input("Your Unique Angle / Hypothesis", placeholder="e.g. Focus on solopreneurs, not enterprises")

        st.markdown("**Agents to Run**")
        run_trend = st.checkbox("📈 Trend Researcher", value=True)
        run_comp  = st.checkbox("🏢 Competitor Analyst", value=True)
        run_voice = st.checkbox("💬 Customer Voice", value=True)
        run_opp   = st.checkbox("🎯 Opportunity Finder", value=True)
        run_exec  = st.checkbox("📋 Executive Summary", value=True)
    else:
        segment = ""; geography = "Global"; market_size = ""
        timeframe = "Current (2025–2026)"; unique_angle = ""
        run_trend = run_comp = run_voice = run_opp = run_exec = True

    params = {
        "segment": segment, "geography": geography,
        "market_size": market_size, "timeframe": timeframe,
        "unique_angle": unique_angle
    }

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    go = st.button("🚀 Run Research", use_container_width=True)

    st.markdown("<hr style='margin:1.5rem 0'>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-family:'DM Mono',monospace; font-size:0.7rem; color:#64748b; line-height:1.8;">
      <div>📈 Trend Researcher</div>
      <div>🏢 Competitor Analyst</div>
      <div>💬 Customer Voice</div>
      <div>🎯 Opportunity Finder</div>
      <div>📋 Executive Summary</div>
    </div>
    """, unsafe_allow_html=True)


# ── Main Area ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="mm-header">
  <div>
    <div class="mm-logo">MarketMind AI</div>
    <div class="mm-tagline">// Autonomous · Multi-Agent · Market Intelligence</div>
  </div>
</div>
""", unsafe_allow_html=True)

# State
if "results" not in st.session_state:
    st.session_state.results = {}
if "last_idea" not in st.session_state:
    st.session_state.last_idea = ""

# ── Show param tags when idea present ────────────────────────────────────────
if st.session_state.last_idea:
    tags_html = f"""<div class="param-row">
      <div class="param-tag">Idea: <span>{st.session_state.last_idea[:60]}{'...' if len(st.session_state.last_idea) > 60 else ''}</span></div>"""
    if segment: tags_html += f'<div class="param-tag">Segment: <span>{segment}</span></div>'
    if geography != "Global": tags_html += f'<div class="param-tag">Geo: <span>{geography}</span></div>'
    if market_size: tags_html += f'<div class="param-tag">Market: <span>{market_size}</span></div>'
    tags_html += "</div>"
    st.markdown(tags_html, unsafe_allow_html=True)


# ── RUN ───────────────────────────────────────────────────────────────────────
if go:
    if not idea.strip():
        st.warning("⚠️ Please enter your idea or product description.")
        st.stop()

    st.session_state.results = {}
    st.session_state.last_idea = idea

    agents = []
    if run_trend: agents.append(("trend", "📈 Trend Researcher", "agent-trend", "badge-trend"))
    if run_comp:  agents.append(("comp",  "🏢 Competitor Analyst", "agent-comp",  "badge-comp"))
    if run_voice: agents.append(("voice", "💬 Customer Voice",    "agent-voice", "badge-voice"))
    if run_opp:   agents.append(("opp",   "🎯 Opportunity Finder","agent-opp",   "badge-opp"))
    if run_exec:  agents.append(("exec",  "📋 Executive Summary", "agent-exec",  "badge-exec"))

    total = len(agents)
    prog  = st.progress(0, text="Initializing agents...")

    for i, (key, label, card_cls, badge_cls) in enumerate(agents):
        pct = int((i / total) * 100)
        prog.progress(pct, text=f"Running {label} ({i+1}/{total})...")

        st.markdown(f"""
        <div class="agent-card {card_cls}">
          <div class="agent-title">
            {label}
            <span class="agent-badge {badge_cls}">RUNNING</span>
          </div>
        """, unsafe_allow_html=True)

        placeholder = st.empty()

        try:
            if key == "trend":
                prompt = trend_prompt(idea, params)
            elif key == "comp":
                prompt = competitor_prompt(idea, params)
            elif key == "voice":
                prompt = voice_prompt(idea, params)
            elif key == "opp":
                prompt = opportunity_prompt(
                    idea, params,
                    st.session_state.results.get("trend", "N/A"),
                    st.session_state.results.get("comp", "N/A"),
                    st.session_state.results.get("voice", "N/A"),
                )
            elif key == "exec":
                prompt = exec_summary_prompt(
                    idea, params,
                    st.session_state.results.get("trend", "N/A"),
                    st.session_state.results.get("comp", "N/A"),
                    st.session_state.results.get("voice", "N/A"),
                    st.session_state.results.get("opp", "N/A"),
                )

            result = run_agent_streaming(prompt, placeholder)
            st.session_state.results[key] = result

        except Exception as e:
            placeholder.error(f"Agent error: {str(e)}")
            st.session_state.results[key] = f"Error: {str(e)}"

        st.markdown("</div>", unsafe_allow_html=True)

    prog.progress(100, text="✅ All agents complete!")
    time.sleep(0.5)
    prog.empty()

    # Download
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    report_md = f"# MarketMind AI Report\n**Idea:** {idea}\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
    for key, label, _, _ in agents:
        if key in st.session_state.results:
            report_md += f"\n---\n\n## {label}\n\n{st.session_state.results[key]}\n"

    st.download_button(
        label="⬇️ Download Full Report (.md)",
        data=report_md,
        file_name=f"marketmind_report_{ts}.md",
        mime="text/markdown",
        use_container_width=True,
    )


# ── Restore previous results ──────────────────────────────────────────────────
elif st.session_state.results and not go:
    label_map = {
        "trend": ("📈 Trend Researcher",  "agent-trend", "badge-trend"),
        "comp":  ("🏢 Competitor Analyst","agent-comp",  "badge-comp"),
        "voice": ("💬 Customer Voice",    "agent-voice", "badge-voice"),
        "opp":   ("🎯 Opportunity Finder","agent-opp",   "badge-opp"),
        "exec":  ("📋 Executive Summary", "agent-exec",  "badge-exec"),
    }
    for key, content in st.session_state.results.items():
        if key in label_map:
            label, card_cls, badge_cls = label_map[key]
            st.markdown(f"""
            <div class="agent-card {card_cls}">
              <div class="agent-title">
                {label}
                <span class="agent-badge {badge_cls}">COMPLETE</span>
              </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(content)
            st.markdown("<hr>", unsafe_allow_html=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M")
    report_md = f"# MarketMind AI Report\n**Idea:** {st.session_state.last_idea}\n\n"
    for key, content in st.session_state.results.items():
        if key in label_map:
            label = label_map[key][0]
            report_md += f"\n---\n\n## {label}\n\n{content}\n"
    st.download_button("⬇️ Download Report", data=report_md,
                       file_name=f"marketmind_{ts}.md", mime="text/markdown",
                       use_container_width=True)


# ── Empty State ───────────────────────────────────────────────────────────────
else:
    st.markdown("""
    <div class="empty-state">
      <div class="empty-icon">🧠</div>
      <div class="empty-title">Your Research Awaits</div>
      <div class="empty-sub">
        Describe your idea in the sidebar and click <strong>Run Research</strong>.
        Five autonomous agents will analyze trends, competitors, customer voice,
        opportunities, and generate an executive summary — in minutes.
      </div>
    </div>

    <div style="display:grid; grid-template-columns:1fr 1fr; gap:1rem; max-width:700px; margin:2rem auto 0;">
      <div class="agent-card agent-trend" style="padding:1.2rem;">
        <div class="agent-title" style="font-size:0.85rem;">📈 Trend Researcher</div>
        <div style="font-size:0.8rem; color:#64748b;">Scans news, Reddit, social signals for emerging patterns</div>
      </div>
      <div class="agent-card agent-comp" style="padding:1.2rem;">
        <div class="agent-title" style="font-size:0.85rem;">🏢 Competitor Analyst</div>
        <div style="font-size:0.8rem; color:#64748b;">Maps the competitive landscape, features, pricing, positioning</div>
      </div>
      <div class="agent-card agent-voice" style="padding:1.2rem;">
        <div class="agent-title" style="font-size:0.85rem;">💬 Customer Voice</div>
        <div style="font-size:0.8rem; color:#64748b;">Mines user complaints, language, and unmet needs</div>
      </div>
      <div class="agent-card agent-opp" style="padding:1.2rem;">
        <div class="agent-title" style="font-size:0.85rem;">🎯 Opportunity Finder</div>
        <div style="font-size:0.8rem; color:#64748b;">Cross-references all agents to surface market white spaces</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
