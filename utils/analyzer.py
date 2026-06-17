"""
AI Resume Analyzer — Core Analysis Engine
Supports:
  • Groq  (FREE — llama3-70b, mixtral)   → https://console.groq.com
  • OpenAI (paid — gpt-3.5/4)            → https://platform.openai.com
Both use LangChain LCEL chains.
"""

import json
import re
from typing import Any

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from prompts.templates import (
    RESUME_EXTRACTION_PROMPT,
    JOB_EXTRACTION_PROMPT,
    RECOMMENDATIONS_PROMPT,
)

 
# ── Free Groq models (updated June 2025) ────────────────────────────────────
# llama3-70b-8192 and mixtral-8x7b-32768 were decommissioned by Groq.
GROQ_MODELS  = [
    "llama-3.3-70b-versatile",          # ← Best: replaces llama3-70b-8192
    "llama-3.1-8b-instant",             # Fastest, lightest
    "gemma2-9b-it",                     # Google Gemma 2
    "meta-llama/llama-4-scout-17b-16e-instruct",   # Llama 4 Scout
]
OPENAI_MODELS = ["gpt-3.5-turbo", "gpt-4o-mini", "gpt-4o", "gpt-4-turbo"]
 
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
 

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _parse_json(text: str) -> dict:
    text = re.sub(r"```(?:json)?\n?", "", text).strip()
    text = re.sub(r"```$", "", text).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{[\s\S]*\}", text)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass
    return {}


def _score_color(score: float) -> str:
    if score >= 80:  return "#10b981"
    if score >= 60:  return "#3b82f6"
    if score >= 40:  return "#f59e0b"
    return "#ef4444"


def _score_label(score: float) -> str:
    if score >= 80:  return "Excellent"
    if score >= 60:  return "Good"
    if score >= 40:  return "Average"
    return "Needs Work"


# ---------------------------------------------------------------------------
# ResumeAnalyzer
# ---------------------------------------------------------------------------
class ResumeAnalyzer:
    """End-to-end resume analysis — Groq (free) or OpenAI."""

    def __init__(self, api_key: str, model: str = None, provider: str = "groq"):
        self.provider = provider

        if provider == "groq":
            chosen_model = model or GROQ_MODELS[0]
            self.llm = ChatOpenAI(
                openai_api_key=api_key,
                openai_api_base=GROQ_BASE_URL,
                model=chosen_model,
                temperature=0.1,
                max_tokens=2000,
            )
        else:  # openai
            chosen_model = model or OPENAI_MODELS[0]
            self.llm = ChatOpenAI(
                openai_api_key=api_key,
                model=chosen_model,
                temperature=0.1,
                max_tokens=2000,
            )

        self._parser = StrOutputParser()

    # ── Chain runner ────────────────────────────────────────────────────────
    def _run(self, template: str, **kwargs: Any) -> dict:
        prompt = ChatPromptTemplate.from_template(template)
        chain  = prompt | self.llm | self._parser
        raw    = chain.invoke(kwargs)
        return _parse_json(raw)

    # ── LLM steps ───────────────────────────────────────────────────────────
    def extract_resume_info(self, resume_text: str) -> dict:
        return self._run(RESUME_EXTRACTION_PROMPT, resume_text=resume_text[:5000])

    def extract_job_requirements(self, job_description: str) -> dict:
        return self._run(JOB_EXTRACTION_PROMPT, job_description=job_description[:5000])

    # ── Deterministic scoring ────────────────────────────────────────────────
    def calculate_ats_score(self, resume_text: str, resume_info: dict, job_req: dict) -> dict:
        text_lower = resume_text.lower()

        req_skills     = job_req.get("required_skills", [])
        matched_skills = [s for s in req_skills if s.lower() in text_lower]
        missing_skills = [s for s in req_skills if s.lower() not in text_lower]
        skills_score   = (len(matched_skills) / len(req_skills) * 100) if req_skills else 75.0

        keywords      = job_req.get("keywords", [])
        matched_kw    = [k for k in keywords if k.lower() in text_lower]
        missing_kw    = [k for k in keywords if k.lower() not in text_lower]
        kw_score      = (len(matched_kw) / len(keywords) * 100) if keywords else 70.0

        req_exp    = float(job_req.get("required_experience_years") or 0)
        resume_exp = float(resume_info.get("experience_years") or 0)
        if req_exp == 0:         exp_score = 100.0
        elif resume_exp >= req_exp: exp_score = 100.0
        else:                    exp_score = min((resume_exp / req_exp) * 100, 100.0)

        pref_skills      = job_req.get("preferred_skills", [])
        matched_preferred = [s for s in pref_skills if s.lower() in text_lower]

        req_langs    = job_req.get("required_languages", [])
        matched_langs = [l for l in req_langs if l.lower() in text_lower]
        missing_langs = [l for l in req_langs if l.lower() not in text_lower]

        req_fw    = job_req.get("required_frameworks", [])
        matched_fw = [f for f in req_fw if f.lower() in text_lower]
        missing_fw = [f for f in req_fw if f.lower() not in text_lower]

        ats = skills_score * 0.40 + kw_score * 0.35 + exp_score * 0.25

        return {
            "ats_score":       round(ats, 1),
            "skills_score":    round(skills_score, 1),
            "keyword_score":   round(kw_score, 1),
            "experience_score": round(exp_score, 1),
            "matched_skills":  matched_skills,
            "missing_skills":  missing_skills,
            "matched_preferred": matched_preferred,
            "matched_keywords": matched_kw,
            "missing_keywords": missing_kw,
            "matched_languages": matched_langs,
            "missing_languages": missing_langs,
            "matched_frameworks": matched_fw,
            "missing_frameworks": missing_fw,
        }

    def calculate_match_score(self, resume_info: dict, job_req: dict, ats: dict) -> dict:
        skills_pct = ats["skills_score"]
        exp_pct    = ats["experience_score"]
        kw_pct     = ats["keyword_score"]

        resume_edu = (resume_info.get("education") or "").lower()
        job_edu    = (job_req.get("education_requirement") or "").lower()
        edu_keys   = ["bachelor","master","phd","doctorate","degree","b.s","m.s"]
        has_degree = any(k in resume_edu for k in edu_keys)
        if "phd" in job_edu or "doctorate" in job_edu:
            edu_score = 100.0 if ("phd" in resume_edu or "doctorate" in resume_edu) else 55.0
        elif "master" in job_edu:
            edu_score = 100.0 if ("master" in resume_edu or "phd" in resume_edu) else (75.0 if has_degree else 50.0)
        else:
            edu_score = 100.0 if has_degree else 65.0

        req_langs  = [l.lower() for l in job_req.get("required_languages", [])]
        res_langs  = [l.lower() for l in resume_info.get("languages", [])]
        lang_score = (len(set(req_langs) & set(res_langs)) / len(req_langs) * 100) if req_langs else 80.0

        overall = (
            skills_pct * 0.30 + exp_pct * 0.20 +
            kw_pct * 0.25 + edu_score * 0.10 + lang_score * 0.15
        )

        return {
            "overall_match":        round(overall, 1),
            "skills_alignment":     round(skills_pct, 1),
            "experience_alignment": round(exp_pct, 1),
            "keyword_alignment":    round(kw_pct, 1),
            "education_alignment":  round(edu_score, 1),
            "language_alignment":   round(lang_score, 1),
        }

    def generate_recommendations(self, resume_info: dict, job_req: dict,
                                  ats: dict, match: dict) -> dict:
        return self._run(
            RECOMMENDATIONS_PROMPT,
            job_title=job_req.get("job_title", "the role"),
            ats_score=ats["ats_score"],
            overall_match=match["overall_match"],
            missing_skills=ats["missing_skills"][:12],
            matched_skills=ats["matched_skills"][:12],
            resume_summary=resume_info.get("summary", "Not provided"),
        )

    # ── Full pipeline ────────────────────────────────────────────────────────
    def full_analysis(self, resume_text: str, job_description: str) -> dict:
        resume_info = self.extract_resume_info(resume_text)
        job_req     = self.extract_job_requirements(job_description)
        ats         = self.calculate_ats_score(resume_text, resume_info, job_req)
        match       = self.calculate_match_score(resume_info, job_req, ats)
        recs        = self.generate_recommendations(resume_info, job_req, ats, match)
        return {
            "resume_info":      resume_info,
            "job_requirements": job_req,
            "ats_analysis":     ats,
            "match_score":      match,
            "recommendations":  recs,
        }
