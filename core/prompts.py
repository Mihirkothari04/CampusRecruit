RESUME_PARSING_PROMPT = """You are a resume parser for campus recruitment.
Extract EXACTLY the following fields from the resume text.
If a field is not found, use null. Do not infer or guess.

Return ONLY valid JSON matching this schema:
{{
    "name": string,
    "email": string | null,
    "phone": string | null,
    "roll_number": string | null,
    "education": {{
        "degree": string,
        "branch": string,
        "institution": string,
        "cgpa_or_percentage": number | null,
        "scale": "10" | "4" | "percentage" | null,
        "graduation_year": number | null
    }},
    "programming_languages": [string],
    "frameworks_and_tools": [string],
    "domains": [string],
    "projects": [
        {{"title": string, "description": string, "technologies_used": [string]}}
    ],
    "internships": [
        {{"company": string, "role": string, "duration": string, "description": string}}
    ],
    "certifications": [string],
    "achievements": [string]
}}

Resume text:
{resume_text}
"""

SCREENING_PROMPT = """You are evaluating a candidate for the role: {role_title}

Role requirements:
{role_requirements_json}

Candidate profile:
{candidate_profile_json}

Score this candidate on each dimension below.
For each dimension: Score from 1-10, provide 1-2 sentence justification.

IMPORTANT: You are evaluating a FRESH GRADUATE. Calibrate accordingly.
- One strong internship = above average
- Three relevant projects = excellent for campus
- Don't penalize for limited work experience

IMPORTANT: This is a BLIND screening. Evaluate only on skills, projects,
experience, and qualifications. Do not factor in name, gender, or institution.

Dimensions:
1. TECHNICAL_SKILLS (weight: {w1}): Match to role requirements
2. PROJECT_RELEVANCE (weight: {w2}): Quality and relevance of projects
3. PRACTICAL_EXPERIENCE (weight: {w3}): Internships, real-world exposure
4. LEARNING_TRAJECTORY (weight: {w4}): Growth, self-learning, curiosity
5. COMMUNICATION_INDICATORS (weight: {w5}): Resume clarity, articulation

Return ONLY valid JSON structure that matches the requested schema.
"""

BRIEF_PROMPT = """Create a concise interview preparation brief for the following candidate.
This will be read by an interviewer 5 minutes before the interview.

Candidate profile: {candidate_profile_json}
Screening assessment: {screening_scores_json}
Role: {role_title}

Generate in this EXACT format:
## PROFILE SNAPSHOT (3 lines max)
[Who is this candidate in a nutshell?]

## STRENGTHS TO EXPLORE (2-3 bullets)
[What looks promising? Include follow-up questions.]

## AREAS TO PROBE (2-3 bullets)
[What needs verification? Gaps? Shallow claims?]

## SUGGESTED QUESTIONS (3-4 questions)
[Tailored to THIS candidate. NOT generic.]

## RED FLAGS (if any)
[Inconsistencies, unexplained gaps, overclaimed skills]

Keep total under 300 words. Interviewers won't read more.
"""

SHORTLISTED_EMAIL_PROMPT = """Write a professional, warm email to a campus placement candidate who has been SHORTLISTED.

Candidate: {name}
Role: {role_title}
Company: {company_name}

Include:
- Congratulations
- Next steps (interview date/time if known)
- What to prepare
- Contact for questions

Tone: Professional but warm. Remember this is likely their first job interview.
Keep under 150 words.
"""

NOT_SHORTLISTED_EMAIL_PROMPT = """Write a respectful, constructive email to a campus placement candidate who was NOT shortlisted.

Candidate: {name}
Key strength area: {top_strength}
Role: {role_title}
Company: {company_name}

Include:
- Thank them for applying
- Brief, constructive reason (without being specific about scores)
- Encouragement
- Note that this doesn't reflect their overall potential

Tone: Respectful, kind. Do NOT be patronizing. Keep under 100 words.
"""
