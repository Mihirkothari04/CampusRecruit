import streamlit as st
from core.models import DriveConfig, RoleConfig
import datetime
from core.theme import apply_theme

apply_theme()
st.title("⚙️ Drive Setup")
st.markdown("Configure the campus drive details, role requirements, and AI screening parameters.")

col1, col2 = st.columns([2, 1])

with col1:
    with st.container(border=True):
        st.subheader("1. Drive Information")
        c1, c2 = st.columns(2)
        company_name = c1.text_input("Company Name", value=st.session_state.drive_config.company_name if st.session_state.drive_config else "")
        college_name = c2.text_input("College Name", value=st.session_state.drive_config.college_name if st.session_state.drive_config else "")
        
        c3, c4 = st.columns(2)
        try:
            default_date = datetime.datetime.strptime(st.session_state.drive_config.drive_date, "%Y-%m-%d").date() if st.session_state.drive_config else datetime.date.today()
        except:
            default_date = datetime.date.today()
        drive_date = c3.date_input("Drive Date", value=default_date)
        
    with st.container(border=True):
        st.subheader("2. Role Configuration")
        role_title = st.text_input("Role Title", value="Software Engineer")
        c1, c2 = st.columns(2)
        department = c1.text_input("Department", value="Engineering")
        positions = c2.number_input("Positions Available", min_value=1, value=5)
        
    with st.container(border=True):
        st.subheader("3. Eligibility Criteria (Hard Filters)")
        c1, c2, c3 = st.columns(3)
        min_cgpa = c1.slider("Minimum CGPA/Percentage", 0.0, 100.0, 7.0, 0.1)
        cgpa_scale = c2.selectbox("CGPA Scale", ["10", "4", "percentage"])
        max_backlogs = c3.number_input("Max Active Backlogs", min_value=0, value=0)
        
        all_branches = ["Computer Science", "Information Technology", "Electronics", "Mechanical", "Civil", "Other"]
        allowed_branches = st.multiselect("Allowed Branches", all_branches, default=["Computer Science", "Information Technology", "Electronics"])
        
    with st.container(border=True):
        st.subheader("4. Skill Requirements")
        req_skills_str = st.text_input("Must-Have Skills (comma-separated)", value="Python, SQL, Data Structures")
        pref_skills_str = st.text_input("Nice-to-Have Skills (comma-separated)", value="React, AWS, Docker")
        
    with st.container(border=True):
        st.subheader("5. Scoring Weights")
        st.info("These weights power the AI screening logic. They must sum to 1.0 (100%).")
        w_tech = st.slider("Technical Skills", 0.0, 1.0, 0.25, 0.05)
        w_proj = st.slider("Project Relevance", 0.0, 1.0, 0.25, 0.05)
        w_prac = st.slider("Practical Experience", 0.0, 1.0, 0.20, 0.05)
        w_learn = st.slider("Learning Trajectory", 0.0, 1.0, 0.15, 0.05)
        w_comm = st.slider("Communication", 0.0, 1.0, 0.15, 0.05)
        
        total_weight = w_tech + w_proj + w_prac + w_learn + w_comm
        if abs(total_weight - 1.0) > 0.01:
            st.warning(f"Weights currently sum to {total_weight:.2f}. Please adjust to exactly 1.00.")

with col2:
    st.subheader("📋 Configuration Preview")
    html_preview = f"""
    <div style="background: rgba(30, 41, 59, 0.7); border-radius: 16px; padding: 24px; border: 1px solid rgba(99, 102, 241, 0.3); box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);">
        <h3 style="color: #F8FAFC; margin-top: 0; margin-bottom: 8px; font-size: 1.4rem;">{role_title}</h3>
        <p style="color: #94A3B8; font-size: 0.95rem; margin-bottom: 20px;">
            <strong style="color: #6366F1;">@ {company_name}</strong> &bull; {college_name} &bull; {drive_date.strftime('%b %d, %Y') if isinstance(drive_date, datetime.date) else drive_date}
        </p>
        
        <div style="display: flex; gap: 10px; margin-bottom: 20px;">
            <div style="background: rgba(99, 102, 241, 0.2); color: #818CF8; padding: 4px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 600;">
                {positions} Positions
            </div>
            <div style="background: rgba(16, 185, 129, 0.2); color: #34D399; padding: 4px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 600;">
                CGPA &ge; {min_cgpa}/{cgpa_scale}
            </div>
        </div>
        
        <div style="margin-bottom: 16px;">
            <h4 style="color: #E2E8F0; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px;">Must Have</h4>
            <div style="display: flex; flex-wrap: wrap; gap: 6px;">
                {' '.join([f'<span style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); padding: 3px 10px; border-radius: 6px; font-size: 0.8rem; color: #cbd5e1;">{s.strip()}</span>' for s in req_skills_str.split(',') if s.strip()])}
            </div>
        </div>
        
        <div style="margin-bottom: 20px;">
            <h4 style="color: #E2E8F0; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px;">Nice to Have</h4>
            <div style="display: flex; flex-wrap: wrap; gap: 6px;">
                {' '.join([f'<span style="background: rgba(255,255,255,0.05); border: 1px dashed rgba(255,255,255,0.1); padding: 3px 10px; border-radius: 6px; font-size: 0.8rem; color: #94A3B8;">{s.strip()}</span>' for s in pref_skills_str.split(',') if s.strip()])}
            </div>
        </div>
        
        <div style="border-top: 1px solid rgba(255,255,255,0.05); padding-top: 16px;">
            <h4 style="color: #E2E8F0; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 12px;">AI Scoring Engine</h4>
            <div style="height: 8px; width: 100%; border-radius: 4px; display: flex; overflow: hidden;">
                <div style="width: {int(w_tech*100)}%; background: #6366F1;" title="Technical: {int(w_tech*100)}%"></div>
                <div style="width: {int(w_proj*100)}%; background: #8B5CF6;" title="Projects: {int(w_proj*100)}%"></div>
                <div style="width: {int(w_prac*100)}%; background: #EC4899;" title="Practical: {int(w_prac*100)}%"></div>
                <div style="width: {int(w_learn*100)}%; background: #14B8A6;" title="Learning: {int(w_learn*100)}%"></div>
                <div style="width: {int(w_comm*100)}%; background: #F59E0B;" title="Communication: {int(w_comm*100)}%"></div>
            </div>
            <div style="display: flex; justify-content: space-between; margin-top: 6px; font-size: 0.75rem; color: #64748B;">
                <span>Tech {int(w_tech*100)}%</span>
                <span>Proj {int(w_proj*100)}%</span>
                <span>Comm {int(w_comm*100)}%</span>
            </div>
        </div>
    </div>
    """
    st.markdown(html_preview, unsafe_allow_html=True)
    
if st.button("Save & Continue →", type="primary"):
    if not company_name or not college_name:
        st.error("Please fill in Company Name and College Name.")
    elif abs(total_weight - 1.0) > 0.01:
        st.error(f"Weights must sum to 1.0. Currently sum to {total_weight:.2f}")
    else:
        role = RoleConfig(
            title=role_title,
            department=department,
            positions_available=positions,
            min_cgpa=min_cgpa,
            cgpa_scale=cgpa_scale,
            allowed_branches=allowed_branches,
            max_backlogs=max_backlogs,
            required_skills=[s.strip() for s in req_skills_str.split(",") if s.strip()],
            preferred_skills=[s.strip() for s in pref_skills_str.split(",") if s.strip()],
            criteria_weights={
                "technical_skills": w_tech,
                "project_relevance": w_proj,
                "practical_experience": w_prac,
                "learning_trajectory": w_learn,
                "communication_indicators": w_comm
            }
        )
        
        drive = DriveConfig(
            company_name=company_name,
            college_name=college_name,
            drive_date=str(drive_date),
            roles=[role]
        )
        st.session_state.drive_config = drive
        st.toast("✅ Drive configuration saved successfully!")
        st.switch_page("app_pages/02_upload_parse.py")
