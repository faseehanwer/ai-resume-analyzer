"""
Prompt templates for AI Resume Analyzer & Job Match System.
All templates are structured to return valid JSON for reliable parsing.
"""

RESUME_EXTRACTION_PROMPT = """\
You are an expert resume parser. Analyze the resume below and extract structured data.
Return ONLY a valid JSON object — no markdown, no explanation, no code fences.

Resume Text:
{resume_text}

Return this exact JSON structure (fill every field; use [] for missing lists and null for missing strings):
{{
  "name": "Full Name",
  "email": "email@example.com",
  "phone": "phone number or null",
  "location": "City, Country or null",
  "current_role": "Most recent job title",
  "experience_years": 0,
  "summary": "Professional summary in 2-3 sentences",
  "skills": ["skill1", "skill2"],
  "languages": ["Python", "JavaScript"],
  "frameworks": ["Django", "React"],
  "tools": ["Git", "Docker", "AWS"],
  "databases": ["PostgreSQL", "MongoDB"],
  "soft_skills": ["communication", "leadership"],
  "certifications": ["cert1"],
  "education": "Highest degree and field",
  "companies": ["Company A", "Company B"],
  "achievements": ["achievement1", "achievement2"]
}}"""

JOB_EXTRACTION_PROMPT = """\
You are an expert job description analyst. Extract structured requirements from the job posting below.
Return ONLY a valid JSON object — no markdown, no explanation, no code fences.

Job Description:
{job_description}

Return this exact JSON structure:
{{
  "job_title": "Position Title",
  "company": "Company Name or Unknown",
  "employment_type": "Full-time / Part-time / Contract",
  "remote": true,
  "required_experience_years": 3,
  "education_requirement": "Bachelor's / Master's / Any",
  "required_skills": ["skill1", "skill2"],
  "preferred_skills": ["skill3", "skill4"],
  "required_languages": ["Python", "SQL"],
  "required_frameworks": ["FastAPI", "React"],
  "required_tools": ["Docker", "Git"],
  "key_responsibilities": ["responsibility1", "responsibility2"],
  "keywords": ["keyword1", "keyword2", "keyword3"],
  "nice_to_have": ["bonus skill 1", "bonus skill 2"]
}}"""

RECOMMENDATIONS_PROMPT = """\
You are a senior career coach and technical recruiter. Based on this resume-job analysis, \
generate highly specific, actionable career advice. Return ONLY valid JSON.

Job Title: {job_title}
ATS Score: {ats_score}%
Overall Match: {overall_match}%
Missing Skills: {missing_skills}
Matched Skills: {matched_skills}
Resume Summary: {resume_summary}

Return this exact JSON structure:
{{
  "overall_advice": "2-3 sentence strategic overview of candidacy and next steps",
  "immediate_actions": [
    {{"action": "specific action to take", "impact": "why this matters", "timeline": "1 week"}},
    {{"action": "...", "impact": "...", "timeline": "..."}},
    {{"action": "...", "impact": "...", "timeline": "..."}}
  ],
  "skill_development": [
    {{"skill": "skill name", "resource": "specific course or resource", "priority": "High", "time_to_learn": "2 weeks"}},
    {{"skill": "...", "resource": "...", "priority": "Medium", "time_to_learn": "..."}},
    {{"skill": "...", "resource": "...", "priority": "Low", "time_to_learn": "..."}}
  ],
  "resume_improvements": [
    "Specific resume improvement tip 1",
    "Specific resume improvement tip 2",
    "Specific resume improvement tip 3",
    "Specific resume improvement tip 4"
  ],
  "interview_tips": [
    "Interview preparation tip 1",
    "Interview preparation tip 2",
    "Interview preparation tip 3"
  ],
  "keywords_to_add": ["keyword1", "keyword2", "keyword3", "keyword4"]
}}"""
