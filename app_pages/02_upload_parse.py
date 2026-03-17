import streamlit as st
import pandas as pd
from core.models import Candidate
from core.file_handler import process_file_bytes, extract_from_zip
from core.llm_client import parse_resume_with_llm
import time
import uuid
from core.theme import apply_theme

apply_theme()
st.title("📄 Upload & Parse Resumes")

if not st.session_state.drive_config:
    st.warning("⚠️ Please configure the drive first before uploading resumes.")
    if st.button("Go to Drive Setup"):
        st.switch_page("app_pages/01_drive_setup.py")
    st.stop()

st.markdown("Upload resumes or a ZIP file containing resumes. The AI will parse them into structured profiles.")

# File uploader
uploaded_files = st.file_uploader(
    "Drop resume files here or click to browse (PDF, DOCX, ZIP)", 
    type=["pdf", "docx", "zip"], 
    accept_multiple_files=True
)

if uploaded_files:
    if st.button("🚀 Parse Resumes", type="primary"):
        my_bar = st.progress(0, text="Reading files...")
        
        # 1. Read files and extract text
        raw_candidates = []
        for file in uploaded_files:
            file_bytes = file.read()
            if file.name.lower().endswith('.zip'):
                extracted = extract_from_zip(file_bytes)
                raw_candidates.extend(extracted)
            else:
                text = process_file_bytes(file.name, file_bytes)
                if text:
                    raw_candidates.append({"file_name": file.name, "raw_text": text})
                    
        total = len(raw_candidates)
        if total == 0:
            st.error("No valid text found in uploaded files.")
            st.stop()
            
        st.write(f"Found {total} valid documents. Starting parsing...")
        
        # 2. Parse text with LLM
        parsed_candidates = []
        for i, raw_cand in enumerate(raw_candidates):
            my_bar.progress((i) / total, text=f"Parsing resume {i+1} of {total}: {raw_cand['file_name']}")
            
            profile = parse_resume_with_llm(raw_cand['raw_text'])
            cand = Candidate(
                id=str(uuid.uuid4()),
                file_name=raw_cand['file_name'],
                raw_text=raw_cand['raw_text'],
                profile=profile,
                parsing_confidence=0.9 if profile else 0.0
            )
            parsed_candidates.append(cand)
            
        my_bar.progress(1.0, text="Parsing complete!")
        st.session_state.candidates.extend(parsed_candidates)
        st.success(f"✅ Successfully parsed {total} resumes.")

if st.session_state.candidates:
    st.markdown("---")
    st.subheader("Data Quality Dashboard")
    
    total_parsed = len(st.session_state.candidates)
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Candidadtes", total_parsed)
    col2.metric("Successfully Parsed", sum(1 for c in st.session_state.candidates if c.profile))
    col3.metric("Failed Parsing", sum(1 for c in st.session_state.candidates if not c.profile))
    
    # Completeness matrix
    data = []
    for c in st.session_state.candidates:
        p = c.profile
        data.append({
            "File": c.file_name,
            "Name": "✅" if p and p.name else "❌",
            "Email": "✅" if p and p.email else "❌",
            "Phone": "✅" if p and p.phone else "❌",
            "Education": "✅" if p and p.education and p.education.degree else "❌",
            "CGPA": "✅" if p and p.education and p.education.cgpa_or_percentage else "❌",
            "Skills": "✅" if p and p.programming_languages else "❌",
            "Projects": "✅" if p and p.projects else "❌"
        })
        
    df = pd.DataFrame(data)
    st.dataframe(df, width='stretch')
    
    if st.button("Proceed to Screening →", type="primary"):
        st.switch_page("app_pages/03_screening.py")
