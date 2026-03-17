from core.models import TierEnum

# Dummy candidates to use for the demo "Try with Sample Data" feature.
MOCK_CANDIDATES_DATA = [
    {
        "id": "cand_1",
        "file_name": "rahul_sharma_resume.pdf",
        "raw_text": "Rahul Sharma\nEmail: rahul.s@example.com\nPhone: 9876543210\nB.Tech CS IIT Bombay 8.4 CGPA\nSkills: Python, TensorFlow, SQL\nProjects: Image Classification using CNN",
        "profile": {
            "name": "Rahul Sharma",
            "email": "rahul.s@example.com",
            "phone": "9876543210",
            "roll_number": "2022CS001",
            "education": {
                "degree": "B.Tech",
                "branch": "Computer Science",
                "institution": "IIT Bombay",
                "cgpa_or_percentage": 8.4,
                "scale": "10",
                "graduation_year": 2026
            },
            "programming_languages": ["Python", "SQL"],
            "frameworks_and_tools": ["TensorFlow"],
            "projects": [
                {"title": "Image Classification", "description": "Built CNN model", "technologies_used": ["Python", "TensorFlow"]}
            ],
            "internships": [
                {"company": "AI Startup", "role": "ML Intern", "duration": "3 months", "description": "Developed predictive models."}
            ]
        },
        "parsing_confidence": 0.95,
        "parsing_errors": []
    },
    {
        "id": "cand_2",
        "file_name": "priya_kumar_cv.pdf",
        "raw_text": "Priya Kumar\npriyaku@example.com\nIT Branch, 7.8 CGPA\nSkills: Java, React",
        "profile": {
            "name": "Priya Kumar",
            "email": "priyaku@example.com",
            "roll_number": "2022IT042",
            "education": {
                "degree": "B.Tech",
                "branch": "Information Technology",
                "institution": "NIT Trichy",
                "cgpa_or_percentage": 7.8,
                "scale": "10",
                "graduation_year": 2026
            },
            "programming_languages": ["Java", "JavaScript"],
            "frameworks_and_tools": ["React"],
            "projects": [
                {"title": "E-commerce Website", "description": "Frontend with React", "technologies_used": ["React", "JavaScript"]}
            ],
            "internships": []
        },
        "parsing_confidence": 0.90,
        "parsing_errors": []
    },
    {
        "id": "cand_3",
        "file_name": "neha_singh.docx",
        "raw_text": "Neha Singh\nCS, 6.9 CGPA\nSkills: C++, HTML\nProjects: Library Management System",
        "profile": {
            "name": "Neha Singh",
            "email": "neha@example.com",
            "roll_number": "2022CS089",
            "education": {
                "degree": "B.Tech",
                "branch": "Computer Science",
                "institution": "Local College",
                "cgpa_or_percentage": 6.9,
                "scale": "10",
                "graduation_year": 2026
            },
            "programming_languages": ["C++", "HTML"],
            "frameworks_and_tools": [],
            "projects": [
                {"title": "Library Management", "description": "Basic CRUD", "technologies_used": ["C++"]}
            ],
            "internships": []
        },
        "parsing_confidence": 0.85,
        "parsing_errors": []
    }
]

def get_demo_drive_config():
    from core.models import DriveConfig, RoleConfig
    return DriveConfig(
        company_name="TechCorp",
        college_name="IIT Demo Campus",
        drive_date="2026-03-25",
        roles=[
            RoleConfig(
                title="Software Engineer",
                department="Engineering",
                positions_available=5,
                min_cgpa=7.0,
                cgpa_scale="10",
                allowed_branches=["Computer Science", "Information Technology", "Electronics"],
                max_backlogs=0,
                required_skills=["Python", "SQL", "Data Structures"],
                preferred_skills=["React", "TensorFlow"],
                criteria_weights={
                    "technical_skills": 0.25,
                    "project_relevance": 0.25,
                    "practical_experience": 0.20,
                    "learning_trajectory": 0.15,
                    "communication_indicators": 0.15
                }
            )
        ]
    )
