from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

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

class DriveConfig(BaseModel):
    company_name: str
    college_name: str
    drive_date: str
    roles: List[RoleConfig]

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

class ScoreDetail(BaseModel):
    score: int
    reasoning: str

class ScreeningScores(BaseModel):
    technical_skills: ScoreDetail
    project_relevance: ScoreDetail
    practical_experience: ScoreDetail
    learning_trajectory: ScoreDetail
    communication_indicators: ScoreDetail
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
    """LangGraph state object equivalent model (if needed outside)"""
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
