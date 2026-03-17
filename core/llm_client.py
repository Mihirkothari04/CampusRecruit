import streamlit as st
import json
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from core.models import CandidateProfile, ScreeningScores
from core.prompts import (
    RESUME_PARSING_PROMPT, 
    SCREENING_PROMPT, 
    BRIEF_PROMPT, 
    SHORTLISTED_EMAIL_PROMPT, 
    NOT_SHORTLISTED_EMAIL_PROMPT
)

def get_openai_client():
    api_key = st.secrets.get("OPENAI_API_KEY", "")
    return OpenAI(api_key=api_key)

def get_langchain_chat(temperature=0):
    api_key = st.secrets.get("OPENAI_API_KEY", "")
    return ChatOpenAI(api_key=api_key, model="gpt-4o", temperature=temperature)

def parse_resume_with_llm(raw_text: str):
    """Uses OpenAI structured output to parse the resume text."""
    client = get_openai_client()
    try:
        completion = client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a resume parser for campus recruitment. Extract fields accurately without guessing."},
                {"role": "user", "content": RESUME_PARSING_PROMPT.format(resume_text=raw_text)}
            ],
            response_format=CandidateProfile,
            temperature=0
        )
        return completion.choices[0].message.parsed
    except Exception as e:
        print(f"Error parsing resume: {e}")
        return None

def score_candidate_with_llm(candidate_profile, config):
    """Scores candidate using structured output based on dimensions."""
    client = get_openai_client()
    role = config.roles[0] if config.roles else None
    if not role:
        return None
        
    role_reqs = {
        "title": role.title,
        "required_skills": role.required_skills,
        "preferred_skills": role.preferred_skills
    }
    
    weights = role.criteria_weights
    prompt = SCREENING_PROMPT.format(
        role_title=role.title,
        role_requirements_json=json.dumps(role_reqs),
        candidate_profile_json=candidate_profile.model_dump_json(),
        w1=weights.get("technical_skills", 0.25),
        w2=weights.get("project_relevance", 0.25),
        w3=weights.get("practical_experience", 0.20),
        w4=weights.get("learning_trajectory", 0.15),
        w5=weights.get("communication_indicators", 0.15)
    )
    
    try:
        completion = client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert HR evaluator for fresh graduates."},
                {"role": "user", "content": prompt}
            ],
            response_format=ScreeningScores,
            temperature=0
        )
        return completion.choices[0].message.parsed
    except Exception as e:
        print(f"Error scoring candidate: {e}")
        return None

def generate_brief_with_llm(candidate_profile, screening_scores, role_title):
    chat = get_langchain_chat(temperature=0.2)
    prompt = BRIEF_PROMPT.format(
        candidate_profile_json=candidate_profile.model_dump_json(),
        screening_scores_json=screening_scores.model_dump_json(),
        role_title=role_title
    )
    
    try:
        response = chat.invoke([HumanMessage(content=prompt)])
        return response.content
    except Exception as e:
        print(f"Error generating brief: {e}")
        return ""

def generate_communication_with_llm(candidate_name, role_title, company_name, is_shortlisted, top_strength=""):
    chat = get_langchain_chat(temperature=0.4)
    if is_shortlisted:
        prompt = SHORTLISTED_EMAIL_PROMPT.format(
            name=candidate_name,
            role_title=role_title,
            company_name=company_name
        )
    else:
        prompt = NOT_SHORTLISTED_EMAIL_PROMPT.format(
            name=candidate_name,
            top_strength=top_strength,
            role_title=role_title,
            company_name=company_name
        )
        
    try:
        response = chat.invoke([HumanMessage(content=prompt)])
        return response.content
    except Exception as e:
        print(f"Error generating communication: {e}")
        return ""
