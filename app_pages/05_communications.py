import streamlit as st
import pandas as pd
from core.models import TierEnum
from core.theme import apply_theme
from core.llm_client import generate_communication_with_llm

apply_theme()
st.title("✉️ Communications")

if not st.session_state.get('shortlist_approved', False):
    st.warning("⚠️ Please approve the shortlist on the Screening page first.")
    if st.button("Go to Screening"):
        st.switch_page("app_pages/03_screening.py")
    st.stop()

st.write("Generate and review communication drafts for all candidates.")

mode = st.radio("Communication Mode", ["📧 Direct to Students", "🏫 Through Placement Cell"])

role_title = st.session_state.drive_config.roles[0].title if st.session_state.drive_config.roles else "Software Engineer"
company_name = st.session_state.drive_config.company_name if st.session_state.drive_config else "Company"

if st.button("✉️ Generate All Drafts", type="primary"):
    my_bar = st.progress(0, text="Generating communications...")
    total = len(st.session_state.candidates)
    
    for i, c in enumerate(st.session_state.candidates):
        my_bar.progress(i / total, text=f"Drafting for {c.profile.name}...")
        
        is_shortlisted = c.tier in [TierEnum.TIER_1, TierEnum.TIER_2]
        c.communication_type = "shortlisted" if is_shortlisted else "rejected"
        
        top_strength = c.ai_scores.key_strengths[0] if getattr(c, 'ai_scores', None) else ""
        
        draft = generate_communication_with_llm(
            candidate_name=c.profile.name,
            role_title=role_title,
            company_name=company_name,
            is_shortlisted=is_shortlisted,
            top_strength=top_strength
        )
        c.communication_draft = draft
        
    my_bar.progress(1.0, text="Generation complete!")
    st.session_state.communications_generated = True
    st.success(f"Generated {total} communication drafts.")

if st.session_state.get('communications_generated', False):
    st.markdown("---")
    
    if mode == "📧 Direct to Students":
        tab1, tab2 = st.tabs(["✅ Shortlisted / Waitlisted", "❌ Not Selected"])
        
        with tab1:
            for c in st.session_state.candidates:
                if c.communication_type == "shortlisted" and c.communication_draft:
                    with st.container(border=True):
                        st.markdown(f"**To:** {c.profile.email or 'N/A'}")
                        st.markdown(f"**Subject:** Interview Invitation — {company_name}")
                        st.text_area("Content", c.communication_draft, height=150, key=f"ta_{c.id}")
                        st.button("✅ Approve", key=f"app_{c.id}")
                        
        with tab2:
            for c in st.session_state.candidates:
                if c.communication_type == "rejected" and c.communication_draft:
                    with st.container(border=True):
                        st.markdown(f"**To:** {c.profile.email or 'N/A'}")
                        st.markdown(f"**Subject:** Update on Your Application — {company_name}")
                        st.text_area("Content", c.communication_draft, height=150, key=f"ta_rej_{c.id}")
                        st.button("✅ Approve", key=f"app_rej_{c.id}")
                        
    else:
        st.subheader("Placement Cell Summary")
        data = []
        for c in st.session_state.candidates:
            data.append({
                "Roll No": c.profile.roll_number if c.profile else "N/A",
                "Name": c.profile.name if c.profile else "N/A",
                "Branch": c.profile.education.branch if (c.profile and c.profile.education) else "N/A",
                "CGPA": c.profile.education.cgpa_or_percentage if (c.profile and c.profile.education) else "N/A",
                "Status": "Shortlisted" if c.communication_type == "shortlisted" else "Not Selected"
            })
        df = pd.DataFrame(data)
        st.dataframe(df, width='stretch')
        st.download_button("📥 Download as CSV", df.to_csv(index=False).encode('utf-8'), "placement_summary.csv", "text/csv")
        
        st.markdown("---")
        st.subheader("Cover Email to Placement Cell")
        short_count = sum(1 for c in st.session_state.candidates if c.communication_type == "shortlisted")
        rej_count = sum(1 for c in st.session_state.candidates if c.communication_type == "rejected")
        
        default_email = f"Subject: Campus Drive Results — {company_name}\n\nDear Placement Cell,\n\nThank you for organizing the campus drive.\n\nSummary:\n- Total resumes reviewed: {len(st.session_state.candidates)}\n- Shortlisted for interview: {short_count}\n- Not proceeding: {rej_count}\n\nPlease find the detailed list attached."
        
        st.text_area("Email Content", default_email, height=200)
    
    st.markdown("---")
    st.success("🎉 You have completed the CampusRecruit AI process!")
