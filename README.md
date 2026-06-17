# 🎯 AI Resume Analyzer & Job Match System

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-red?logo=streamlit)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/LangChain-LCEL-yellow)](https://langchain.com)
[![Groq](https://img.shields.io/badge/Groq-Free%20LLM-green)](https://console.groq.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)

> AI-powered resume analyzer and job matching system — built with LangChain, Groq (free LLM), and Streamlit.  
> **100% free to run and deploy.**

## 🌐 Live Demo
👉 **[https://your-app-name.streamlit.app](https://your-app-name.streamlit.app)**  
_(replace with your Streamlit Cloud URL after deployment)_

---

## 📸 Screenshots

| Input | ATS Score | Skills Gap | Recommendations |
|---|---|---|---|
| _(add screenshot)_ | _(add screenshot)_ | _(add screenshot)_ | _(add screenshot)_ |

---

## ✨ Features

- 📄 Upload resume as **PDF, DOCX, or TXT**
- 🤖 **LangChain LCEL chains** extract structured data from resume and job description
- 📊 **ATS Score** — keyword, skills & experience matching algorithm
- 🎯 **5-dimension Match Score** — skills · keywords · experience · education · languages
- ❌ **Skills Gap Analysis** — matched vs missing with coloured badges
- 💡 **AI Recommendations** — immediate actions, learning roadmap, resume tips
- 📈 **Interactive charts** — gauge, radar, bar (Plotly)
- 💾 **Export** full analysis as JSON

---

## 🚀 Quick Start (Local)

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/ai-resume-analyzer.git
cd ai-resume-analyzer

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up your free Groq API key
cp .env.example .env
# Edit .env → add your key from https://console.groq.com

# 5. Run
streamlit run app.py
```

**Full deployment guide → [DEPLOY_GUIDE.md](DEPLOY_GUIDE.md)**

---

## 📁 Project Structure

```
ai-resume-analyzer/
├── app.py                    # Main Streamlit UI (748 lines)
├── utils/
│   ├── resume_parser.py      # PDF/DOCX/TXT extraction
│   └── analyzer.py           # LangChain + Groq/OpenAI engine
├── prompts/
│   └── templates.py          # All GPT prompt templates
├── .streamlit/config.toml    # Theme config
├── requirements.txt
├── .env.example
├── DEPLOY_GUIDE.md           # Step-by-step deployment guide
└── README.md
```

---

## 🧠 How It Works

```
Resume (PDF/DOCX)              Job Description (text)
       │                               │
       ▼                               ▼
  Text Extraction              LangChain Chain
  (PyPDF2 / docx)              (Groq LLaMA 3 70B)
       │                               │
       └──────────┬────────────────────┘
                  ▼
     ┌─────────────────────────┐
     │  ATS Scoring Algorithm  │  ← keyword matching
     │  Match Score Engine     │  ← 5-dimension weighted
     └────────────┬────────────┘
                  ▼
     LangChain Recommendations Chain
     (Groq LLaMA 3 70B + Prompt Engineering)
                  │
                  ▼
     Streamlit Dashboard
     (Gauge · Radar · Bar Charts · Badges)
```

---

## 🛠 Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| UI | Streamlit | Web interface |
| LLM Orchestration | LangChain LCEL | Chain management |
| Free LLM | Groq (LLaMA 3 70B) | AI analysis & recommendations |
| Paid LLM (optional) | OpenAI GPT-4 | Alternative provider |
| Document Parsing | PyPDF2, python-docx | Resume extraction |
| Visualisation | Plotly | Charts & gauges |
| Data | Pandas | Score tables |
| Deployment | Streamlit Community Cloud | Free hosting |
| Code Hosting | GitHub | Version control |

---

## 📝 CV Description (Ready to Copy)

> **AI Resume Analyzer & Job Matching System**
> - Built AI-powered web app analyzing resumes against job descriptions using NLP and LangChain LCEL chains with Groq LLaMA 3 (70B)
> - Implemented ATS compatibility scoring via keyword matching, skill gap analysis, and 5-dimension weighted match algorithm
> - Engineered prompt templates for structured extraction of resume fields, job requirements, and personalized career recommendations
> - Deployed on Streamlit Community Cloud with interactive Plotly dashboards (gauge, radar, bar charts)
>
> **Stack:** Python · LangChain · Groq API · OpenAI API · Streamlit · Plotly · Pandas · PyPDF2

---

## 📜 License
MIT — free to use, modify, and distribute.
