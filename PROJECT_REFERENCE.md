# CampusRecruit AI — Complete Project Reference Document

> **Purpose**: This document is the single source of truth for building the CampusRecruit AI project. If the chat session is lost, a new session can use this document to continue building from where we left off.

> **Last Updated**: March 17, 2026

---

## Table of Contents

1. [Problem Statement](#1-problem-statement)
2. [Scope & Constraints](#2-scope--constraints)
3. [User Personas](#3-user-personas)
4. [System Architecture](#4-system-architecture)
5. [Tech Stack (Verified Versions)](#5-tech-stack-verified-versions)
6. [Data Models](#6-data-models)
7. [Agent Design (LangGraph)](#7-agent-design-langgraph)
8. [Phase-by-Phase Implementation](#8-phase-by-phase-implementation)
9. [Streamlit UI Structure](#9-streamlit-ui-structure)
10. [Deployment Strategy](#10-deployment-strategy)
11. [Project File Structure](#11-project-file-structure)
12. [Production Vision (Not Implemented)](#12-production-vision-not-implemented)
13. [Design Decisions & Trade-offs](#13-design-decisions--trade-offs)
14. [Implementation Checklist](#14-implementation-checklist)

---

## 1. Problem Statement

Build an **Agentic AI-based Internal HR (Recruitment) Tool** specifically designed for **Campus Placement** drives. The system automates the entire placement pipeline from resume dump intake through candidate communication — everything except the actual human interviews.

**Key constraint**: This is a campus placement tool, NOT a general recruitment platform. Resumes come as a bulk dump from a single college, not from LinkedIn/job boards. The entire drive is compressed into days, not weeks.

---

## 2. Scope & Constraints

### Time Constraint

- **3 hours** for implementation
- Can use Claude's help during building

### Delivery Requirements

- Must be **deployed** with a sharable link (evaluators may not have technical knowledge to run a repo)
- **Deployment target**: Streamlit Community Cloud (free, shareable URL, Python-native)
- GitHub repo must include comprehensive documentation of full system design even for unimplemented features

### Evaluation Criteria (from evaluator)

- System Design based on Requirements
- User Empathy and Satisfaction
- Code implementation (secondary to design thinking)
- Mention what you were thinking of building even if not implemented due to time constraints

### What We're Implementing (MVP — Phases 1-4)

- Phase 1: Drive Setup & Resume Intake/Parsing
- Phase 2: Two-Stage Screening & Shortlisting
- Phase 3: Candidate Brief Generation
- Phase 4: Communication Draft Generation

### What We're Documenting Only (Production Vision)

- Multi-user authentication (email + JWT)
- Role-based access control (HR Admin, Interviewer, Placement Cell)
- PostgreSQL database with full relational schema
- Object storage for resumes (signed URLs)
- Interview day live dashboard
- Decision support post-interview
- Concurrency handling (optimistic locking, async jobs)
- Analytics and bias detection

---

## 3. User Personas

### Primary: HR Recruiter / Placement Coordinator

- Goes to campus, receives bulk resume dump from college
- Currently manually filters 300-800 resumes in Excel the night before
- Needs: Upload dump → define criteria → get shortlist in minutes → send communications
- Pain: Fatigue-driven inconsistency, missed candidates, time pressure

### Secondary: Interview Panel Members

- Technical leads who fly in for the campus drive
- Get a stack of resumes morning-of with zero context
- Need: One-page candidate brief with strengths, concerns, suggested questions
- Pain: Cold-reading resumes, inconsistent interviews

### Tertiary: College Placement Cell

- Intermediary between company and students
- Provides the resume dump, manages student communication
- Enforces rules (e.g., CGPA cutoff compliance)
- Need: Status dashboard, communication logs, compliance reporting

### Quaternary: Student Candidate

- Anxious, applying to multiple companies through same placement cell
- Need: Timely, clear communication about status
- Pain: Ghosting, unclear timelines, unfair evaluation

---

## 4. System Architecture

### MVP Architecture (What We Build)

```
Streamlit App (single user, Streamlit Cloud)
│
├── Page 1: Drive Setup & Configuration
├── Page 2: Resume Upload & Parsing
├── Page 3: Screening & Shortlisting (two-stage)
├── Page 4: Candidate Briefs
└── Page 5: Communication Drafts

Backend: Python + LangGraph agent orchestration
State: st.session_state + SQLite (single-user, in-memory fallback)
AI: Open AI (GPT 5.2/GPT 5.3)
File handling: pymupdf (PDF), python-docx (DOCX)
Deploy: Streamlit Community Cloud
```

### Production Architecture (Documented Only)

```
┌──────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR AGENT                     │
│            (State Machine + Event Router)                 │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────┐   ┌──────────┐   ┌─────────────────────┐   │
│  │ INTAKE  │──▶│ PARSER   │──▶│ DATA QUALITY CHECK  │   │
│  │ Agent   │   │ Agent    │   │ + Merge with CSV     │   │
│  └─────────┘   └──────────┘   └──────────┬──────────┘   │
│                                           │              │
│                               ┌───────────▼───────────┐  │
│                               │   SCREENING AGENT     │  │
│                               │  Stage A: Hard Filter │  │
│                               │  Stage B: AI Ranking  │  │
│                               └───────────┬───────────┘  │
│                                           │              │
│                              ┌────────────▼────────────┐ │
│                              │  HUMAN APPROVAL GATE    │ │
│                              │  (HR Reviews Shortlist) │ │
│                              └────────────┬────────────┘ │
│                                           │              │
│                    ┌──────────────────────┬┴─────────┐   │
│                    ▼                      ▼          ▼   │
│           ┌──────────────┐  ┌──────────────┐ ┌────────┐ │
│           │ CANDIDATE    │  │COMMUNICATION │ │SCHEDULE│ │
│           │ BRIEF GEN    │  │   AGENT      │ │ AGENT  │ │
│           └──────────────┘  └──────────────┘ └────────┘ │
│                                                          │
├──────────────────────────────────────────────────────────┤
│  SHARED STATE: Candidate DB │ AUDIT LOG │ CONFIG         │
└──────────────────────────────────────────────────────────┘
```

---

## 5. Tech Stack (Verified Versions — March 2026)

### Core Dependencies

#"""Here even if Anthropic is Written use Openai's(GPT 5.2/5.3) Instead"""
| Package | Version | Purpose | Notes |
|---------|---------|---------|-------|
| `langgraph` | 1.1.0 | Agent orchestration, state machine | Latest stable. v1.0 released Oct 2025. Uses `interrupt()` + `Command(resume=...)` for HITL |
| `langchain-core` | ~1.2.x | Base abstractions | Required by langgraph |
| `langchain-anthropic` | latest | Claude LLM integration | For `ChatAnthropic` |
| `streamlit` | ~1.42.x | UI framework | Multi-page via `st.navigation()` + `st.Page()`. Use `app_pages/` not `pages/` directory |
| `pymupdf` | ~1.27.x | PDF text extraction | Fastest PDF extractor. AGPL license (fine for open-source). Import as `pymupdf` or `fitz` |
| `python-docx` | ~1.1.x | DOCX text extraction | For .docx resume parsing |
| `pandas` | ~2.2.x | CSV/Excel handling, data manipulation | For college data CSV processing |
| `openpyxl` | ~3.1.x | Excel file reading | Required by pandas for .xlsx |
| `anthropic` | latest | Anthropic API client | Direct API calls for structured output |
| `pydantic` | ~2.x | Data validation, structured models | For candidate profiles, configs |

### Key Technical Notes (from research)

**LangGraph v1.1.0 (March 2026)**:

- `interrupt()` function is the recommended way for human-in-the-loop (replaces older `interrupt_before` pattern)
- Requires a checkpointer: use `InMemorySaver` for MVP, `SqliteSaver` for persistence
- Resume with `Command(resume=value)`
- `StateGraph` with `TypedDict` state is the core pattern
- v1.1 introduces `version="v2"` for type-safe streaming (optional, not needed for MVP)

**Streamlit Multi-page (2026)**:

- Use `st.navigation()` + `st.Page()` API (newer approach)
- Name pages directory `app_pages/` NOT `pages/` (avoids conflict with old auto-discovery)
- `st.session_state` persists across pages within a session
- Initialize all shared state in main `streamlit_app.py` before `page.run()`

**PDF Extraction**:

- PyPDF2 is DEPRECATED → use `pypdf` (lowercase) or `pymupdf`
- `pymupdf` is fastest and highest quality for text extraction
- `pymupdf4llm` available for markdown output but adds dependency
- For our use case: plain `pymupdf` text extraction is sufficient since LLM handles structuring

**Streamlit Community Cloud Limits**:

- ~1GB RAM (approximate, not officially documented)
- Apps from public repos are public by default
- API keys via `st.secrets` (Settings → Secrets in Streamlit Cloud dashboard)
- Apps sleep after inactivity, wake on visit
- No persistent filesystem — use session_state or external DB

### requirements.txt

```
streamlit>=1.42.0
langgraph>=1.1.0
langchain-core>=1.2.0
langchain-anthropic>=0.3.0
anthropic>=0.40.0
pymupdf>=1.27.0
python-docx>=1.1.0
pandas>=2.2.0
openpyxl>=3.1.0
pydantic>=2.0.0
```

---

## 6. Data Models

### Pydantic Models

```python
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class DriveConfig(BaseModel):
    company_name: str
    college_name: str
    drive_date: str
    roles: List[RoleConfig]

class RoleConfig(BaseModel):
    title: str
    department: str
    positions_available: int
    min_cgpa: float = 0.0
    cgpa_scale: str = "10"  # "10", "4", "percentage"
    allowed_branches: List[str] = []
    max_backlogs: int = 0
    required_skills: List[str] = []
    preferred_skills: List[str] = []
    criteria_weights: dict = Field(default_factory=lambda: {
        "technical_skills": 0.25,
        "project_relevance": 0.25,
        "practical_experience": 0.20,
        "learning_trajectory": 0.15,
        "communication_indicators": 0.15
    })

class Education(BaseModel):
    degree: Optional[str] = None
    branch: Optional[str] = None
    institution: Optional[str] = None
    cgpa_or_percentage: Optional[float] = None
    scale: Optional[str] = None
    graduation_year: Optional[int] = None

class Project(BaseModel):
    title: str
    description: str
    technologies_used: List[str] = []

class Internship(BaseModel):
    company: str
    role: str
    duration: str
    description: str

class CandidateProfile(BaseModel):
    # Identification
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    roll_number: Optional[str] = None

    # Education
    education: Optional[Education] = None

    # Skills
    programming_languages: List[str] = []
    frameworks_and_tools: List[str] = []
    domains: List[str] = []

    # Experience
    projects: List[Project] = []
    internships: List[Internship] = []

    # Additional
    certifications: List[str] = []
    achievements: List[str] = []

class ScreeningScores(BaseModel):
    technical_skills: dict  # {"score": int, "reasoning": str}
    project_relevance: dict
    practical_experience: dict
    learning_trajectory: dict
    communication_indicators: dict
    overall_score: float
    key_strengths: List[str]
    concerns: List[str]

class TierEnum(str, Enum):
    TIER_1 = "TIER_1"  # Strong match
    TIER_2 = "TIER_2"  # Partial match
    TIER_3 = "TIER_3"  # Weak match

class Candidate(BaseModel):
    id: str
    file_name: str
    raw_text: str
    profile: Optional[CandidateProfile] = None
    parsing_confidence: float = 0.0
    parsing_errors: List[str] = []

    # Screening results
    hard_filter_passed: Optional[bool] = None
    hard_filter_details: dict = {}
    ai_scores: Optional[ScreeningScores] = None
    tier: Optional[TierEnum] = None

    # Brief
    candidate_brief: Optional[str] = None

    # Communication
    communication_draft: Optional[str] = None
    communication_type: Optional[str] = None  # "shortlisted", "waitlisted", "rejected"

class RecruitmentState(BaseModel):
    """LangGraph state object"""
    drive_config: Optional[DriveConfig] = None
    candidates: List[Candidate] = []

    # Phase tracking
    parsing_complete: bool = False
    screening_complete: bool = False
    shortlist_approved: bool = False
    briefs_generated: bool = False
    communications_generated: bool = False

    # Statistics
    total_uploaded: int = 0
    total_parsed: int = 0
    parsing_failed: int = 0
    passed_hard_filter: int = 0
    failed_hard_filter: int = 0
    tier_1_count: int = 0
    tier_2_count: int = 0
    tier_3_count: int = 0
```

---

## 7. Agent Design (LangGraph)

### State Machine Definition

```python
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command
from typing import TypedDict, List, Optional, Annotated
import operator

class GraphState(TypedDict):
    drive_config: dict
    candidates: Annotated[list, operator.add]  # or replace strategy
    parsing_complete: bool
    screening_complete: bool
    shortlist_approved: bool
    briefs_generated: bool
    communications_generated: bool

# Build graph
builder = StateGraph(GraphState)

# Nodes
builder.add_node("parse_resumes", parse_resumes_node)
builder.add_node("quality_check", quality_check_node)
builder.add_node("hard_filter", hard_filter_node)
builder.add_node("ai_screening", ai_screening_node)
builder.add_node("human_review_shortlist", human_review_shortlist_node)  # uses interrupt()
builder.add_node("generate_briefs", generate_briefs_node)
builder.add_node("generate_communications", generate_comms_node)

# Edges
builder.add_edge(START, "parse_resumes")
builder.add_edge("parse_resumes", "quality_check")
builder.add_edge("quality_check", "hard_filter")
builder.add_edge("hard_filter", "ai_screening")
builder.add_edge("ai_screening", "human_review_shortlist")

# Conditional after human review
builder.add_conditional_edges(
    "human_review_shortlist",
    lambda s: "proceed" if s["shortlist_approved"] else "revise",
    {"proceed": "generate_briefs", "revise": "ai_screening"}
)

builder.add_edge("generate_briefs", "generate_communications")
builder.add_edge("generate_communications", END)

checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)
```

### Human-in-the-Loop Pattern (LangGraph v1.1)

```python
def human_review_shortlist_node(state):
    """Pauses execution and returns control to Streamlit UI"""
    decision = interrupt({
        "message": "Please review the shortlist and approve or request changes",
        "tier_counts": {
            "tier_1": state["tier_1_count"],
            "tier_2": state["tier_2_count"],
            "tier_3": state["tier_3_count"]
        }
    })

    # When resumed via Command(resume={"approved": True/False, ...})
    if decision.get("approved"):
        return {"shortlist_approved": True}
    else:
        # Apply adjustments and re-screen
        return {"shortlist_approved": False, "drive_config": decision.get("updated_config")}
```

### Practical Note for Streamlit Integration

Due to Streamlit's rerun-on-interaction model, the LangGraph interrupt pattern needs adaptation. Instead of using LangGraph's native interrupt/resume cycle (which works well with FastAPI/async backends), the MVP will:

1. Run each agent node as a separate function called from Streamlit
2. Store intermediate state in `st.session_state`
3. Use Streamlit buttons/forms as the "interrupt" mechanism
4. This preserves the architectural design while being pragmatic for the 3-hour constraint

The LangGraph graph definition serves as the **documented architecture** and could be used directly in the production version with a proper backend.

---

## 8. Phase-by-Phase Implementation

### Phase 1: Drive Setup & Resume Intake/Parsing

**Drive Setup (Page 1)**:

- Conversational-style form (not just blank inputs)
- Fields: company name, college, drive date, role title, department, positions
- Hard filter config: min CGPA, allowed branches, max backlogs
- Skill requirements: must-have vs nice-to-have
- Criteria weight sliders (sum to 1.0)
- Store in session_state as DriveConfig

**Resume Upload & Parsing (Page 2)**:

- File uploader: accept ZIP, multiple PDFs, multiple DOCXs
- Optional: college CSV upload (roll_number, name, branch, cgpa, email)
- Extraction pipeline:
  1. If ZIP: extract files, filter to PDF/DOCX
  2. For each file: extract raw text
     - PDF: `pymupdf.open(file)` → iterate pages → `page.get_text()`
     - DOCX: `python-docx` Document → iterate paragraphs → `.text`
  3. Send raw text to LLM with structured extraction prompt
  4. If CSV provided: merge by roll_number or name+email (CSV wins on CGPA, branch)
  5. Flag low-confidence parses

**LLM Parsing Prompt**:

```
You are a resume parser for campus recruitment.
Extract EXACTLY the following fields from the resume text.
If a field is not found, use null. Do not infer or guess.

Return ONLY valid JSON matching this schema:
{
    "name": string,
    "email": string | null,
    "phone": string | null,
    "roll_number": string | null,
    "education": {
        "degree": string,
        "branch": string,
        "institution": string,
        "cgpa_or_percentage": number | null,
        "scale": "10" | "4" | "percentage" | null,
        "graduation_year": number | null
    },
    "skills": {
        "programming_languages": [string],
        "frameworks_and_tools": [string],
        "domains": [string]
    },
    "projects": [
        {"title": string, "description": string, "technologies_used": [string]}
    ],
    "internships": [
        {"company": string, "role": string, "duration": string, "description": string}
    ],
    "certifications": [string],
    "achievements": [string]
}

Resume text:
{resume_text}
```

**Quality Check Dashboard**:

- Total uploaded vs successfully parsed
- Parsing failures listed with file names
- Confidence scores per candidate
- Data completeness indicators (% with email, phone, CGPA)
- If CSV provided: match rate

### Phase 2: Two-Stage Screening

**Stage A: Deterministic Hard Filters (Python, no AI)**:

```python
def apply_hard_filters(candidate, config):
    results = {}
    passed = True

    # CGPA check (normalize scales)
    if config.min_cgpa > 0 and candidate.profile.education:
        cgpa = normalize_cgpa(
            candidate.profile.education.cgpa_or_percentage,
            candidate.profile.education.scale,
            config.cgpa_scale
        )
        results["cgpa"] = {"passed": cgpa >= config.min_cgpa, "value": cgpa, "required": config.min_cgpa}
        if not results["cgpa"]["passed"]:
            passed = False

    # Branch check
    if config.allowed_branches:
        branch_match = any(
            b.lower() in (candidate.profile.education.branch or "").lower()
            for b in config.allowed_branches
        )
        results["branch"] = {"passed": branch_match, "value": candidate.profile.education.branch}
        if not results["branch"]["passed"]:
            passed = False

    return passed, results
```

**Stage B: AI-Powered Ranking (LLM)**:

```
You are evaluating a candidate for the role: {role_title}

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

Return ONLY valid JSON:
{
    "scores": {
        "technical_skills": {"score": int, "reasoning": string},
        "project_relevance": {"score": int, "reasoning": string},
        "practical_experience": {"score": int, "reasoning": string},
        "learning_trajectory": {"score": int, "reasoning": string},
        "communication_indicators": {"score": int, "reasoning": string}
    },
    "overall_score": float,
    "key_strengths": [string],
    "concerns": [string],
    "tier": "TIER_1" | "TIER_2" | "TIER_3"
}
```

**Tier Thresholds (configurable)**:

- TIER_1: overall_score >= 7.5 (strong match, definite interview)
- TIER_2: 5.5 <= overall_score < 7.5 (partial match, if capacity)
- TIER_3: overall_score < 5.5 (weak match, not recommended)

**Shortlist Review UI**:

- Summary stats: total → passed filters → tier breakdown
- Filter breakdown chart (why candidates were eliminated)
- Expandable candidate cards with score dimensions
- Override capability (move between tiers with reason)
- Threshold adjustment sliders (re-run screening)
- APPROVE button (gates Phase 3 and 4)

### Phase 3: Candidate Brief Generation

**Brief Prompt**:

```
Create a concise interview preparation brief for the following candidate.
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
```

**UI**: Display briefs in expandable cards, option to download all as a single document.

### Phase 4: Communication Draft Generation

**Two modes**:

1. **Direct to student**: Individual personalized emails
2. **Through placement cell**: Consolidated list + summary email

**Shortlisted communication prompt**:

```
Write a professional, warm email to a campus placement candidate who has been SHORTLISTED.

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
```

**Not-shortlisted communication prompt**:

```
Write a respectful, constructive email to a campus placement candidate who was NOT shortlisted.

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
```

**Placement cell batch output**: CSV/table with Roll No, Name, Status, Interview Slot.

**UI**: Draft review interface, edit capability per message, batch approve, download CSV.

---

## 9. Streamlit UI Structure & Complete Feature Specification

### File Layout

```
streamlit_app.py              ← Main entry, st.navigation(), shared state init
app_pages/
  01_drive_setup.py           ← Configure drive, roles, criteria
  02_upload_parse.py          ← Upload resumes + CSV, trigger parsing, quality dashboard
  03_screening.py             ← Run screening, review shortlist, approve
  04_briefs.py                ← Generate & view candidate briefs
  05_communications.py        ← Generate, review, approve communications
```

### streamlit_app.py pattern

```python
import streamlit as st

st.set_page_config(page_title="CampusRecruit AI", page_icon="🎓", layout="wide")

# Initialize shared state
if "drive_config" not in st.session_state:
    st.session_state.drive_config = None
if "candidates" not in st.session_state:
    st.session_state.candidates = []
if "phase" not in st.session_state:
    st.session_state.phase = "setup"

# Navigation
page = st.navigation([
    st.Page("app_pages/01_drive_setup.py", title="Drive Setup", icon="⚙️"),
    st.Page("app_pages/02_upload_parse.py", title="Upload & Parse", icon="📄"),
    st.Page("app_pages/03_screening.py", title="Screening", icon="🔍"),
    st.Page("app_pages/04_briefs.py", title="Candidate Briefs", icon="📋"),
    st.Page("app_pages/05_communications.py", title="Communications", icon="✉️"),
])

# Shared sidebar
with st.sidebar:
    st.title("🎓 CampusRecruit AI")
    if st.session_state.drive_config:
        st.success(f"Drive: {st.session_state.drive_config['company_name']} → {st.session_state.drive_config['college_name']}")
        st.metric("Candidates", len(st.session_state.candidates))

page.run()
```

### Build Order (prioritized by demo impact, NOT page order)

1. Core infrastructure (models, LLM client, file handler) — 30 min
2. **Page 3: Screening** — the money page, most evaluator attention — 45 min
3. Page 1: Drive Setup — 20 min
4. Page 2: Upload & Parse — 30 min
5. Page 4: Briefs — 20 min
6. Page 5: Communications — 20 min
7. Sample data + demo mode — 15 min
8. Polish, deploy, test — 20 min

### Cross-Cutting UI Features (appear on ALL pages)

**Persistent Sidebar**:

- App title with branding icon
- Drive status indicator (configured / not configured)
- Pipeline progress tracker — visual stepper showing: Setup → Upload → Screen → Briefs → Comms
  - Completed steps: green checkmark
  - Current step: blue highlight with pulse animation (CSS)
  - Locked steps: grey with lock icon
- Quick stats when data exists: total candidates, shortlisted, pending actions
- "🔄 Try with Sample Data" button — loads pre-configured demo data so evaluator can skip setup

**Phase Gating**:

- Pages unlock sequentially (you can't screen before parsing, can't brief before approving shortlist)
- Navigation to locked pages shows a friendly message: "Complete [previous step] to unlock this page" with a button to go to the required page
- Going back to completed pages is always allowed (for review/modification)

**Loading States (for ALL LLM operations)**:

- `st.status()` container with animated spinner
- Candidate-level progress: "Parsing candidate 4 of 10: Extracting skills..."
- Estimated time remaining based on average per-candidate time
- Individual candidate status icons update in real-time

**Error Handling (visible to user)**:

- Failed operations don't block others (batch continues on individual failure)
- Failed items shown with red indicator and retry button
- Toast notifications for success/failure: `st.toast("✅ 8/10 resumes parsed successfully")`

---

### PAGE 1: Drive Setup — Detailed Feature Spec

**Layout**: Two-column layout. Left column: configuration form. Right column: live preview.

**Section 1: Drive Information**

- Company name (text input)
- College name (text input)
- Drive date (date picker)
- Drive description (optional text area)

**Section 2: Role Configuration**

- Role title (text input, e.g., "Software Engineer")
- Department (text input, e.g., "Engineering")
- Number of positions (number input with +/- buttons)
- Support for multiple roles (but MVP focuses on single role per drive for simplicity)

**Section 3: Eligibility Criteria (Hard Filters)**

- CGPA/Percentage cutoff: **slider** from 0 to 10 (or 0-100 for percentage)
  - Scale selector: radio buttons for "Out of 10" / "Out of 4" / "Percentage"
  - Helper text below slider: "Setting cutoff to 7.0 typically filters 30-40% of candidates"
- Allowed branches: **multi-select checkboxes** with common options pre-populated
  - CS/IT, ECE, EE, Mechanical, Civil, Chemical, Other
  - "Select All Engineering" shortcut button
- Maximum active backlogs: **number input** (default 0)

**Section 4: Skill Requirements**

- Two-column tag input:
  - Left: "Must-Have Skills" — type and press Enter to add as tag chips
  - Right: "Nice-to-Have Skills" — same interaction
- Pre-populated suggestions based on role title (e.g., "Software Engineer" suggests Python, Java, SQL, Git)

**Section 5: Scoring Weight Configuration**

- Five sliders, one per scoring dimension:
  - Technical Skills Match (default 25%)
  - Project Relevance (default 25%)
  - Practical Experience (default 20%)
  - Learning Trajectory (default 15%)
  - Communication Indicators (default 15%)
- Visual indicator showing weights sum to 100%
- If weights don't sum to 100%, show warning and auto-normalize button
- Horizontal stacked bar showing weight distribution visually

**Right Column: Live Configuration Preview**

- Plain English summary that updates in real-time:

  ```
  Looking for: Software Engineer at TechCorp
  College: IIT Bombay | Date: March 25, 2026
  Positions: 5

  Eligibility: CGPA ≥ 7.0/10, CS/IT/ECE branches, 0 backlogs
  Must have: Python, SQL, Data Structures
  Nice to have: AWS, Docker, React

  Scoring emphasis: Technical Skills (25%) and Projects (25%)
  weighted highest
  ```

**Bottom**: Large "Save & Continue →" button. On save, shows success toast and auto-navigates to Page 2.

---

### PAGE 2: Upload & Parse — Detailed Feature Spec

**Phase Gate Check**: If drive not configured, show message + redirect button to Page 1.

**Section 1: File Upload**

- Large drag-and-drop zone: "Drop resume files here or click to browse"
  - Accepts: PDF, DOCX (multiple files)
  - Also accepts: ZIP file containing PDFs/DOCXs
  - File type and size validation with clear error messages
  - Shows uploaded file list with individual remove buttons
- Secondary upload area: "Optional: Upload College Data (CSV/Excel)"
  - Expected columns: roll_number, name, branch, cgpa, email
  - On upload: preview first 5 rows in a table
  - Column mapping if headers don't match expected names

**Section 2: Parsing Controls**

- "🚀 Parse All Resumes" button (large, prominent)
- During parsing: `st.status()` with real-time progress
  ```
  📄 Parsing resumes... (4/10)
  ├── ✅ john_doe_resume.pdf — Parsed successfully
  ├── ✅ jane_smith_resume.pdf — Parsed successfully
  ├── ✅ raj_patel_resume.docx — Parsed successfully
  ├── ⏳ priya_kumar_resume.pdf — Extracting skills...
  ├── ⬜ remaining_6_files...
  ```

**Section 3: Parsing Quality Dashboard** (appears after parsing)

**Top Row — Key Metrics** (using `st.metric` with delta indicators):

```
| Total Uploaded | Successfully Parsed | Needs Review | Failed |
| 10             | 8 (✅)              | 1 (⚠️)       | 1 (❌)  |
```

**Data Completeness Matrix**:

- Table showing each candidate (rows) vs fields (columns): Name, Email, Phone, CGPA, Branch, Skills, Projects
- Color-coded: Green (present), Yellow (partial), Red (missing)
- Sortable by completeness score

**CSV Match Report** (if CSV provided):

- "Matched 8/10 resumes with college data"
- "2 resumes could not be matched — listed below for manual review"
- Matched data shown with indicators of which fields came from CSV vs resume

**Individual Candidate Cards** (expandable):

- **Side-by-side view**:
  - Left panel: Raw resume text (scrollable, first 500 chars with "show more")
  - Right panel: Extracted structured data in clean format
- Parse confidence indicator (high/medium/low with color)
- "Flag for manual review" checkbox
- For each extracted field: small icon indicating source (📄 resume / 📊 CSV)

**Section 4: Post-Parse Actions**

- "Proceed to Screening →" button (enabled only if parsing complete)
- "Re-parse Failed" button (retries only failed candidates)
- Download parsed data as CSV (for backup/review)

---

### PAGE 3: Screening & Shortlisting — Detailed Feature Spec (THE MONEY PAGE)

**Phase Gate Check**: If parsing not complete, show message + redirect.

**Two-stage process with clear visual separation.**

**STAGE A: Eligibility Filtering (instant, no AI)**

"Apply Eligibility Criteria" button → runs instantly (Python code, no LLM).

**Results Dashboard**:

- Funnel visualization using `st.columns` + custom metric cards:
  ```
  [Total: 500] → [Eligible: 320] → [Filtered Out: 180]
  ```
- Filter Breakdown (horizontal bar chart or metric cards):
  ```
  ❌ CGPA below 7.0:     120 candidates
  ❌ Ineligible branch:    45 candidates
  ❌ Active backlogs:      15 candidates
  ────────────────────────────────────
  ✅ Passed all filters:  320 candidates
  ```
- Each filter category is expandable — shows the list of candidates who failed that specific filter
- "Adjust Criteria" button → opens a modal/expander to change cutoffs and re-run

**STAGE B: AI-Powered Scoring**

"🧠 Run AI Screening" button → triggers LLM scoring with progress tracking.

Progress display during scoring:

```
🧠 AI Screening in progress... (12/320)
Estimated time remaining: ~8 minutes
├── ✅ Candidate 1: Score 8.2 — Tier 1
├── ✅ Candidate 2: Score 6.4 — Tier 2
├── ...
```

**After scoring — The Main Shortlist View:**

**Top Summary Row**:

```
Tier 1 (Strong Match)     | Tier 2 (Partial Match)    | Tier 3 (Weak Match)
🟢 45 candidates           | 🟡 120 candidates          | 🔴 155 candidates
Score ≥ 7.5                | Score 5.5-7.4              | Score < 5.5
```

**Score Distribution Chart**: Histogram or bar chart showing score distribution across all candidates. Visual line markers showing tier boundaries. Evaluator can see the shape of the candidate pool at a glance.

**Tier Tabs**: Three tabs — Tier 1 / Tier 2 / Tier 3

**Within each tab — Candidate Cards**:

Each candidate card contains:

**Card Header**:

- Name, Branch, CGPA — prominent
- Overall score badge (large, color-coded: green/yellow/red)
- Tier badge

**Score Breakdown — Radar/Spider Chart** (using plotly or matplotlib):

- 5 axes: Technical Skills, Project Relevance, Experience, Learning, Communication
- Score values on each axis (1-10)
- Role requirements overlay (dotted line) showing what the ideal candidate looks like
- At a glance shows WHERE the candidate is strong/weak

**Alternative if radar chart is too complex**: Horizontal bar chart per dimension:

```
Technical Skills    ████████░░  8.0/10
Project Relevance   ██████░░░░  6.0/10
Experience          ████░░░░░░  4.0/10
Learning            ███████░░░  7.0/10
Communication       ████████░░  8.0/10
```

**Key Insights** (AI-generated, 2-3 bullets each):

- 💪 Strengths: "Strong Python skills demonstrated through 3 ML projects"
- ⚠️ Concerns: "No internship experience, limited real-world exposure"

**"View Detailed Assessment"** expander:

- Full AI reasoning for each score dimension
- Original skills list, projects, internships extracted from resume

**Tier Override Control**:

- Dropdown: "Move to → Tier 1 / Tier 2 / Tier 3"
- Reason text input (required for override): "Candidate has exceptional hackathon wins not captured in scoring"
- On override: visual indicator showing "Manually adjusted" with the reason

**Shortlist Adjustment Panel** (collapsible, at top of page):

- Tier threshold sliders: adjust where Tier 1/2/3 boundaries fall
- "Preview" button: shows how many candidates move between tiers WITHOUT applying
- "Apply New Thresholds" button: re-classifies all candidates
- Scoring weight adjustment: same 5 sliders from Page 1, but now with "Re-score All" button

**THE APPROVAL GATE** (bottom of page, sticky/prominent):

- Large panel with summary:
  ```
  ┌─────────────────────────────────────────────────┐
  │  SHORTLIST SUMMARY FOR APPROVAL                 │
  │                                                 │
  │  ✅ Shortlisted for Interview:  45 (Tier 1)     │
  │  ⏳ Waitlisted:                 120 (Tier 2)    │
  │  ❌ Not Selected:               155 (Tier 3)    │
  │                                                 │
  │  Manual Overrides Applied: 3                    │
  │                                                 │
  │  [  ✅ APPROVE SHORTLIST  ]                     │
  └─────────────────────────────────────────────────┘
  ```
- On click: confirmation dialog: "This will finalize the shortlist. You can still modify later. Proceed?"
- On approval: success animation, Pages 4 and 5 unlock, sidebar updates

---

### PAGE 4: Candidate Briefs — Detailed Feature Spec

**Phase Gate Check**: If shortlist not approved, show message + redirect.

**Top Controls**:

- "📋 Generate All Briefs" button (generates for all Tier 1 + Tier 2 candidates)
- Progress indicator during generation
- After generation: count badge "45 briefs generated"

**Brief Display**:
Each brief as a clean, professional card:

```
┌──────────────────────────────────────────┐
│  INTERVIEW BRIEF: Rahul Sharma           │
│  Role: Software Engineer | Score: 8.2    │
│  ⏱ Est. read time: ~90 seconds          │
├──────────────────────────────────────────┤
│                                          │
│  📸 PROFILE SNAPSHOT                     │
│  B.Tech CS from IIT Bombay, 8.4 CGPA.   │
│  Strong ML background with 2 internships │
│  at startups. Published research paper.  │
│                                          │
│  💪 STRENGTHS TO EXPLORE                 │
│  • Deep Python/TensorFlow expertise      │
│    → Ask: "Walk me through your CNN      │
│       architecture for the image         │
│       classification project"            │
│  • Real startup experience               │
│    → Ask about scaling challenges faced  │
│                                          │
│  🔍 AREAS TO PROBE                       │
│  • Claims "expert" in Docker but no      │
│    project evidence — verify depth       │
│  • No team project experience listed     │
│    → Probe collaboration skills          │
│                                          │
│  ❓ SUGGESTED QUESTIONS                   │
│  1. [Tailored technical question]        │
│  2. [Project deep-dive question]         │
│  3. [Behavioral/collaboration question]  │
│  4. [Problem-solving question]           │
│                                          │
│  🚩 RED FLAGS                            │
│  • None significant                      │
│                                          │
│  [📥 Download] [📋 Copy to Clipboard]    │
└──────────────────────────────────────────┘
```

**Bulk Actions**:

- "Download All Briefs" → generates a single consolidated document (markdown or text)
- "Download as Interview Pack" → one brief per page, ready to print
- Filter briefs by tier, sort by interview slot or score

---

### PAGE 5: Communications — Detailed Feature Spec

**Phase Gate Check**: If shortlist not approved, show message + redirect.

**Top Controls**:

- Communication mode toggle: "📧 Direct to Students" / "🏫 Through Placement Cell"
- "✉️ Generate All Drafts" button with progress indicator

**FOR "Direct to Students" MODE:**

Three tabs: ✅ Shortlisted | ⏳ Waitlisted | ❌ Not Selected

Each tab shows a list of communication drafts:

**Draft Card**:

```
┌──────────────────────────────────────────┐
│  To: rahul.sharma@iitb.ac.in            │
│  Subject: Interview Invitation — TechCorp│
│  Status: 📝 Draft                        │
├──────────────────────────────────────────┤
│                                          │
│  [Editable text area with AI-generated   │
│   email content. HR can modify before    │
│   approving.]                            │
│                                          │
│  Dear Rahul,                             │
│                                          │
│  Congratulations! We were impressed by   │
│  your profile, particularly your work    │
│  in machine learning...                  │
│                                          │
├──────────────────────────────────────────┤
│  [✅ Approve] [✏️ Reset to Original]     │
└──────────────────────────────────────────┘
```

**Bulk Actions**:

- "Approve All in Tab" button
- "Download All Approved as CSV" (columns: email, subject, body, status)
- Approved count indicator: "32/45 approved"

**FOR "Through Placement Cell" MODE:**

**Summary Table** (the primary deliverable for placement cells):

```
| Roll No    | Name           | Branch | CGPA | Status      | Interview Slot |
|------------|----------------|--------|------|-------------|----------------|
| 2022CS001  | Rahul Sharma   | CS     | 8.4  | Shortlisted | Slot 1 (9 AM)  |
| 2022IT042  | Priya Kumar    | IT     | 7.8  | Shortlisted | Slot 2 (9:30)  |
| 2022EC015  | Amit Verma     | ECE    | 7.2  | Waitlisted  | —              |
| 2022CS089  | Neha Singh     | CS     | 6.9  | Not Selected| —              |
```

- Sortable and filterable
- Color-coded status column
- "Download as CSV" and "Download as Excel" buttons

**Cover Email to Placement Cell**:

- Auto-generated summary email (editable text area):

  ```
  Subject: Campus Drive Results — TechCorp, March 25, 2026

  Dear Placement Cell,

  Thank you for organizing the campus drive at [College].

  Summary:
  - Total resumes reviewed: 500
  - Shortlisted for interview: 45
  - Waitlisted: 120
  - Not proceeding: 335

  Please find the detailed list attached.
  Interview schedule: [date/time]

  Please inform shortlisted candidates to carry...
  ```

**Communication Statistics** (bottom of page):

```
📊 Communication Summary
├── ✅ Shortlisted: 45 — personalized interview invites
├── ⏳ Waitlisted: 120 — status update with timeline
├── ❌ Not Selected: 335 — respectful feedback with encouragement
└── 📧 Total drafts: 500
```

---

### "TRY WITH SAMPLE DATA" Feature — Complete Spec

This is CRITICAL for the evaluator experience. It must work flawlessly.

**What it does**: One button click loads a complete pre-configured demo with:

- Drive config: "TechCorp → IIT Demo Campus" hiring for "Software Engineer" (5 positions)
- Criteria: CGPA ≥ 7.0, CS/IT/ECE branches, skills: Python, SQL, Data Structures
- 8-10 pre-parsed candidate profiles with realistic data (mix of strong/medium/weak)
- Candidates already have parsed profiles in session_state

**After loading**:

- Page 1 shows the pre-filled configuration (view-only with "Edit" option)
- Page 2 shows parsing as already complete with the quality dashboard populated
- Page 3 is ready for screening — evaluator can immediately run AI scoring
- The evaluator is 2 clicks away from seeing the most impressive features

**Sample candidate variety** (pre-built into sample_data/):

- 2-3 strong candidates (Tier 1 material): high CGPA, relevant projects, internships
- 3-4 medium candidates (Tier 2): decent CGPA, some gaps, mixed relevance
- 2-3 weak candidates (Tier 3): below average, irrelevant skills, minimal projects
- 1 edge case: high CGPA but completely wrong branch/skills (tests hard filter)
- 1 edge case: low CGPA but exceptional projects (tests if AI scoring catches potential)

This variety ensures the evaluator sees meaningful differentiation in tiers, interesting edge cases, and the system handling nuanced judgment.

---

## 10. Deployment Strategy

### Streamlit Community Cloud

- Free hosting, shareable URL: `https://your-app-name.streamlit.app`
- Deploy from public GitHub repo
- API keys stored in Streamlit Secrets (dashboard → Settings → Secrets)
- Secrets format (TOML):
  ```toml
  ANTHROPIC_API_KEY = "sk-ant-..."
  ```
- Access in code: `st.secrets["ANTHROPIC_API_KEY"]`
- Auto-deploys on git push
- App sleeps after inactivity, wakes on visit (~30s cold start)

### Deployment Steps

1. Push code to public GitHub repo
2. Go to share.streamlit.io, connect GitHub
3. Select repo, branch, main file (`streamlit_app.py`)
4. Add secrets in settings
5. Deploy → get shareable URL

### Resource Considerations

- Keep memory usage low: don't store all resume texts in session_state permanently
- Process candidates in batches for LLM calls
- Use `st.cache_data` for expensive operations that don't change
- Handle LLM rate limits with retry logic and progress bars

---

## 11. Project File Structure

```
campus-recruit-ai/
│
├── README.md                          ← Comprehensive (see Section 12 for template)
├── requirements.txt
├── streamlit_app.py                   ← Main entry point
│
├── app_pages/
│   ├── 01_drive_setup.py
│   ├── 02_upload_parse.py
│   ├── 03_screening.py
│   ├── 04_briefs.py
│   └── 05_communications.py
│
├── agents/
│   ├── __init__.py
│   ├── orchestrator.py                ← LangGraph state machine definition
│   ├── parser_agent.py                ← Resume parsing logic
│   ├── screening_agent.py             ← Hard filters + AI scoring
│   ├── brief_agent.py                 ← Candidate brief generation
│   └── communication_agent.py         ← Communication draft generation
│
├── core/
│   ├── __init__.py
│   ├── models.py                      ← Pydantic data models
│   ├── prompts.py                     ← All LLM prompts centralized
│   ├── file_handler.py                ← PDF/DOCX text extraction
│   ├── hard_filters.py                ← Deterministic screening logic
│   └── llm_client.py                  ← Anthropic API wrapper with retry
│
├── sample_data/
│   ├── sample_resumes/                ← 5-10 test PDFs
│   ├── college_data.csv               ← Sample college CSV
│   └── sample_jd.json                 ← Sample job description
│
├── docs/
│   ├── SYSTEM_DESIGN.md
│   ├── DATABASE_SCHEMA.md
│   ├── API_DESIGN.md
│   ├── SCALING_STRATEGY.md
│   ├── SECURITY.md
│   └── USER_PERSONAS.md
│
└── .streamlit/
    └── config.toml                    ← Streamlit theme/config
```

---

## 12. Production Vision (Not Implemented — For README)

### Authentication

- Email + password registration → email verification → JWT session
- Managed auth: Supabase Auth or Clerk
- Role-based access: HR_ADMIN, INTERVIEWER, PLACEMENT_CELL
- Row-level security at database layer

### Database (PostgreSQL via Supabase)

- Full relational schema: organizations → users → drives → roles → candidates → screening_results → shortlists → communications → audit_log
- JSONB for flexible fields (parsed_profile, ai_scores, config)
- Why PostgreSQL over MongoDB: relational data with complex joins, JSONB for flexibility
- Why not SQLite: no concurrent write support for multi-user

### File Storage

- Supabase Storage (S3-compatible) with signed URLs
- Structure: /resumes/{drive_id}/{candidate_id}/original.pdf
- Signed URLs expire after configurable time (privacy)
- Max 5MB per file, PDF/DOCX only

### Concurrency

- Optimistic locking for shortlist modifications
- Async job queue for batch AI operations
- Real-time progress via Supabase subscriptions
- Rate limiting for LLM API calls (batched processing)

### API Design

```
POST /drives                          → create drive
POST /drives/:id/upload               → bulk upload
POST /drives/:id/parse                → trigger parsing (async)
POST /drives/:id/screen               → trigger screening (async)
GET  /drives/:id/shortlist            → current shortlist
PATCH /shortlist/:id                  → override tier
POST /drives/:id/shortlist/approve    → bulk approve
POST /drives/:id/briefs/generate      → trigger briefs
POST /drives/:id/communications       → generate drafts
```

### Interview Day Dashboard

- Real-time schedule with status tracking
- Quick candidate brief pull-up
- Interviewer feedback capture (structured form)
- Running selection tally

### Analytics & Bias Detection

- Time-to-shortlist metrics
- Score distribution analysis
- Demographic bias detection (if demographics available)
- Funnel conversion rates

---

## 13. Design Decisions & Trade-offs

| Decision                   | Chosen                                              | Alternative                | Why                                                                       |
| -------------------------- | --------------------------------------------------- | -------------------------- | ------------------------------------------------------------------------- |
| Orchestration              | LangGraph                                           | CrewAI                     | Explicit state control, native HITL support, visible graph for evaluators |
| Hard filters               | Python code                                         | LLM                        | Deterministic accuracy, zero cost, instant execution                      |
| AI screening               | Per-dimension scoring                               | Single overall score       | Explainability, consistency, actionable feedback                          |
| PDF extraction             | pymupdf                                             | pypdf, pdfminer            | Fastest, highest quality, active maintenance                              |
| Resume parsing             | LLM structured output                               | Rule-based NLP             | Handles non-standard formats, creative templates                          |
| Screening approach         | Two-stage (code + AI)                               | Pure AI                    | Code for objective criteria, AI for nuanced judgment                      |
| Bias mitigation            | Blind screening (no name/institution in first pass) | Standard screening         | Ethical, legally safer, shows design awareness                            |
| Communication              | Drafts with human review                            | Auto-send                  | Safety, prevents AI errors from reaching candidates                       |
| Deployment                 | Streamlit Cloud                                     | Netlify + separate backend | Single deploy, Python-native, free, shareable URL                         |
| Database (MVP)             | session_state                                       | SQLite/Supabase            | Fastest to implement, sufficient for single-user demo                     |
| Database (prod)            | PostgreSQL                                          | MongoDB                    | Relational data, JSONB flexibility, complex queries                       |
| File storage (prod)        | Object storage (Supabase)                           | Database BLOBs             | Performance, scalability, signed URL security                             |
| Auth method                | Email + password                                    | Phone OTP                  | No SMS gateway cost, standard for B2B enterprise                          |
| Candidate comms            | Through placement cell option                       | Direct only                | Reflects real campus placement protocol                                   |
| Brief length               | 300 words max                                       | Full report                | Interviewer time constraint (3 min between interviews)                    |
| Fresh graduate calibration | Explicit in prompt                                  | Generic scoring            | Prevents unfairly low scores for campus candidates                        |

---

## 14. Implementation Checklist

### Priority 1 (Must Have for Demo)

- [ ] Project structure & requirements.txt
- [ ] streamlit_app.py with navigation
- [ ] Pydantic models (core/models.py)
- [ ] LLM client with retry logic (core/llm_client.py)
- [ ] All prompts centralized (core/prompts.py)
- [ ] File extraction: PDF + DOCX (core/file_handler.py)
- [ ] Page 1: Drive setup form
- [ ] Page 2: Upload + parse resumes + quality dashboard
- [ ] Hard filters (core/hard_filters.py)
- [ ] Page 3: Screening with tier display + approve button
- [ ] Page 4: Brief generation + display
- [ ] Page 5: Communication drafts + review
- [ ] Sample test data (5-10 PDFs + CSV)
- [ ] Deploy to Streamlit Cloud

### Priority 2 (Nice to Have)

- [ ] LangGraph orchestrator definition (even if UI drives flow)
- [ ] Download briefs as consolidated document
- [ ] Download communications as CSV
- [ ] Batch progress bars for LLM operations
- [ ] Score distribution visualizations (charts)
- [ ] Override tier with reason logging

### Priority 3 (Documentation Only)

- [ ] README with full architecture
- [ ] docs/SYSTEM_DESIGN.md
- [ ] docs/DATABASE_SCHEMA.md
- [ ] docs/API_DESIGN.md
- [ ] docs/SCALING_STRATEGY.md
- [ ] docs/SECURITY.md
- [ ] docs/USER_PERSONAS.md

---

## Key Principles (for evaluators)

1. **AI where it adds value, code where it doesn't** — don't LLM a CGPA check
2. **Human-in-the-loop at every irreversible decision** — AI recommends, humans decide
3. **Domain-aware design** — understands campus placement (placement cell, college cutoffs, batch processing)
4. **User empathy across ALL stakeholders** — HR, interviewers, placement cell, AND candidates
5. **Transparency and auditability** — every AI score has a breakdown, every decision is logged
6. **Graceful degradation** — failed parses flagged, not silently dropped
7. **Blind screening** — names/institutions hidden in first scoring pass for fairness
