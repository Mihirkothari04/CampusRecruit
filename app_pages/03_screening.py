import streamlit as st
import pandas as pd
from core.models import Candidate, TierEnum
from core.hard_filters import apply_hard_filters
from core.llm_client import score_candidate_with_llm
from core.theme import apply_theme

apply_theme()
st.title("🔍 Screening & Shortlisting")

if not st.session_state.candidates:
    st.warning("⚠️ No parsed candidates found. Please upload resumes first.")
    if st.button("Go to Upload & Parse"):
        st.switch_page("app_pages/02_upload_parse.py")
    st.stop()

st.markdown("### STAGE A: Eligibility Filtering")
if st.button("Apply Hard Filters", type="primary"):
    with st.spinner("Applying rules..."):
        for cand in st.session_state.candidates:
            if not cand.profile:
                cand.hard_filter_passed = False
                continue
            passed, details = apply_hard_filters(cand, st.session_state.drive_config)
            cand.hard_filter_passed = passed
            cand.hard_filter_details = details
    st.success("Eligibility checked.")

# Summarize hard filters
total = len(st.session_state.candidates)
passed_hf = sum(1 for c in st.session_state.candidates if c.hard_filter_passed)
eval_hf = sum(1 for c in st.session_state.candidates if c.hard_filter_passed is not None)

if eval_hf > 0:
    st.info(f"Passed Hard Filters: {passed_hf} out of {eval_hf}")
    
    st.markdown("---")
    st.markdown("### STAGE B: AI Screening")
    st.write("Score eligible candidates based on multi-dimensional criteria using AI.")
    
    if st.button("🧠 Run AI Screening", type="primary"):
        eligible_cands = [c for c in st.session_state.candidates if c.hard_filter_passed]
        my_bar = st.progress(0, text="Starting screening...")
        
        for i, cand in enumerate(eligible_cands):
            my_bar.progress((i) / len(eligible_cands), text=f"Scoring {cand.profile.name}...")
            scores = score_candidate_with_llm(cand.profile, st.session_state.drive_config)
            if scores:
                cand.ai_scores = scores
                if scores.overall_score >= 7.5:
                    cand.tier = TierEnum.TIER_1
                elif scores.overall_score >= 5.5:
                    cand.tier = TierEnum.TIER_2
                else:
                    cand.tier = TierEnum.TIER_3
        my_bar.progress(1.0, text="Screening complete!")
        st.success("AI Screening finished.")

# Show Tier Dashboards if screening is done
screened = sum(1 for c in st.session_state.candidates if c.ai_scores)
if screened > 0:
    st.markdown("---")
    t1 = sum(1 for c in st.session_state.candidates if c.tier == TierEnum.TIER_1)
    t2 = sum(1 for c in st.session_state.candidates if c.tier == TierEnum.TIER_2)
    t3 = sum(1 for c in st.session_state.candidates if c.tier == TierEnum.TIER_3)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Tier 1 (Strong Match) 🟢", t1)
    col2.metric("Tier 2 (Partial Match) 🟡", t2)
    col3.metric("Tier 3 (Weak Match) 🔴", t3)
    
    tab1, tab2, tab3 = st.tabs(["Tier 1", "Tier 2", "Tier 3"])
    
    def display_candidates_for_tier(tier):
        for c in st.session_state.candidates:
            if c.tier == tier and c.ai_scores:
                with st.expander(f"**{c.profile.name}** | Score: {c.ai_scores.overall_score:.1f}/10"):
                    st.write(f"🎓 {c.profile.education.degree if c.profile.education else 'Edu'} | {c.profile.education.branch if c.profile.education else 'No Branch'} | CGPA: {c.profile.education.cgpa_or_percentage if c.profile.education else 'N/A'}")
                    st.markdown("**Strengths:** " + ", ".join(c.ai_scores.key_strengths[:2]))
                    st.markdown("**Concerns:** " + ", ".join(c.ai_scores.concerns[:2]))
                    st.write("---")
                    st.write(f"Tech: {c.ai_scores.technical_skills.score} | Proj: {c.ai_scores.project_relevance.score} | Prac: {c.ai_scores.practical_experience.score} | Learn: {c.ai_scores.learning_trajectory.score} | Comm: {c.ai_scores.communication_indicators.score}")

    with tab1: display_candidates_for_tier(TierEnum.TIER_1)
    with tab2: display_candidates_for_tier(TierEnum.TIER_2)
    with tab3: display_candidates_for_tier(TierEnum.TIER_3)

    st.markdown("---")
    st.subheader("Action")
    if st.button("✅ APPROVE SHORTLIST", type="primary"):
        st.session_state.shortlist_approved = True
        st.toast("Shortlist approved! Briefs and Communications unlocked.")
        st.switch_page("app_pages/04_briefs.py")
