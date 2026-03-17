# CampusRecruit AI

## Single Source of Truth for Automation

**CampusRecruit AI** is an Agentic AI-based Internal HR Tool developed specifically for Campus Placement drives. It automates the entire placement pipeline starting from a bulk resume intake dump from colleges through dynamic AI-driven scoring, to final email communication draft generation.

### Key Features (MVP)
1. **Drive Setup & Resume Intake:** Configurable roles, weights, hard filters (CGPA, branches, backlogs), and ZIP/PDF/DOCX uploading and AI-based resume parsing.
2. **Two-Stage Screening & Shortlisting:** Deterministic validation layered with an LLM-powered multi-dimensional evaluation (Technical, Project, Experience, Learning, Communication).
3. **Candidate Brief Generation:** Automated 1-page generation of what to ask candidates.
4. **Communication:** Email drafting to candidates or bulk CSV summaries for the Placement cells.

### Quick Start
To run this application locally:

1. Create a `.streamlit/secrets.toml` with `OPENAI_API_KEY = "sk-..."` (or rely on Streamlit Cloud's Secrets).
2. Install standard dependencies from `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run streamlit_app.py
   ```

### Application Structure
* `streamlit_app.py` and `app_pages/` - Streamlit views.
* `core/models.py` - Pydantic definition models.
* `core/prompts.py` - AI prompts and tuning instructions.
* `core/hard_filters.py` - Deterministic parsing rules.
* `core/llm_client.py` - LangChain & OpenAI API integrations.
* `agents/orchestrator.py` - LangGraph state machine structure for future scalable workflow adaptation.

### Production Vision
For a detailed look into what exactly should be implemented moving from this MVP to enterprise scale (Role-Based Access Control, PostgreSQL, multi-user deployments), check `docs/`.
