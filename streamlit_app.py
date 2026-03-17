import streamlit as st
import time
from core.theme import apply_theme

st.set_page_config(page_title="CampusRecruit AI", page_icon="🎓", layout="wide")
apply_theme()

# Initialize shared state
if "drive_config" not in st.session_state:
    st.session_state.drive_config = None
if "candidates" not in st.session_state:
    st.session_state.candidates = []

# Navigation
pages = [
    st.Page("app_pages/01_drive_setup.py", title="Drive Setup", icon="⚙️"),
    st.Page("app_pages/02_upload_parse.py", title="Upload & Parse", icon="📄"),
    st.Page("app_pages/03_screening.py", title="Screening", icon="🔍"),
    st.Page("app_pages/04_briefs.py", title="Candidate Briefs", icon="📋"),
    st.Page("app_pages/05_communications.py", title="Communications", icon="✉️"),
]
page = st.navigation(pages)

# Shared sidebar
with st.sidebar:
    st.title("🎓 CampusRecruit AI")
    if st.session_state.drive_config:
        st.success(f"Drive: {st.session_state.drive_config.company_name} → {st.session_state.drive_config.college_name}")
        st.metric("Candidates", len(st.session_state.candidates))
    else:
        st.warning("Drive not configured")
        
    st.markdown("---")
    st.markdown("### 🔄 Quick Demo")
    if st.button("Load Sample Data"):
        from sample_data.mock_data import get_demo_drive_config, MOCK_CANDIDATES_DATA
        from core.models import Candidate, TierEnum
        st.session_state.drive_config = get_demo_drive_config()
        st.session_state.candidates = [Candidate(**c) for c in MOCK_CANDIDATES_DATA]
        
        # Determine tiers simply based on mock parsing config so that app flows logic starts smoothly
        from core.hard_filters import apply_hard_filters
        for candidate in st.session_state.candidates:
            passed, details = apply_hard_filters(candidate, st.session_state.drive_config)
            candidate.hard_filter_passed = passed
            candidate.hard_filter_details = details
            
        st.success("Sample data loaded successfully!")
        time.sleep(1)
        st.rerun()

page.run()
