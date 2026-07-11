"""
Database seed script — Populates the database with demo data for all modules.

Usage:
    python -m src.scripts.seed_data

Creates:
    - Admin user + sample employees
    - Department structure
    - Leave balances and sample requests
    - Attendance records
    - Payroll records
    - Job postings and candidates
    - Performance goals and reviews
    - Training courses
    - Compliance policies
"""

from __future__ import annotations

import asyncio
import hashlib
import logging
import uuid
from datetime import date, datetime, time, timedelta
from decimal import Decimal

logger = logging.getLogger(__name__)

# ── Demo Data ────────────────────────────────────────────────

DEPARTMENTS = [
    {"name": "Engineering", "code": "ENG", "head": "Rajesh Kumar"},
    {"name": "Product", "code": "PROD", "head": "Priya Menon"},
    {"name": "Data Science", "code": "DS", "head": "Anil Sharma"},
    {"name": "Design", "code": "DES", "head": "Sneha Nair"},
    {"name": "Marketing", "code": "MKT", "head": "Kavita Mehta"},
    {"name": "Sales", "code": "SAL", "head": "Rohit Singh"},
    {"name": "Human Resources", "code": "HR", "head": "Deepa Iyer"},
    {"name": "Finance", "code": "FIN", "head": "Amit Gupta"},
    {"name": "QA", "code": "QA", "head": "Suresh Babu"},
    {"name": "Operations", "code": "OPS", "head": "Neha Verma"},
]

EMPLOYEES = [
    {"name": "Rajesh Kumar", "email": "rajesh.kumar@hrcopilot.io", "role": "admin", "designation": "VP Engineering", "department": "Engineering", "salary": 250000},
    {"name": "Priya Menon", "email": "priya.menon@hrcopilot.io", "role": "hr_manager", "designation": "Director of Product", "department": "Product", "salary": 220000},
    {"name": "Arjun Sharma", "email": "arjun.sharma@hrcopilot.io", "role": "employee", "designation": "Senior Software Engineer", "department": "Engineering", "salary": 120000},
    {"name": "Deepak Verma", "email": "deepak.verma@hrcopilot.io", "role": "employee", "designation": "ML Engineer", "department": "Data Science", "salary": 135000},
    {"name": "Sneha Nair", "email": "sneha.nair@hrcopilot.io", "role": "employee", "designation": "Lead Designer", "department": "Design", "salary": 110000},
    {"name": "Rohit Singh", "email": "rohit.singh@hrcopilot.io", "role": "manager", "designation": "DevOps Lead", "department": "Engineering", "salary": 140000},
    {"name": "Kavita Mehta", "email": "kavita.mehta@hrcopilot.io", "role": "employee", "designation": "Marketing Manager", "department": "Marketing", "salary": 95000},
    {"name": "Amit Gupta", "email": "amit.gupta@hrcopilot.io", "role": "employee", "designation": "Finance Analyst", "department": "Finance", "salary": 85000},
    {"name": "Swati Reddy", "email": "swati.reddy@hrcopilot.io", "role": "employee", "designation": "QA Engineer", "department": "QA", "salary": 78000},
    {"name": "Rahul Joshi", "email": "rahul.joshi@hrcopilot.io", "role": "employee", "designation": "Sales Executive", "department": "Sales", "salary": 72000},
    {"name": "Neha Verma", "email": "neha.verma@hrcopilot.io", "role": "manager", "designation": "Operations Manager", "department": "Operations", "salary": 105000},
    {"name": "Vikram Patel", "email": "vikram.patel@hrcopilot.io", "role": "employee", "designation": "Full Stack Developer", "department": "Engineering", "salary": 95000},
    {"name": "Ananya Das", "email": "ananya.das@hrcopilot.io", "role": "employee", "designation": "Data Analyst", "department": "Data Science", "salary": 82000},
    {"name": "Kiran Bhat", "email": "kiran.bhat@hrcopilot.io", "role": "employee", "designation": "UI Developer", "department": "Design", "salary": 88000},
    {"name": "Sanjay Mishra", "email": "sanjay.mishra@hrcopilot.io", "role": "employee", "designation": "Backend Engineer", "department": "Engineering", "salary": 105000},
]

JOB_POSTINGS = [
    {"title": "Senior React Developer", "department": "Engineering", "experience": "4-7 years", "skills": ["React", "TypeScript", "Next.js", "REST APIs"], "positions": 2, "status": "active"},
    {"title": "ML Ops Engineer", "department": "Data Science", "experience": "3-5 years", "skills": ["Python", "MLflow", "Kubernetes", "Docker"], "positions": 1, "status": "active"},
    {"title": "Product Designer", "department": "Design", "experience": "2-4 years", "skills": ["Figma", "User Research", "Design Systems", "Prototyping"], "positions": 1, "status": "active"},
    {"title": "Technical Content Writer", "department": "Marketing", "experience": "1-3 years", "skills": ["Technical Writing", "SEO", "Developer Docs"], "positions": 1, "status": "active"},
    {"title": "DevOps Engineer", "department": "Engineering", "experience": "3-6 years", "skills": ["AWS", "Terraform", "CI/CD", "Kubernetes"], "positions": 2, "status": "active"},
]

TRAINING_COURSES = [
    {"title": "Advanced Python for Engineers", "category": "Technical", "duration": "20 hours", "provider": "Internal", "mode": "Online"},
    {"title": "Leadership Fundamentals", "category": "Soft Skills", "duration": "8 hours", "provider": "External - Coursera", "mode": "Online"},
    {"title": "AWS Solutions Architect Prep", "category": "Certification", "duration": "40 hours", "provider": "AWS Training", "mode": "Hybrid"},
    {"title": "Data Privacy & GDPR Compliance", "category": "Compliance", "duration": "4 hours", "provider": "Internal", "mode": "Online"},
    {"title": "Effective Communication Workshop", "category": "Soft Skills", "duration": "6 hours", "provider": "Internal", "mode": "In-Person"},
    {"title": "React & Next.js Masterclass", "category": "Technical", "duration": "30 hours", "provider": "Frontend Masters", "mode": "Online"},
    {"title": "POSH Awareness Training", "category": "Compliance", "duration": "2 hours", "provider": "Internal", "mode": "Online"},
]


def generate_seed_summary() -> dict:
    """Generate a summary of seed data without requiring a database connection."""
    return {
        "departments": len(DEPARTMENTS),
        "employees": len(EMPLOYEES),
        "job_postings": len(JOB_POSTINGS),
        "training_courses": len(TRAINING_COURSES),
        "admin_credentials": {
            "email": "rajesh.kumar@hrcopilot.io",
            "password": "admin123",
            "note": "Change this immediately in production",
        },
        "demo_user": {
            "email": "arjun.sharma@hrcopilot.io",
            "password": "demo123",
        },
    }


if __name__ == "__main__":
    import json
    summary = generate_seed_summary()
    print("=" * 60)
    print("  HR Copilot — Seed Data Summary")
    print("=" * 60)
    print(json.dumps(summary, indent=2))
    print("\nTo seed the database, start the application and call:")
    print("  POST /api/v1/seed")
    print("=" * 60)
