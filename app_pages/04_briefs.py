import streamlit as st
from core.models import TierEnum
from core.theme import apply_theme
from core.llm_client import generate_brief_with_llm

apply_theme()
st.title("📋 Candidate Briefs")

if not st.session_state.get('shortlist_approved', False):
    st.warning("⚠️ Please approve the shortlist on the Screening page first.")
    if st.button("Go to Screening"):
        st.switch_page("app_pages/03_screening.py")
    st.stop()

shortlisted = [c for c in st.session_state.candidates if c.tier in [TierEnum.TIER_1, TierEnum.TIER_2]]

if not shortlisted:
    st.info("No candidates were shortlisted.")
    st.stop()

st.write(f"Generate interview preparation briefs for {len(shortlisted)} shortlisted candidates.")

if st.button("📋 Generate All Briefs", type="primary"):
    my_bar = st.progress(0, text="Generating briefs...")
    for i, c in enumerate(shortlisted):
        my_bar.progress(i / len(shortlisted), text=f"Generating brief for {c.profile.name}...")
        
        if not c.candidate_brief and c.ai_scores:
            role_title = st.session_state.drive_config.roles[0].title if st.session_state.drive_config.roles else "Software Engineer"
            brief = generate_brief_with_llm(c.profile, c.ai_scores, role_title)
            c.candidate_brief = brief
            
    my_bar.progress(1.0, text="Generation complete!")
    st.session_state.briefs_generated = True
    st.success(f"Generated {len(shortlisted)} briefs.")

if st.session_state.get('briefs_generated', False):
    st.markdown("---")
    
    for c in shortlisted:
        if c.candidate_brief:
            with st.container(border=True):
                st.subheader(f"{c.profile.name} | {c.tier}")
                st.markdown(c.candidate_brief)
                col1, col2 = st.columns([1, 4])
                col1.button("📥 Download", key=f"dl_{c.id}")
                col2.button("📋 Copy to Clipboard", key=f"cp_{c.id}")
                
    st.markdown("---")
    if st.button("Proceed to Communications →", type="primary"):
        st.switch_page("app_pages/05_communications.py")
