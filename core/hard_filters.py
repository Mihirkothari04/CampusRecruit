from core.models import Candidate, DriveConfig

def normalize_cgpa(val, scale, target_scale="10"):
    if not val:
        return 0.0
    
    val = float(val)
    if scale == "10" and target_scale == "10":
        return val
    elif scale == "4" and target_scale == "10":
        return (val / 4.0) * 10.0
    elif scale == "percentage" and target_scale == "10":
        return val / 9.5  # standard conversion used in some Indian universities
    elif not scale and val <= 10.0:
        return val
    elif not scale and val <= 100.0:
        return val / 9.5
    return val

def apply_hard_filters(candidate: Candidate, config: DriveConfig):
    results = {}
    passed = True

    # CGPA check
    if hasattr(candidate.profile, 'education') and candidate.profile.education:
        cgpa = normalize_cgpa(
            candidate.profile.education.cgpa_or_percentage,
            candidate.profile.education.scale,
            config.roles[0].cgpa_scale if config.roles else "10"
        )
        min_cgpa = config.roles[0].min_cgpa if config.roles else 0.0
        
        results["cgpa"] = {
            "passed": cgpa >= min_cgpa, 
            "value": cgpa, 
            "required": min_cgpa
        }
        if not results["cgpa"]["passed"]:
            passed = False
    else:
        results["cgpa"] = {"passed": False, "value": None, "required": config.roles[0].min_cgpa if config.roles else 0.0}
        passed = False

    # Branch check
    allowed_branches = config.roles[0].allowed_branches if config.roles else []
    if allowed_branches:
        if hasattr(candidate.profile, 'education') and candidate.profile.education and candidate.profile.education.branch:
            branch_match = any(
                b.lower() in candidate.profile.education.branch.lower()
                for b in allowed_branches
            )
            results["branch"] = {"passed": branch_match, "value": candidate.profile.education.branch}
            if not results["branch"]["passed"]:
                passed = False
        else:
            results["branch"] = {"passed": False, "value": None}
            passed = False
    else:
        results["branch"] = {"passed": True, "value": "Any"}

    return passed, results
