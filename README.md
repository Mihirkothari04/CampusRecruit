<p align="center">
  <img src="https://img.shields.io/badge/AI-Agentic_Recruitment-0F172A?style=for-the-badge&logo=openai&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-MVP-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/LangGraph-Orchestration-4B0082?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/FastAPI-Extended_System-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
</p>

# 🎓 CampusRecruit AI

### Agentic AI-Powered Internal HR Tool for Campus Placement Drives
Access it Live here "https://campusrecruit.streamlit.app/"
> Automates the entire campus recruitment pipeline — from resume dump to personalized candidate communication — while keeping humans in control of final decisions.

---

# 📌 Table of Contents

- [Problem Statement](#-problem-statement)
- [Scope & Constraints](#-scope--constraints)
- [User Personas](#-user-personas)
- [System Architecture](#-system-architecture)
- [Agent Pipeline](#-agent-pipeline-design)
- [Tech Stack](#-tech-stack)
- [Data Models](#-data-models)
- [Screening Logic](#-screening-logic)
- [AI Prompt Design](#-ai-prompt-design)
- [Features Implemented (MVP)](#-features-implemented-mvp)
- [Extended System (If Given More Time)](#-extended-system-if-given-more-time)
- [Production Vision](#-production-vision)
- [How to Run](#-how-to-run)
- [Project Structure](#-project-structure)
- [Design Decisions](#-design-decisions--trade-offs)

---

# 📋 Problem Statement

Campus placement drives are compressed, high-pressure events:

- 300–800 resumes received in bulk
- Manual filtering leads to inconsistency and fatigue
- Interviewers lack structured candidate context
- Students receive delayed or no communication

**Goal:** Build an **agentic AI system** that automates the pipeline while ensuring:

- Fairness (blind evaluation)
- Speed (minutes instead of hours)
- Explainability (why candidates were selected/rejected)
- Human control (approval gates)

---

# ⏱ Scope & Constraints

- ⏳ **Time Constraint**: 3-hour MVP build
- 🚀 **Deployment Required**: Streamlit Cloud (non-technical evaluators)
- 🧠 Focus: System Design > Code completeness
- 📌 Must clearly show **what was built vs what was intended**

---

# 👥 User Personas

### 🧑‍💼 HR Recruiter

- Filters 300–800 resumes overnight
- Needs fast, explainable shortlist

### 🧑‍💻 Interview Panel

- Gets resumes minutes before interview
- Needs structured candidate briefs

### 🏫 Placement Cell

- Coordinates between company and students
- Needs visibility and communication tools

### 🎓 Student Candidate

- Wants fair evaluation and timely updates

---

# 🏗 System Architecture

## ✅ 1. MVP Architecture (FINAL — Implemented)

```
Streamlit App (single user, Streamlit Cloud)
│
├── Page 1: Drive Setup
├── Page 2: Upload & Parse
├── Page 3: Screening
├── Page 4: Candidate Briefs
└── Page 5: Communication Drafts

Backend: Python + LangGraph agent orchestration
State: st.session_state + SQLite
AI: OpenAI GPT-5.2/5.3
File handling: pymupdf + python-docx
Deploy: Streamlit Community Cloud
```

---

## 🔁 2. Extended System (If Given More Time)

> This architecture represents a **scalable full-stack implementation** beyond MVP constraints.

```
Frontend: React 19 + Tailwind + shadcn/ui
Backend: FastAPI (async Python APIs)
Database: MongoDB
AI: OpenAI GPT-4o (structured JSON mode)
Auth: JWT-based authentication

Pipeline exposed via REST APIs instead of direct LangGraph execution.
```

**Why this exists:**

- Streamlit is ideal for rapid MVP
- FastAPI + React enables:
  - Multi-user support
  - Scalability
  - Production deployment readiness

---

## 🧠 3. Production Architecture (Designed, Not Implemented)

```
Orchestrator Agent (LangGraph State Machine)
│
├── Intake Agent
├── Parser Agent
├── Data Quality Agent
├── Screening Agent
│     ├── Hard Filters
│     └── AI Ranking
├── Human Approval Gate
├── Brief Generation Agent
├── Communication Agent
└── Scheduler Agent

Shared State:
PostgreSQL (JSONB) + Object Storage + Audit Logs + RBAC
```

---

## 🧩 Why Multiple Architectures?

| Layer           | Purpose                           |
| --------------- | --------------------------------- |
| MVP (Streamlit) | Rapid prototype for evaluation    |
| Extended System | Demonstrates scalable engineering |
| Production      | Ideal agentic architecture        |

---

# 🤖 Agent Pipeline Design

```
Resume Upload
      ↓
File Extraction (PDF/DOCX)
      ↓
AI Resume Parsing (Structured JSON)
      ↓
Hard Filters (Deterministic)
      ↓
AI Scoring (5 Dimensions)
      ↓
🚨 Human Approval Gate
      ↓
Candidate Brief Generation
      ↓
Communication Draft Generation
```

---

# 🛠 Tech Stack

### MVP

- Streamlit
- LangGraph
- OpenAI GPT-5.2/5.3
- PyMuPDF + python-docx
- SQLite / Session State

### Extended

- React 19 + Tailwind
- FastAPI (async)
- MongoDB
- JWT Auth

---

# 📊 Data Models (Simplified)

### Candidate

```
Candidate
├── profile (education, skills, projects)
├── parsing_confidence
├── hard_filter_passed
├── ai_scores (5 dimensions)
├── tier (1 / 2 / 3)
├── candidate_brief
└── communication_draft
```

---

# 🔍 Screening Logic

## Stage A: Hard Filters (Code, No AI)

- CGPA normalization
- Branch eligibility
- Skills threshold

✔ Deterministic
✔ Instant
✔ Zero cost

---

## Stage B: AI Scoring (LLM)

Dimensions:

- Technical Skills
- Project Relevance
- Practical Experience
- Learning Trajectory
- Communication

---

### Tier Classification

| Tier   | Score   | Action    |
| ------ | ------- | --------- |
| TIER 1 | ≥ 7.5   | Interview |
| TIER 2 | 5.5–7.4 | Waitlist  |
| TIER 3 | < 5.5   | Reject    |

---

# 🧠 AI Prompt Design

### Key Principles

- **Structured JSON outputs** → no parsing failures
- **Blind evaluation** → removes bias
- **Fresh graduate calibration**
- **Concise outputs** → interviewer-friendly

---

# ✅ Features Implemented (MVP)

- Drive setup with criteria configuration
- Resume upload (PDF/DOCX)
- AI resume parsing
- Deterministic filtering
- AI scoring + tier classification
- Human-in-the-loop approval
- Candidate brief generation
- Communication drafts

---

# 🚀 Extended System (If Given More Time)

- Multi-user authentication
- Role-based access (HR / Interviewer / Placement Cell)
- Real-time dashboards
- Resume storage (S3)
- Async job queues
- WebSocket updates
- Advanced analytics

---

# 🔮 Production Vision

- LangGraph orchestration
- Interrupt-based human approval
- PostgreSQL + JSONB
- Bias detection engine
- Interview day dashboard
- Audit logging system

---

# ▶️ How to Run (MVP)

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

---

# 📁 Project Structure

```
streamlit_app.py
app_pages/
  ├── 01_drive_setup.py
  ├── 02_upload_parse.py
  ├── 03_screening.py
  ├── 04_briefs.py
  └── 05_communications.py
backend/
  ├── models.py
  ├── prompts.py
  ├── llm_client.py
  └── utils/
```

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

---

# ⚖️ Design Decisions & Trade-offs

| Decision               | Why                          |
| ---------------------- | ---------------------------- |
| Hard filters in Python | Deterministic, fast, no cost |
| AI for scoring only    | Where judgment is needed     |
| Blind screening        | Reduces bias                 |
| Human approval gate    | Prevents over-automation     |
| Streamlit for MVP      | Fastest deployable UI        |
| FastAPI (extended)     | Scalability                  |

---

# 🎯 Key Takeaways

- Separation of **logic vs intelligence**
- Strong **human-in-the-loop design**
- Clear **architecture evolution path**
- Built for **real-world constraints, not theory**

---

# 🏁 Conclusion

CampusRecruit AI is not just a tool — it's a **system design demonstration of agentic AI applied to real-world workflows**, balancing:

- Automation
- Explainability
- Human control

---
