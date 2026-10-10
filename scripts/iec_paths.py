#!/usr/bin/env python3
"""
Central path definitions for IUS Engineering Club Desktop synchronization.
All club-related documents, forms, exports, and assets reside in C:\\Users\\Kaan\\Desktop\\IEC.
"""

import os
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
DESKTOP_DIR = Path(os.environ.get("USERPROFILE", r"C:\Users\Kaan")) / "Desktop"
DESKTOP_IEC_DIR = DESKTOP_DIR / "IEC"

# Key official file paths
FORM_F252_DOCX = DESKTOP_IEC_DIR / "student_club_registration_form_f252.docx"
DEANERY_PROPOSAL_PDF = DESKTOP_IEC_DIR / "IUS_Engineering_Club_Deanery_Proposal.pdf"
LINKEDIN_GUIDE_DOCX = DESKTOP_IEC_DIR / "IUS_Engineering_Club_LinkedIn_Rehberi.docx"
LINKEDIN_IMAGES_DIR = DESKTOP_IEC_DIR / "LinkedIn_Gorselleri"

def ensure_iec_dir() -> Path:
    """Ensure the Desktop\\IEC directory exists."""
    DESKTOP_IEC_DIR.mkdir(parents=True, exist_ok=True)
    return DESKTOP_IEC_DIR

def get_iec_path(*subpaths: str) -> Path:
    """Return a path inside Desktop\\IEC, ensuring its parent directory exists."""
    ensure_iec_dir()
    target = DESKTOP_IEC_DIR.joinpath(*subpaths)
    target.parent.mkdir(parents=True, exist_ok=True)
    return target
