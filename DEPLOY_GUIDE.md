# 🚀 Complete Deployment Guide — Zero to Live
## AI Resume Analyzer (100% Free Stack)

> **Total time:** ~30 minutes  
> **Cost:** $0.00 — GitHub (free) + Groq API (free) + Streamlit Cloud (free)

---

## ✅ What You'll Have at the End

- 🌐 A **live public URL** like `https://your-name-resume-ai.streamlit.app`
- 📂 A **GitHub repository** showing professional code
- 📸 **Screenshots** for your CV and portfolio
- 📋 **CV bullet points** ready to copy

---

## 📋 CHECKLIST — Open This While You Work

```
[ ] Step 1 — Get free Groq API key
[ ] Step 2 — Install Python and Git
[ ] Step 3 — Download and run project locally
[ ] Step 4 — Take screenshots
[ ] Step 5 — Create GitHub account and repo
[ ] Step 6 — Push code to GitHub
[ ] Step 7 — Deploy on Streamlit Cloud
[ ] Step 8 — Get live URL and add to CV
```

---

## STEP 1 — Get Your FREE Groq API Key (5 minutes)

Groq gives you a **completely free** API key to use powerful LLMs.

1. Go to 👉 **https://console.groq.com**
2. Click **"Sign Up"** — use Google or GitHub to sign in (fastest)
3. After login, click **"API Keys"** in the left sidebar
4. Click **"Create API Key"**
5. Name it `resume-analyzer`
6. **Copy the key** — it looks like `gsk_xxxxxxxxxxxxxxxxxxxx`
7. Save it somewhere safe (you only see it once!)

> ✅ This key is FREE — no credit card, no limits for personal projects

---

## STEP 2 — Install Python & Git on Your Computer

### Check if already installed (open Terminal / Command Prompt):
```bash
python --version    # Need 3.10 or higher
git --version       # Need any version
```

### If NOT installed:

**Python** → https://www.python.org/downloads/
- Windows: Download the `.exe`, tick ✅ **"Add Python to PATH"** during install
- Mac: `brew install python` or download from website
- Linux: `sudo apt install python3 python3-pip`

**Git** → https://git-scm.com/downloads
- Windows: Download installer, use all default options
- Mac: `brew install git`
- Linux: `sudo apt install git`

---

## STEP 3 — Set Up the Project Locally

### Windows (Command Prompt or PowerShell)

```bat
# 1. Download project (if you have the zip — extract it first)
#    OR clone from GitHub after Step 5-6

# 2. Go into the project folder
cd ai-resume-analyzer

# 3. Create a virtual environment
python -m venv venv

# 4. Activate it
venv\Scripts\activate
# You should see (venv) at the start of your prompt

# 5. Install all packages
pip install -r requirements.txt

# 6. Create your .env file
copy .env.example .env
```

Now open `.env` in Notepad and paste your Groq key:
```
GROQ_API_KEY=gsk_your_actual_key_here
```

### Mac / Linux (Terminal)

```bash
cd ai-resume-analyzer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nano .env   # or: open .env with any text editor
```

Paste your key:
```
GROQ_API_KEY=gsk_your_actual_key_here
```

### Run the app locally

```bash
streamlit run app.py
```

Your browser opens automatically at **http://localhost:8501** 🎉

---

## STEP 4 — Test the App & Take Screenshots

### Test it works:
1. In the sidebar → provider is **"🆓 Groq — Free"** ✅
2. Your Groq API key is pre-filled from `.env`
3. Click **"📋 Load Sample Resume"**
4. Click **"📋 Load Sample Job Description"**
5. Click **"🚀 Analyze Resume & Match Job"**
6. Wait ~15 seconds
7. Switch to **"📊 Analysis Results"** tab

### Take 4 screenshots for portfolio:

| Screenshot | What to Capture |
|---|---|
| `01_input.png` | Input tab with resume loaded |
| `02_scores.png` | Analysis tab — top KPI scores + gauge |
| `03_skills.png` | Skills analysis (green + red badges) |
| `04_recommendations.png` | Recommendations tab |

**Windows:** Press `Windows + Shift + S`, drag to select  
**Mac:** Press `Cmd + Shift + 4`, drag to select  

Save all 4 images to a `screenshots/` folder inside your project.

---

## STEP 5 — Create GitHub Account & Repository

1. Go to 👉 **https://github.com**
2. Click **"Sign up"** (free)
3. After login, click **"+"** top-right → **"New repository"**
4. Fill in:
   - **Repository name:** `ai-resume-analyzer`
   - **Description:** `AI-powered resume analyzer & job match system using LangChain, Groq LLM, and Streamlit`
   - Set to **Public** ← important for portfolio
   - **Do NOT** tick "Initialize this repository" (we'll push code ourselves)
5. Click **"Create repository"**
6. **Copy the repo URL** shown on screen — looks like:
   `https://github.com/YOUR_USERNAME/ai-resume-analyzer.git`

---

## STEP 6 — Push Your Code to GitHub

In your terminal (inside the `ai-resume-analyzer` folder):

```bash
# 1. Set up your name and email in git (first-time only)
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# 2. Initialize git in the project folder
git init

# 3. Add all files (the .gitignore will automatically skip .env and venv/)
git add .

# 4. Make first commit
git commit -m "Initial commit: AI Resume Analyzer with LangChain + Groq"

# 5. Connect to your GitHub repo (paste YOUR repo URL here)
git remote add origin https://github.com/YOUR_USERNAME/ai-resume-analyzer.git

# 6. Push to GitHub
git branch -M main
git push -u origin main
```

**First-time GitHub push may ask for credentials:**
- Username: your GitHub username
- Password: use a **Personal Access Token** (NOT your GitHub password)
  - Go to GitHub → Settings → Developer Settings → Personal Access Tokens → Tokens (classic)
  - Click "Generate new token (classic)" → tick "repo" → Generate → copy it
  - Paste this as your password

✅ **Verify:** Go to `https://github.com/YOUR_USERNAME/ai-resume-analyzer`
You should see all your files listed there!

---

## STEP 7 — Deploy to Streamlit Community Cloud (Free)

1. Go to 👉 **https://streamlit.io/cloud**
2. Click **"Sign in"** → use **"Continue with GitHub"** ← same account you just used
3. Click **"New app"** (top right)
4. Fill in the form:

   | Field | Value |
   |---|---|
   | **Repository** | `YOUR_USERNAME/ai-resume-analyzer` |
   | **Branch** | `main` |
   | **Main file path** | `app.py` |
   | **App URL** | choose a name e.g. `resume-ai-yourname` |

5. Click **"Advanced settings"**
6. In the **Secrets** box, paste:
   ```toml
   GROQ_API_KEY = "gsk_your_actual_groq_key_here"
   ```
   ⚠️ Use the **exact format** above with quotes
7. Click **"Save"**
8. Click **"Deploy!"**

### ⏳ Deployment takes 3–5 minutes

Watch the logs — you'll see packages being installed. When you see:
```
You can now view your Streamlit app in your browser.
```
Your app is LIVE! 🎉

Your URL is something like:
```
https://resume-ai-yourname.streamlit.app
```

**Test it:** Open the URL in a private/incognito window. 
No API key needed — it uses the secret you added!

---

## STEP 8 — Add to CV & Portfolio

### Your CV — Project Section

```
AI Resume Analyzer & Job Matching System                     [GitHub] [Live Demo]
• Built an AI-powered web app that analyzes resumes against job descriptions
  using NLP and LLM models, generating ATS scores and skill-gap reports
• Implemented LangChain LCEL chains with Groq LLaMA 3 (70B) for structured
  resume extraction, job parsing, and personalized career recommendations
• Engineered ATS scoring algorithm with keyword matching, skills alignment,
  and experience gap detection across 5 weighted dimensions
• Deployed on Streamlit Community Cloud; live at https://yourapp.streamlit.app

Stack: Python · LangChain · Groq API · OpenAI API · Streamlit · Plotly · Pandas
```

### Your LinkedIn — Projects Section

1. Go to LinkedIn → Profile → **"Add section"** → **"Projects"**
2. Fill in:
   - **Name:** AI Resume Analyzer & Job Match System
   - **Description:** (paste the CV text above)
   - **URL:** Your Streamlit app URL

### Update Your GitHub README

Add this badge to your README.md:
```markdown
[![Live Demo](https://img.shields.io/badge/Live-Demo-green?logo=streamlit)](https://yourapp.streamlit.app)
```

---

## 🔧 Troubleshooting

### ❌ "Invalid API key" error
- Make sure you copied the key correctly (starts with `gsk_` for Groq)
- In Streamlit Cloud → App settings → Secrets — check format has quotes

### ❌ "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### ❌ "streamlit: command not found"
```bash
# Make sure venv is activated
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### ❌ Push rejected on GitHub
```bash
git pull origin main --rebase
git push origin main
```

### ❌ App shows blank / crashes on Streamlit Cloud
- Check the **Logs** tab in Streamlit Cloud dashboard
- Most common: missing secret key or typo in `secrets.toml`
- Secret format MUST be: `GROQ_API_KEY = "gsk_..."` (with quotes)

### ❌ Groq rate limit error
- Free tier: 30 req/min — wait 60 seconds and retry
- Or switch model from `llama3-70b-8192` to `llama3-8b-8192` (faster)

---

## 💡 Pro Tips for Portfolio

1. **Pin the repo** on GitHub profile (Settings → Repositories → pin it)
2. **Add screenshots** to the GitHub README using:
   ```markdown
   ![App Screenshot](screenshots/02_scores.png)
   ```
3. **Record a 60-second demo video** with Loom (free) → add link to LinkedIn
4. **Star your own repo** after making it public — looks professional
5. Use the app URL as a **hyperlink in your PDF CV** (most ATS systems allow it)

---

## 📞 Free Resources Used

| Service | What For | Link |
|---|---|---|
| Groq | Free LLM API (LLaMA 3 70B) | https://console.groq.com |
| GitHub | Free code hosting | https://github.com |
| Streamlit Cloud | Free deployment (3 apps) | https://streamlit.io/cloud |
| Python | Programming language | https://python.org |

**Total monthly cost: $0** ✅
