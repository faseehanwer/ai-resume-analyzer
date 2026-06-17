"""
AI Resume Analyzer & Job Match System
======================================
Free stack: Groq API (free) + Streamlit Cloud (free) + GitHub (free)
"""

import os, json, re
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from dotenv import load_dotenv

from utils.resume_parser import parse_resume
from utils.analyzer import ResumeAnalyzer, GROQ_MODELS, OPENAI_MODELS, _score_color, _score_label

load_dotenv()

# ── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  .block-container{padding-top:1.4rem}
  .main-header{
    background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);
    padding:2rem 2.5rem;border-radius:14px;color:#fff;text-align:center;
    margin-bottom:1.6rem;box-shadow:0 8px 32px rgba(102,126,234,.25)
  }
  .main-header h1{margin:0;font-size:1.9rem;font-weight:700}
  .main-header p{margin:.4rem 0 0;font-size:1rem;opacity:.9}
  .badge-green {background:#dcfce7;color:#166534;padding:.25rem .7rem;border-radius:20px;font-size:.82rem;font-weight:600;display:inline-block;margin:.2rem}
  .badge-red   {background:#fee2e2;color:#991b1b;padding:.25rem .7rem;border-radius:20px;font-size:.82rem;font-weight:600;display:inline-block;margin:.2rem}
  .badge-blue  {background:#dbeafe;color:#1e40af;padding:.25rem .7rem;border-radius:20px;font-size:.82rem;font-weight:600;display:inline-block;margin:.2rem}
  .badge-amber {background:#fef3c7;color:#92400e;padding:.25rem .7rem;border-radius:20px;font-size:.82rem;font-weight:600;display:inline-block;margin:.2rem}
  .badge-purple{background:#ede9fe;color:#5b21b6;padding:.25rem .7rem;border-radius:20px;font-size:.82rem;font-weight:600;display:inline-block;margin:.2rem}
  .action-card{background:#f0fdf4;border:1px solid #86efac;border-radius:10px;padding:1rem 1.2rem;margin:.5rem 0}
  .rec-card   {background:#f0f9ff;border:1px solid #bae6fd;border-radius:10px;padding:1rem 1.2rem;margin:.5rem 0}
  .tip-card   {background:#faf5ff;border:1px solid #d8b4fe;border-radius:10px;padding:1rem 1.2rem;margin:.5rem 0}
  .advice-box {background:linear-gradient(135deg,#f0f9ff,#faf5ff);border:1px solid #c7d2fe;
               border-radius:12px;padding:1.2rem 1.5rem;margin:1rem 0;font-size:1.02rem;line-height:1.7}
  div[data-testid="metric-container"]{background:#fff;border:1px solid #e5e7eb;
    border-radius:12px;padding:1rem;box-shadow:0 2px 8px rgba(0,0,0,.04)}
  .free-badge{background:#dcfce7;color:#15803d;padding:.15rem .5rem;border-radius:6px;font-size:.75rem;font-weight:700}
</style>
""", unsafe_allow_html=True)

# ── Sample data ──────────────────────────────────────────────────────────────
SAMPLE_RESUME = """
John Smith | Python Developer & AI Engineer
john.smith@email.com | +1-555-0193 | San Francisco, CA | github.com/johnsmith

PROFESSIONAL SUMMARY
Results-driven Python Developer with 4 years of experience building scalable REST APIs,
data pipelines, and ML models. Expert in NLP, LLM integration, and LangChain workflows.
Reduced model inference latency by 35% and cut manual data-processing effort by 60%.

TECHNICAL SKILLS
Languages: Python, JavaScript, SQL, Bash
Frameworks: FastAPI, Django, Flask, Scikit-learn, Pandas, NumPy
AI/ML: TensorFlow, PyTorch, OpenAI API, LangChain, Hugging Face Transformers
Tools: Git, Docker, AWS (EC2, S3, Lambda), PostgreSQL, Redis, Streamlit

EXPERIENCE
Senior Python Developer — TechCorp Inc | 2022–2024
• Built REST APIs with FastAPI handling 500 K+ requests/day
• Created NLP pipeline (Hugging Face) to classify support tickets with 91% accuracy
• Integrated GPT-4 API for automated report generation, saving 70% writing time
• Led migration from Django monolith to AWS microservices

Python Developer — DataStack LLC | 2020–2022
• Built ETL pipelines with Pandas/PySpark for a 10 TB data warehouse
• Delivered Streamlit dashboards for real-time KPI monitoring

EDUCATION
B.Sc. Computer Science — State University, 2020 (GPA 3.8/4.0)

CERTIFICATIONS
AWS Certified Developer – Associate (2023) | TensorFlow Developer Certificate (2022)

PROJECTS
ResumeBot — LangChain + OpenAI resume-screening chatbot (GitHub ⭐ 420)
SentimentStream — Real-time Twitter sentiment with Kafka + BERT
"""

SAMPLE_JD = """
AI/ML Engineer — TechStartup Inc (San Francisco / Remote)

REQUIRED
• 3+ years Python development experience
• Machine learning frameworks: TensorFlow or PyTorch
• LLMs, prompt engineering, LangChain workflows
• OpenAI API and vector databases (Pinecone / Weaviate)
• REST API development with FastAPI or Flask
• Docker and cloud platforms (AWS or GCP)
• Pandas, NumPy, data manipulation

PREFERRED
• Retrieval-Augmented Generation (RAG) pipelines
• MLflow or experiment tracking tools
• Open-source AI/ML contributions
• B.Sc. / M.Sc. Computer Science or related

KEY RESPONSIBILITIES
• Design, train and deploy ML models for production
• Integrate LLM APIs into customer-facing products
• Build and maintain LangChain agents
• Optimise model performance and reduce inference latency

KEYWORDS: Python, Machine Learning, LangChain, OpenAI, LLM, NLP, FastAPI,
Docker, AWS, TensorFlow, PyTorch, Pandas, Git, REST API, Prompt Engineering,
Streamlit, Transformer, RAG, Vector Database, Deep Learning
"""

# ── Visualisations ────────────────────────────────────────────────────────────
def make_gauge(value, title):
    color = _score_color(value)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number={"suffix": "%", "font": {"size": 38, "color": color}},
        title={"text": title, "font": {"size": 15}},
        gauge={
            "axis": {"range": [0, 100], "tickfont": {"size": 11}},
            "bar": {"color": color, "thickness": 0.28},
            "bgcolor": "white",
            "steps": [
                {"range": [0,  40], "color": "#fee2e2"},
                {"range": [40, 60], "color": "#fef3c7"},
                {"range": [60, 80], "color": "#dbeafe"},
                {"range": [80,100], "color": "#dcfce7"},
            ],
            "threshold": {"line": {"color": "#64748b", "width": 3}, "thickness": .75, "value": 70},
        },
    ))
    fig.update_layout(height=240, margin=dict(t=40,b=20,l=20,r=20),
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    return fig


def make_radar(match):
    cats = ["Skills","Experience","Keywords","Education","Languages"]
    vals = [match.get("skills_alignment",0), match.get("experience_alignment",0),
            match.get("keyword_alignment",0), match.get("education_alignment",0),
            match.get("language_alignment",0)]
    fig = go.Figure(go.Scatterpolar(
        r=vals+[vals[0]], theta=cats+[cats[0]], fill="toself",
        fillcolor="rgba(102,126,234,.15)", line=dict(color="#667eea",width=2),
        marker=dict(color="#667eea", size=7),
    ))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True,range=[0,100]),
                                  angularaxis=dict(tickfont={"size":12})),
                      height=320, margin=dict(t=30,b=30,l=30,r=30),
                      paper_bgcolor="rgba(0,0,0,0)")
    return fig


def make_skills_bar(matched, missing):
    items  = matched + missing
    colors = ["#10b981"]*len(matched) + ["#ef4444"]*len(missing)
    labels = ["✅ Matched"]*len(matched) + ["❌ Missing"]*len(missing)
    fig = go.Figure(go.Bar(y=items, x=[100]*len(items), orientation="h",
                           marker_color=colors, text=labels, textposition="inside",
                           hovertemplate="%{y}: %{text}<extra></extra>"))
    fig.update_layout(height=max(280,len(items)*30), margin=dict(t=10,b=10,l=10,r=10),
                      xaxis=dict(visible=False), paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)", showlegend=False)
    return fig


def badge(text, kind="blue"):
    return f'<span class="badge-{kind}">{text}</span>'


def priority_icon(p):
    p = (p or "").lower()
    if "high"   in p: return "🔴"
    if "medium" in p: return "🟡"
    return "🟢"


# ── Session state ─────────────────────────────────────────────────────────────
for k,v in {"analysis_done":False,"results":None,"resume_text":"","job_text":""}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Configuration")

    # Provider selector
    provider_choice = st.radio(
        "AI Provider",
        ["🆓 Groq — Free", "💰 OpenAI"],
        index=0,
        help="Groq is 100% free. OpenAI requires a paid key.",
    )
    provider = "groq" if "Groq" in provider_choice else "openai"

    if provider == "groq":
        st.markdown('<span class="free-badge">FREE</span> No credit card needed', unsafe_allow_html=True)
        api_key = st.text_input(
            "🔑 Groq API Key",
            type="password",
            placeholder="gsk_...",
            value=os.getenv("GROQ_API_KEY", ""),
            help="Get your free key at console.groq.com",
        )
        st.caption("👉 [Get free Groq key →](https://console.groq.com)")
        model = st.selectbox("Model", GROQ_MODELS, index=0)
    else:
        api_key = st.text_input(
            "🔑 OpenAI API Key",
            type="password",
            placeholder="sk-...",
            value=os.getenv("OPENAI_API_KEY", ""),
        )
        st.caption("👉 [Get OpenAI key →](https://platform.openai.com/api-keys)")
        model = st.selectbox("Model", OPENAI_MODELS, index=0)

    st.divider()
    st.markdown("### 📊 Modules (all active)")
    for m in ["ATS Scoring","Skills Gap Analysis","Keyword Matching","AI Recommendations"]:
        st.markdown(f"✅ {m}")

    st.divider()
    st.markdown("""
**🔗 Free Hosting:**
[Streamlit Community Cloud](https://streamlit.io/cloud)

**🛠 Stack:** Python · LangChain · Groq/OpenAI · Streamlit · Plotly
""")
    if st.session_state.analysis_done and st.session_state.results:
        st.divider()
        st.download_button(
            "💾 Download Results JSON",
            data=json.dumps(st.session_state.results, indent=2),
            file_name="resume_analysis.json",
            mime="application/json",
        )

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
  <h1>🎯 AI Resume Analyzer & Job Match System</h1>
  <p>Powered by LangChain · Groq (Free) · OpenAI · Streamlit</p>
</div>
""", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📄  Input", "📊  Analysis Results", "💡  Recommendations"])


# ═══════════════════════════════════════════════════════════
# TAB 1 — INPUT
# ═══════════════════════════════════════════════════════════
with tab1:
    c1, c2 = st.columns(2, gap="large")

    with c1:
        st.markdown("### 📄 Upload Your Resume")
        uploaded = st.file_uploader("PDF · DOCX · TXT", type=["pdf","docx","txt"])
        if uploaded:
            try:
                d = parse_resume(uploaded)
                st.session_state.resume_text = d["raw_text"]
                st.success(f"✅ **{uploaded.name}** — {d['word_count']:,} words ({d['file_type']})")
                with st.expander("👁 Preview"):
                    txt = st.session_state.resume_text
                    st.text_area("", txt[:3000]+("\n…" if len(txt)>3000 else ""), height=260)
            except Exception as e:
                st.error(f"❌ {e}")

        if st.button("📋 Load Sample Resume", use_container_width=True):
            st.session_state.resume_text = SAMPLE_RESUME
            st.success("✅ Sample resume loaded!")

    with c2:
        st.markdown("### 💼 Job Description")
        jd = st.text_area("Paste full job posting here", height=320,
                           placeholder="Paste job description…",
                           value=st.session_state.job_text)
        if jd:
            st.session_state.job_text = jd
        if st.button("📋 Load Sample Job Description", use_container_width=True):
            st.session_state.job_text = SAMPLE_JD
            st.rerun()

    st.markdown("---")
    _, bc, _ = st.columns([1,2,1])
    with bc:
        go_btn = st.button("🚀  Analyze Resume & Match Job", type="primary", use_container_width=True)

    if go_btn:
        errs = []
        if not api_key:
            pname = "Groq" if provider == "groq" else "OpenAI"
            errs.append(f"Enter your **{pname} API key** in the sidebar.")
        if not st.session_state.resume_text.strip():
            errs.append("Upload a resume or click *Load Sample Resume*.")
        if not st.session_state.job_text.strip():
            errs.append("Paste a job description or click *Load Sample Job Description*.")

        if errs:
            for e in errs: st.error(f"❌ {e}")
        else:
            pb = st.progress(0)
            st_txt = st.empty()
            try:
                analyzer = ResumeAnalyzer(api_key=api_key, model=model, provider=provider)
                for pct, msg in [(20,"🔍 Parsing resume…"),(45,"📋 Parsing job description…"),
                                  (65,"🎯 Scoring ATS & match…"),(85,"🤖 Generating recommendations…")]:
                    st_txt.info(msg); pb.progress(pct)

                results = analyzer.full_analysis(
                    resume_text=st.session_state.resume_text,
                    job_description=st.session_state.job_text,
                )
                pb.progress(100); st_txt.success("✅ Analysis complete!")
                st.session_state.results = results
                st.session_state.analysis_done = True
                st.balloons()
                st.info("👉 Open the **📊 Analysis Results** tab to see your report.")
            except Exception as e:
                pb.empty(); st_txt.empty()
                msg = str(e)
                if "api_key" in msg.lower() or "authentication" in msg.lower() or "401" in msg:
                    pname = "Groq (console.groq.com)" if provider=="groq" else "OpenAI (platform.openai.com)"
                    st.error(f"❌ Invalid API key. Check your {pname} key in the sidebar.")
                elif "rate" in msg.lower():
                    st.error("❌ Rate limit hit — wait 60 s and try again (free tier limit).")
                elif "connection" in msg.lower():
                    st.error("❌ Connection error — check your internet and try again.")
                else:
                    st.error(f"❌ {msg}")


# ═══════════════════════════════════════════════════════════
# TAB 2 — ANALYSIS RESULTS
# ═══════════════════════════════════════════════════════════
with tab2:
    if not st.session_state.analysis_done or not st.session_state.results:
        st.info("📌 Complete the analysis in the **📄 Input** tab first.")
        st.stop()

    R     = st.session_state.results
    ats   = R["ats_analysis"]
    match = R["match_score"]
    info  = R["resume_info"]
    job   = R["job_requirements"]

    st.markdown(f"### 👤 {info.get('name','Candidate')} → 🏢 {job.get('job_title','Role')} @ {job.get('company','Company')}")

    # KPIs
    k1,k2,k3,k4,k5 = st.columns(5)
    k1.metric("🎯 Overall Match",  f"{match['overall_match']:.0f}%")
    k2.metric("📋 ATS Score",      f"{ats['ats_score']:.0f}%")
    k3.metric("🔧 Skills Match",   f"{ats['skills_score']:.0f}%")
    k4.metric("🔑 Keyword Match",  f"{ats['keyword_score']:.0f}%")
    k5.metric("⏱ Experience",      f"{ats['experience_score']:.0f}%")

    st.markdown("---")

    # Gauge + Radar
    gc, rc = st.columns(2, gap="large")
    with gc:
        st.markdown("#### ATS Compatibility")
        st.plotly_chart(make_gauge(ats["ats_score"], "ATS Score"), use_container_width=True)
        lbl = _score_label(ats["ats_score"]); col = _score_color(ats["ats_score"])
        st.markdown(f"<p style='text-align:center;font-weight:700;color:{col};font-size:1.1rem;'>Rating: {lbl}</p>",
                    unsafe_allow_html=True)
        if ats["ats_score"] < 70:
            st.warning("💡 Score below 70 — most ATS systems may filter this resume out.")
        else:
            st.success("🎉 Strong ATS score — well optimised for this role!")

    with rc:
        st.markdown("#### Score Breakdown (Radar)")
        st.plotly_chart(make_radar(match), use_container_width=True)

    st.markdown("---")

    # Skills
    st.markdown("#### 🔧 Skills Analysis")
    sc1, sc2 = st.columns(2)
    with sc1:
        st.markdown(f"**✅ Matched Required Skills ({len(ats['matched_skills'])})**")
        if ats["matched_skills"]:
            st.markdown(" ".join(badge(s,"green") for s in ats["matched_skills"]), unsafe_allow_html=True)
        else:
            st.caption("None found.")
        if ats.get("matched_preferred"):
            st.markdown(f"**⭐ Preferred Skills Present ({len(ats['matched_preferred'])})**")
            st.markdown(" ".join(badge(s,"purple") for s in ats["matched_preferred"]), unsafe_allow_html=True)
    with sc2:
        st.markdown(f"**❌ Missing Required Skills ({len(ats['missing_skills'])})**")
        if ats["missing_skills"]:
            st.markdown(" ".join(badge(s,"red") for s in ats["missing_skills"]), unsafe_allow_html=True)
        else:
            st.success("🎉 All required skills present!")
        if ats.get("missing_languages"):
            st.markdown(f"**⚠️ Missing Languages ({len(ats['missing_languages'])})**")
            st.markdown(" ".join(badge(s,"amber") for s in ats["missing_languages"]), unsafe_allow_html=True)

    if ats["matched_skills"] or ats["missing_skills"]:
        with st.expander("📊 Skills Bar Chart"):
            st.plotly_chart(make_skills_bar(ats["matched_skills"],ats["missing_skills"]),
                            use_container_width=True)

    st.markdown("---")

    # Keywords
    st.markdown("#### 🔑 Keyword Analysis")
    kc1, kc2 = st.columns(2)
    with kc1:
        st.markdown(f"**✅ Matched ({len(ats['matched_keywords'])})**")
        if ats["matched_keywords"]:
            st.markdown(" ".join(badge(k,"green") for k in ats["matched_keywords"]), unsafe_allow_html=True)
    with kc2:
        st.markdown(f"**❌ Missing ({len(ats['missing_keywords'])})**")
        if ats["missing_keywords"]:
            st.markdown(" ".join(badge(k,"red") for k in ats["missing_keywords"]), unsafe_allow_html=True)
        else:
            st.success("All keywords matched!")

    st.markdown("---")

    # Score table
    st.markdown("#### 📈 Score Breakdown Table")
    df = pd.DataFrame([
        {"Category":"Skills Alignment",    "Score (%)": match["skills_alignment"],    "Weight":"30%"},
        {"Category":"Keyword Density",      "Score (%)": match["keyword_alignment"],   "Weight":"25%"},
        {"Category":"Experience Match",     "Score (%)": match["experience_alignment"],"Weight":"20%"},
        {"Category":"Language/Tech Overlap","Score (%)": match["language_alignment"],  "Weight":"15%"},
        {"Category":"Education Match",      "Score (%)": match["education_alignment"], "Weight":"10%"},
    ])
    df["Score (%)"] = df["Score (%)"].round(1)
    df["Rating"] = df["Score (%)"].apply(_score_label)
    st.dataframe(df, use_container_width=True, hide_index=True)

    with st.expander("📄 Extracted Resume Data (JSON)"):  st.json(info)
    with st.expander("💼 Extracted Job Requirements (JSON)"): st.json(job)


# ═══════════════════════════════════════════════════════════
# TAB 3 — RECOMMENDATIONS
# ═══════════════════════════════════════════════════════════
with tab3:
    if not st.session_state.analysis_done or not st.session_state.results:
        st.info("📌 Complete the analysis in the **📄 Input** tab first.")
        st.stop()

    R     = st.session_state.results
    recs  = R.get("recommendations", {})
    ats   = R["ats_analysis"]
    match = R["match_score"]

    if not recs:
        st.warning("⚠️ Recommendations could not be generated. Check your API key and retry.")
        st.stop()

    # Overall advice
    st.markdown("### 🧠 AI Career Coach Assessment")
    if recs.get("overall_advice"):
        st.markdown(f'<div class="advice-box">💬 <strong>Overall:</strong><br><br>{recs["overall_advice"]}</div>',
                    unsafe_allow_html=True)
    st.markdown("---")

    # Immediate actions
    st.markdown("### ⚡ Immediate Action Plan")
    for i, a in enumerate(recs.get("immediate_actions",[]), 1):
        if isinstance(a, dict):
            st.markdown(
                f'<div class="action-card"><strong>Action {i}:</strong> {a.get("action","")}<br>'
                f'<strong>⚡ Impact:</strong> {a.get("impact","")}&nbsp;|&nbsp;'
                f'<strong>⏰ Timeline:</strong> {a.get("timeline","")}</div>',
                unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="action-card">✅ {a}</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Skills roadmap
    st.markdown("### 📚 Skill Development Roadmap")
    plan = recs.get("skill_development", [])
    if plan:
        cols = st.columns(min(len(plan),3))
        for i, item in enumerate(plan):
            if isinstance(item, dict):
                p = item.get("priority","Medium")
                with cols[i % 3]:
                    st.markdown(
                        f'<div class="rec-card"><strong>{priority_icon(p)} {item.get("skill","")}</strong><br>'
                        f'📖 {item.get("resource","")}<br>'
                        f'⏱ {item.get("time_to_learn","")} | Priority: <strong>{p}</strong></div>',
                        unsafe_allow_html=True)

    st.markdown("---")

    # Resume tips + keywords
    rc1, rc2 = st.columns(2, gap="large")
    with rc1:
        st.markdown("### 📝 Resume Improvement Tips")
        for tip in recs.get("resume_improvements",[]):
            st.markdown(f'<div class="tip-card">✏️ {tip}</div>', unsafe_allow_html=True)
    with rc2:
        st.markdown("### 🔑 Keywords to Add")
        kws = recs.get("keywords_to_add", []) or ats.get("missing_keywords",[])[:12]
        if kws:
            st.markdown(" ".join(badge(k,"blue") for k in kws), unsafe_allow_html=True)
            st.caption("Add these naturally in your bullet points and skills section.")

    st.markdown("---")

    # Interview tips
    st.markdown("### 🎤 Interview Preparation")
    for tip in recs.get("interview_tips",[]):
        st.markdown(f'<div class="tip-card">🎯 {tip}</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Summary bar
    st.markdown("### 📊 Quick Summary")
    s1,s2,s3 = st.columns(3)
    for col, val, label, border in [
        (s1, f"{match['overall_match']:.0f}%", "Overall Match",    _score_color(match["overall_match"])),
        (s2, len(ats.get("missing_skills",[])), "Skills to Acquire","#f59e0b"),
        (s3, len(recs.get("immediate_actions",[])), "Action Items","#667eea"),
    ]:
        col.markdown(
            f"<div style='text-align:center;padding:1rem;background:#fff;border-radius:12px;"
            f"border:2px solid {border};'>"
            f"<p style='font-size:2rem;margin:0;font-weight:700;color:{border};'>{val}</p>"
            f"<p style='font-weight:600;margin:0;color:#374151;'>{label}</p></div>",
            unsafe_allow_html=True)
