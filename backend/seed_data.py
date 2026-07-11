"""
Comprehensive seed data for the HR Copilot system.

Generates realistic Indian HR data including:
- Users with different roles
- Departments and designations
- 50+ employees with full profiles
- Leave types and balances
- Shifts and attendance
- Job postings and candidates
- Salary structures
- Performance goals
- Training courses
- Compliance policies
- Holidays (Indian calendar)
"""

import asyncio
import random
import uuid
from datetime import date, datetime, time, timedelta, timezone
from decimal import Decimal

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import async_session_factory, engine, Base
from src.core.security import UserRole, hash_password

# ── Import all models ────────────────────────────────────────
from src.auth.models import User, Role, Permission, AuditLog
from src.employees.models import (
    Department, Designation, Employee, EmployeeDocument,
    EmployeeSkill, EmergencyContact, EmployeeTimeline,
)
from src.leaves.models import LeaveType, LeaveBalance, LeaveRequest, Holiday
from src.attendance.models import Shift, ShiftAssignment, AttendanceRecord
from src.recruitment.models import JobPosting, Candidate, CandidateResume, Interview, InterviewFeedback
from src.payroll.models import SalaryStructure, PayrollRun, Payslip, TaxDeclaration
from src.performance.models import PerformanceGoal, PerformanceReview, ReviewFeedback
from src.training.models import TrainingCourse, LearningPath, LearningPathCourse, CourseEnrollment
from src.compliance.models import CompliancePolicy, PolicyAcknowledgment, Notification

# ── Data Pools ───────────────────────────────────────────────
FIRST_NAMES_MALE = [
    "Arjun", "Vikram", "Rahul", "Amit", "Suresh", "Rajesh", "Karan", "Rohit",
    "Deepak", "Manish", "Anil", "Sanjay", "Nikhil", "Pranav", "Gaurav",
    "Ravi", "Ashish", "Vivek", "Harsh", "Abhishek", "Sameer", "Tarun",
    "Naveen", "Pankaj", "Sachin",
]

FIRST_NAMES_FEMALE = [
    "Priya", "Sneha", "Ananya", "Kavita", "Ritu", "Meera", "Pooja", "Neha",
    "Divya", "Shruti", "Swati", "Anjali", "Pallavi", "Nisha", "Aarti",
    "Tanvi", "Ishita", "Sonal", "Megha", "Radhika", "Simran", "Komal",
    "Aditi", "Bhavna", "Nikita",
]

LAST_NAMES = [
    "Sharma", "Verma", "Patel", "Singh", "Kumar", "Gupta", "Mehta",
    "Joshi", "Reddy", "Iyer", "Nair", "Pillai", "Desai", "Shah",
    "Chauhan", "Yadav", "Thakur", "Saxena", "Agarwal", "Mishra",
    "Rao", "Dutta", "Chopra", "Malhotra", "Kapoor",
]

CITIES = [
    "Bangalore", "Mumbai", "Delhi", "Hyderabad", "Pune",
    "Chennai", "Kolkata", "Gurgaon", "Noida", "Ahmedabad",
]

SKILLS_POOL = [
    "Python", "JavaScript", "TypeScript", "React", "Next.js", "Node.js",
    "FastAPI", "Django", "PostgreSQL", "MongoDB", "Redis", "Docker",
    "Kubernetes", "AWS", "Azure", "GCP", "Machine Learning", "Deep Learning",
    "NLP", "Computer Vision", "Data Engineering", "SQL", "GraphQL",
    "REST APIs", "Microservices", "CI/CD", "Git", "Agile", "Scrum",
    "Product Management", "UI/UX Design", "Figma", "Leadership",
    "Communication", "Problem Solving", "Project Management",
    "DevOps", "Terraform", "Java", "Go", "Rust", "C++",
]

BLOOD_GROUPS = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]

DEPARTMENTS_DATA = [
    {"name": "Engineering", "code": "ENG", "color": "#6366f1"},
    {"name": "Product", "code": "PRD", "color": "#8b5cf6"},
    {"name": "Design", "code": "DES", "color": "#ec4899"},
    {"name": "Marketing", "code": "MKT", "color": "#f97316"},
    {"name": "Sales", "code": "SLS", "color": "#22c55e"},
    {"name": "Human Resources", "code": "HR", "color": "#06b6d4"},
    {"name": "Finance", "code": "FIN", "color": "#eab308"},
    {"name": "Operations", "code": "OPS", "color": "#64748b"},
    {"name": "Data Science", "code": "DS", "color": "#a855f7"},
    {"name": "Quality Assurance", "code": "QA", "color": "#14b8a6"},
]

DESIGNATIONS_DATA = [
    {"title": "Software Engineer", "level": 2},
    {"title": "Senior Software Engineer", "level": 3},
    {"title": "Staff Engineer", "level": 4},
    {"title": "Principal Engineer", "level": 5},
    {"title": "Engineering Manager", "level": 5},
    {"title": "Senior Engineering Manager", "level": 6},
    {"title": "Director of Engineering", "level": 7},
    {"title": "VP Engineering", "level": 8},
    {"title": "CTO", "level": 10},
    {"title": "Product Manager", "level": 4},
    {"title": "Senior Product Manager", "level": 5},
    {"title": "Lead Designer", "level": 4},
    {"title": "UX Researcher", "level": 3},
    {"title": "Data Scientist", "level": 3},
    {"title": "Senior Data Scientist", "level": 4},
    {"title": "ML Engineer", "level": 4},
    {"title": "DevOps Engineer", "level": 3},
    {"title": "QA Engineer", "level": 2},
    {"title": "Senior QA Engineer", "level": 3},
    {"title": "HR Manager", "level": 5},
    {"title": "HR Executive", "level": 2},
    {"title": "Recruiter", "level": 3},
    {"title": "Finance Manager", "level": 5},
    {"title": "Accountant", "level": 2},
    {"title": "Marketing Manager", "level": 5},
    {"title": "Content Writer", "level": 2},
    {"title": "Sales Executive", "level": 2},
    {"title": "Business Analyst", "level": 3},
    {"title": "Project Manager", "level": 4},
    {"title": "Intern", "level": 1},
]

LEAVE_TYPES_DATA = [
    {"name": "Casual Leave", "code": "CL", "max_days": 12, "paid": True, "carry": False, "color": "#6366f1"},
    {"name": "Sick Leave", "code": "SL", "max_days": 12, "paid": True, "carry": False, "color": "#ef4444"},
    {"name": "Privilege Leave", "code": "PL", "max_days": 15, "paid": True, "carry": True, "max_carry": 30, "color": "#22c55e"},
    {"name": "Maternity Leave", "code": "ML", "max_days": 182, "paid": True, "carry": False, "color": "#ec4899"},
    {"name": "Paternity Leave", "code": "PTL", "max_days": 15, "paid": True, "carry": False, "color": "#3b82f6"},
    {"name": "Comp Off", "code": "CO", "max_days": 5, "paid": True, "carry": False, "color": "#f59e0b"},
    {"name": "Loss of Pay", "code": "LOP", "max_days": 365, "paid": False, "carry": False, "color": "#94a3b8"},
    {"name": "Work From Home", "code": "WFH", "max_days": 60, "paid": True, "carry": False, "color": "#8b5cf6"},
]

HOLIDAYS_2026 = [
    {"name": "Republic Day", "date": "2026-01-26", "type": "public"},
    {"name": "Maha Shivaratri", "date": "2026-02-27", "type": "restricted"},
    {"name": "Holi", "date": "2026-03-14", "type": "public"},
    {"name": "Good Friday", "date": "2026-04-03", "type": "public"},
    {"name": "Ram Navami", "date": "2026-04-04", "type": "restricted"},
    {"name": "Eid ul-Fitr", "date": "2026-04-21", "type": "public"},
    {"name": "May Day", "date": "2026-05-01", "type": "public"},
    {"name": "Buddha Purnima", "date": "2026-05-12", "type": "restricted"},
    {"name": "Eid ul-Adha", "date": "2026-06-27", "type": "restricted"},
    {"name": "Independence Day", "date": "2026-08-15", "type": "public"},
    {"name": "Janmashtami", "date": "2026-08-25", "type": "restricted"},
    {"name": "Gandhi Jayanti", "date": "2026-10-02", "type": "public"},
    {"name": "Dussehra", "date": "2026-10-12", "type": "public"},
    {"name": "Diwali", "date": "2026-10-31", "type": "public"},
    {"name": "Guru Nanak Jayanti", "date": "2026-11-19", "type": "restricted"},
    {"name": "Christmas", "date": "2026-12-25", "type": "public"},
]

TRAINING_COURSES_DATA = [
    {"title": "Advanced Python Programming", "category": "Technical", "hours": 40, "level": "intermediate"},
    {"title": "React & Next.js Masterclass", "category": "Technical", "hours": 60, "level": "intermediate"},
    {"title": "System Design Fundamentals", "category": "Technical", "hours": 30, "level": "advanced"},
    {"title": "Machine Learning with Python", "category": "Technical", "hours": 80, "level": "advanced"},
    {"title": "Docker & Kubernetes", "category": "DevOps", "hours": 40, "level": "intermediate"},
    {"title": "AWS Cloud Practitioner", "category": "Cloud", "hours": 30, "level": "beginner"},
    {"title": "Leadership Development", "category": "Soft Skills", "hours": 20, "level": "intermediate"},
    {"title": "Effective Communication", "category": "Soft Skills", "hours": 15, "level": "beginner"},
    {"title": "Agile & Scrum Mastery", "category": "Process", "hours": 20, "level": "intermediate"},
    {"title": "Data Engineering Pipeline", "category": "Technical", "hours": 50, "level": "advanced"},
    {"title": "Cybersecurity Fundamentals", "category": "Security", "hours": 25, "level": "beginner"},
    {"title": "Product Management 101", "category": "Business", "hours": 30, "level": "beginner"},
]

POLICIES_DATA = [
    {"title": "Leave Policy", "category": "HR", "content": "All employees are entitled to leaves as per the company leave policy. Casual Leave: 12 days, Sick Leave: 12 days, Privilege Leave: 15 days per calendar year. Leave must be applied in advance (minimum 3 days for planned leave). Sick leave beyond 3 consecutive days requires a medical certificate. Sandwich policy applies to casual leaves taken adjacent to weekends/holidays."},
    {"title": "Code of Conduct", "category": "Compliance", "content": "All employees must maintain professional conduct at all times. This includes treating colleagues with respect, maintaining confidentiality of company information, avoiding conflicts of interest, and adhering to all company policies. Violations may result in disciplinary action up to and including termination."},
    {"title": "Work From Home Policy", "category": "HR", "content": "Employees may work from home up to 60 days per year with prior approval from their reporting manager. WFH requests must be submitted at least 1 day in advance. Employees must be available during core hours (10 AM - 6 PM IST) and attend all scheduled meetings."},
    {"title": "Anti-Harassment Policy", "category": "Compliance", "content": "The company maintains zero tolerance for any form of harassment including sexual harassment, bullying, discrimination, and retaliation. All complaints will be investigated promptly and confidentially. Employees can report incidents through the POSH committee or the anonymous grievance portal."},
    {"title": "Data Privacy Policy", "category": "IT", "content": "Employee and company data must be handled with utmost care. Access to sensitive data is role-based. Data sharing outside the organization requires explicit approval. All devices must be encrypted and password-protected. Breaches must be reported to IT security within 24 hours."},
    {"title": "Performance Review Policy", "category": "HR", "content": "Performance reviews are conducted quarterly with a comprehensive annual review. Employees set goals at the beginning of each quarter in collaboration with their managers. Rating scale: 1 (Needs Improvement) to 5 (Exceptional). Reviews include self-assessment, manager assessment, and 360-degree feedback."},
]


async def seed_database():
    """Seed the database with comprehensive test data."""
    
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_factory() as db:
        # Check if already seeded
        result = await db.execute(text("SELECT COUNT(*) FROM users"))
        count = result.scalar()
        if count and count > 0:
            print("⚠️  Database already seeded. Skipping.")
            return

        print("🌱 Seeding database...")

        # ── 1. Create Roles ──────────────────────────────────
        roles = {}
        for role in UserRole:
            r = Role(
                name=role.value,
                display_name=role.value.replace("_", " ").title(),
                description=f"System role: {role.value}",
                is_system=True,
            )
            db.add(r)
            roles[role.value] = r
        await db.flush()
        print("   ✅ Roles created")

        # ── 2. Create Departments ────────────────────────────
        departments = {}
        for d in DEPARTMENTS_DATA:
            dept = Department(name=d["name"], code=d["code"], color=d["color"])
            db.add(dept)
            departments[d["code"]] = dept
        await db.flush()
        print("   ✅ Departments created")

        # ── 3. Create Designations ───────────────────────────
        designations = {}
        for d in DESIGNATIONS_DATA:
            des = Designation(title=d["title"], level=d["level"])
            db.add(des)
            designations[d["title"]] = des
        await db.flush()
        print("   ✅ Designations created")

        # ── 4. Create Admin User ─────────────────────────────
        admin_user = User(
            email="admin@hrcopilot.ai",
            hashed_password=hash_password("Admin@123"),
            first_name="System",
            last_name="Administrator",
            primary_role=UserRole.SUPER_ADMIN,
            is_active=True,
            is_verified=True,
        )
        db.add(admin_user)
        await db.flush()

        admin_employee = Employee(
            user_id=admin_user.id,
            employee_code="EMP001",
            department_id=departments["HR"].id,
            designation_id=designations["HR Manager"].id,
            employment_type="full_time",
            employment_status="active",
            date_of_birth=date(1985, 3, 15),
            gender="Male",
            nationality="Indian",
            date_of_joining=date(2020, 1, 1),
            ctc=Decimal("2500000"),
            basic_salary=Decimal("100000"),
            work_location="Bangalore",
            city="Bangalore",
            state="Karnataka",
        )
        db.add(admin_employee)
        await db.flush()
        print("   ✅ Admin user created (admin@hrcopilot.ai / Admin@123)")

        # ── 5. Create 50 Employees ──────────────────────────
        employees = [admin_employee]
        dept_codes = list(departments.keys())
        desig_titles = list(designations.keys())

        special_users = [
            {"email": "hr@hrcopilot.ai", "role": UserRole.HR_MANAGER, "first": "Kavita", "last": "Sharma", "dept": "HR", "desig": "HR Manager"},
            {"email": "recruiter@hrcopilot.ai", "role": UserRole.RECRUITER, "first": "Priya", "last": "Gupta", "dept": "HR", "desig": "Recruiter"},
            {"email": "payroll@hrcopilot.ai", "role": UserRole.PAYROLL_OFFICER, "first": "Sanjay", "last": "Mehta", "dept": "FIN", "desig": "Finance Manager"},
            {"email": "manager@hrcopilot.ai", "role": UserRole.DEPARTMENT_MANAGER, "first": "Vikram", "last": "Reddy", "dept": "ENG", "desig": "Engineering Manager"},
            {"email": "employee@hrcopilot.ai", "role": UserRole.EMPLOYEE, "first": "Rahul", "last": "Kumar", "dept": "ENG", "desig": "Software Engineer"},
        ]

        for idx, su in enumerate(special_users, start=2):
            user = User(
                email=su["email"],
                hashed_password=hash_password("Test@123"),
                first_name=su["first"],
                last_name=su["last"],
                primary_role=su["role"],
                is_active=True,
                is_verified=True,
            )
            db.add(user)
            await db.flush()

            emp = Employee(
                user_id=user.id,
                employee_code=f"EMP{idx:03d}",
                department_id=departments[su["dept"]].id,
                designation_id=designations[su["desig"]].id,
                employment_type="full_time",
                employment_status="active",
                date_of_birth=date(random.randint(1985, 1998), random.randint(1, 12), random.randint(1, 28)),
                gender="Male" if su["first"] in FIRST_NAMES_MALE else "Female",
                nationality="Indian",
                date_of_joining=date(2021, random.randint(1, 12), random.randint(1, 28)),
                ctc=Decimal(str(random.randint(800000, 3000000))),
                basic_salary=Decimal(str(random.randint(30000, 120000))),
                work_location=random.choice(CITIES[:5]),
                city=random.choice(CITIES[:5]),
                state="Karnataka",
                blood_group=random.choice(BLOOD_GROUPS),
                pan_number=f"{''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=5))}{random.randint(1000, 9999)}{''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=1))}",
            )
            db.add(emp)
            await db.flush()
            employees.append(emp)

        # Generate remaining employees
        used_emails = set(su["email"] for su in special_users)
        used_emails.add("admin@hrcopilot.ai")

        for i in range(7, 55):
            is_male = random.random() > 0.45
            first = random.choice(FIRST_NAMES_MALE if is_male else FIRST_NAMES_FEMALE)
            last = random.choice(LAST_NAMES)
            email = f"{first.lower()}.{last.lower()}{random.randint(1, 99)}@hrcopilot.ai"
            while email in used_emails:
                email = f"{first.lower()}.{last.lower()}{random.randint(100, 999)}@hrcopilot.ai"
            used_emails.add(email)

            user = User(
                email=email,
                hashed_password=hash_password("Test@123"),
                first_name=first,
                last_name=last,
                primary_role=UserRole.EMPLOYEE,
                is_active=True,
                is_verified=True,
            )
            db.add(user)
            await db.flush()

            dept = random.choice(dept_codes)
            join_date = date(random.randint(2020, 2025), random.randint(1, 12), random.randint(1, 28))
            ctc = random.randint(400000, 4000000)

            emp = Employee(
                user_id=user.id,
                employee_code=f"EMP{i:03d}",
                department_id=departments[dept].id,
                designation_id=random.choice(list(designations.values())).id,
                reporting_manager_id=random.choice(employees[:min(len(employees), 6)]).id if len(employees) > 1 else None,
                employment_type=random.choice(["full_time"] * 8 + ["contract", "intern"]),
                employment_status=random.choice(["active"] * 9 + ["on_notice"]),
                date_of_birth=date(random.randint(1985, 2000), random.randint(1, 12), random.randint(1, 28)),
                gender="Male" if is_male else "Female",
                marital_status=random.choice(["Single", "Married"]),
                blood_group=random.choice(BLOOD_GROUPS),
                nationality="Indian",
                date_of_joining=join_date,
                ctc=Decimal(str(ctc)),
                basic_salary=Decimal(str(int(ctc * 0.4 / 12))),
                work_location=random.choice(CITIES),
                city=random.choice(CITIES),
                state="Karnataka",
                personal_phone=f"+91 {random.randint(70000, 99999)}{random.randint(10000, 99999)}",
            )
            db.add(emp)
            await db.flush()

            # Add skills
            num_skills = random.randint(3, 8)
            for skill in random.sample(SKILLS_POOL, num_skills):
                db.add(EmployeeSkill(
                    employee_id=emp.id,
                    skill_name=skill,
                    proficiency=random.randint(2, 5),
                    years_experience=random.randint(1, 10),
                    is_primary=random.random() > 0.7,
                ))

            # Add timeline event
            db.add(EmployeeTimeline(
                employee_id=emp.id,
                event_type="joining",
                title="Joined the organization",
                description=f"Joined as {random.choice(desig_titles)}",
                event_date=join_date,
            ))

            employees.append(emp)

        await db.flush()
        print(f"   ✅ {len(employees)} employees created")

        # ── 6. Leave Types ───────────────────────────────────
        leave_types = {}
        for lt in LEAVE_TYPES_DATA:
            leave_type = LeaveType(
                name=lt["name"],
                code=lt["code"],
                max_days_per_year=lt["max_days"],
                is_paid=lt["paid"],
                is_carry_forward=lt.get("carry", False),
                max_carry_forward_days=lt.get("max_carry", 0),
                color=lt.get("color"),
            )
            db.add(leave_type)
            leave_types[lt["code"]] = leave_type
        await db.flush()

        # Create leave balances for all employees
        for emp in employees:
            for code, lt in leave_types.items():
                if code in ["ML", "PTL"]:
                    continue
                db.add(LeaveBalance(
                    employee_id=emp.id,
                    leave_type_id=lt.id,
                    year=2026,
                    allocated=Decimal(str(lt.max_days_per_year)),
                    used=Decimal(str(random.randint(0, min(6, lt.max_days_per_year)))),
                ))
        await db.flush()
        print("   ✅ Leave types and balances created")

        # ── 7. Holidays ─────────────────────────────────────
        for h in HOLIDAYS_2026:
            db.add(Holiday(
                name=h["name"],
                date=date.fromisoformat(h["date"]),
                type=h["type"],
                year=2026,
            ))
        await db.flush()
        print("   ✅ Holidays created")

        # ── 8. Shifts ───────────────────────────────────────
        shifts_data = [
            {"name": "General", "code": "GEN", "start": time(9, 0), "end": time(18, 0), "color": "#6366f1"},
            {"name": "Morning", "code": "MOR", "start": time(6, 0), "end": time(14, 0), "color": "#f59e0b"},
            {"name": "Evening", "code": "EVE", "start": time(14, 0), "end": time(22, 0), "color": "#8b5cf6"},
            {"name": "Night", "code": "NGT", "start": time(22, 0), "end": time(6, 0), "night": True, "color": "#1e293b"},
        ]
        shifts = {}
        for s in shifts_data:
            shift = Shift(
                name=s["name"], code=s["code"],
                start_time=s["start"], end_time=s["end"],
                is_night_shift=s.get("night", False),
                color=s.get("color"),
            )
            db.add(shift)
            shifts[s["code"]] = shift
        await db.flush()
        print("   ✅ Shifts created")

        # ── 9. Salary Structures ─────────────────────────────
        salary_structures = [
            SalaryStructure(
                name="Standard - CTC Based",
                description="Standard salary structure for full-time employees",
                components={
                    "basic": 40, "hra": 20, "da": 5,
                    "special_allowance": 23, "pf_employer": 12,
                },
            ),
            SalaryStructure(
                name="Senior Management",
                description="Salary structure for senior management (Level 7+)",
                components={
                    "basic": 50, "hra": 25, "special_allowance": 15,
                    "pf_employer": 10,
                },
            ),
        ]
        for ss in salary_structures:
            db.add(ss)
        await db.flush()
        print("   ✅ Salary structures created")

        # ── 10. Job Postings ─────────────────────────────────
        job_postings_data = [
            {
                "title": "Senior Full-Stack Engineer",
                "dept": "ENG",
                "desc": "We are looking for an experienced full-stack engineer to build and scale our core platform. You will work with React, Next.js, Python, and PostgreSQL.",
                "reqs": "5+ years experience with modern web technologies. Strong knowledge of React, TypeScript, and Python. Experience with cloud services (AWS/GCP). Understanding of system design and scalability.",
                "skills": ["React", "TypeScript", "Python", "PostgreSQL", "AWS"],
                "exp_min": 5, "exp_max": 10,
                "sal_min": 2500000, "sal_max": 4500000,
                "status": "open",
            },
            {
                "title": "ML Engineer - NLP",
                "dept": "DS",
                "desc": "Join our AI team to build state-of-the-art NLP models for HR automation. Work with LLMs, RAG pipelines, and agentic AI systems.",
                "reqs": "3+ years in ML/NLP. Experience with PyTorch/TensorFlow. Knowledge of LLMs, embeddings, and vector databases.",
                "skills": ["Python", "Machine Learning", "NLP", "Deep Learning", "PyTorch"],
                "exp_min": 3, "exp_max": 7,
                "sal_min": 2000000, "sal_max": 4000000,
                "status": "open",
            },
            {
                "title": "Product Manager",
                "dept": "PRD",
                "desc": "Drive product strategy and roadmap for our HR platform. Work closely with engineering, design, and business teams.",
                "reqs": "4+ years in product management at a SaaS company. Strong analytical skills. Experience with B2B products.",
                "skills": ["Product Management", "Agile", "SQL", "Communication"],
                "exp_min": 4, "exp_max": 8,
                "sal_min": 2000000, "sal_max": 3500000,
                "status": "open",
            },
            {
                "title": "DevOps Engineer",
                "dept": "ENG",
                "desc": "Build and maintain our cloud infrastructure. Implement CI/CD pipelines, monitoring, and security best practices.",
                "reqs": "3+ years in DevOps/SRE. Experience with AWS/GCP, Docker, Kubernetes, Terraform.",
                "skills": ["Docker", "Kubernetes", "AWS", "Terraform", "CI/CD"],
                "exp_min": 3, "exp_max": 6,
                "sal_min": 1800000, "sal_max": 3200000,
                "status": "open",
            },
        ]

        job_postings = []
        for jp in job_postings_data:
            posting = JobPosting(
                title=jp["title"],
                department_id=departments[jp["dept"]].id,
                description=jp["desc"],
                requirements=jp["reqs"],
                required_skills=jp["skills"],
                experience_min=jp["exp_min"],
                experience_max=jp["exp_max"],
                salary_min=Decimal(str(jp["sal_min"])),
                salary_max=Decimal(str(jp["sal_max"])),
                location="Bangalore",
                status=jp["status"],
                positions=random.randint(1, 3),
                posted_at=datetime.now(timezone.utc) - timedelta(days=random.randint(5, 30)),
            )
            db.add(posting)
            job_postings.append(posting)
        await db.flush()

        # Add some candidates
        stages = ["applied", "screening", "shortlisted", "interview", "technical", "hr_round", "offer"]
        for posting in job_postings:
            num_candidates = random.randint(5, 15)
            for _ in range(num_candidates):
                is_male = random.random() > 0.45
                first = random.choice(FIRST_NAMES_MALE if is_male else FIRST_NAMES_FEMALE)
                last = random.choice(LAST_NAMES)
                cand = Candidate(
                    job_posting_id=posting.id,
                    first_name=first,
                    last_name=last,
                    email=f"{first.lower()}.{last.lower()}{random.randint(1, 999)}@gmail.com",
                    phone=f"+91 {random.randint(70000, 99999)}{random.randint(10000, 99999)}",
                    experience_years=random.randint(posting.experience_min, posting.experience_max or 10),
                    current_ctc=Decimal(str(random.randint(600000, int(posting.salary_min or 1500000)))),
                    expected_ctc=Decimal(str(random.randint(int(posting.salary_min or 1500000), int(posting.salary_max or 3000000)))),
                    notice_period_days=random.choice([0, 15, 30, 60, 90]),
                    source=random.choice(["linkedin", "naukri", "referral", "website", "indeed"]),
                    stage=random.choice(stages),
                    ai_score=Decimal(str(round(random.uniform(40, 95), 2))),
                    skills_extracted=random.sample(SKILLS_POOL, random.randint(3, 7)),
                )
                db.add(cand)
        await db.flush()
        print("   ✅ Job postings and candidates created")

        # ── 11. Training Courses ─────────────────────────────
        courses = []
        for tc in TRAINING_COURSES_DATA:
            course = TrainingCourse(
                title=tc["title"],
                category=tc["category"],
                duration_hours=tc["hours"],
                difficulty_level=tc["level"],
                instructor=f"{random.choice(FIRST_NAMES_MALE)} {random.choice(LAST_NAMES)}",
                skills_covered=random.sample(SKILLS_POOL, random.randint(2, 5)),
            )
            db.add(course)
            courses.append(course)
        await db.flush()

        # Enroll some employees
        for emp in random.sample(employees, min(30, len(employees))):
            for course in random.sample(courses, random.randint(1, 3)):
                db.add(CourseEnrollment(
                    employee_id=emp.id,
                    course_id=course.id,
                    status=random.choice(["enrolled", "in_progress", "completed"]),
                    progress=random.randint(0, 100),
                ))
        await db.flush()
        print("   ✅ Training courses and enrollments created")

        # ── 12. Performance Goals ────────────────────────────
        for emp in random.sample(employees, min(40, len(employees))):
            num_goals = random.randint(2, 4)
            for g in range(num_goals):
                db.add(PerformanceGoal(
                    employee_id=emp.id,
                    title=random.choice([
                        "Improve code quality metrics by 20%",
                        "Complete AWS certification",
                        "Mentor 2 junior engineers",
                        "Deliver Q2 product milestones on time",
                        "Reduce API response time by 30%",
                        "Implement automated testing pipeline",
                        "Increase customer satisfaction score",
                        "Launch new feature module",
                    ]),
                    description="Measurable goal aligned with team OKRs",
                    progress=random.randint(0, 100),
                    status=random.choice(["not_started", "in_progress", "completed"]),
                    start_date=date(2026, 1, 1),
                    due_date=date(2026, 3, 31),
                    review_period="Q1",
                    year=2026,
                ))
        await db.flush()
        print("   ✅ Performance goals created")

        # ── 13. Compliance Policies ──────────────────────────
        for p in POLICIES_DATA:
            db.add(CompliancePolicy(
                title=p["title"],
                category=p["category"],
                content=p["content"],
                effective_date=date(2024, 1, 1),
                is_mandatory=True,
                created_by=admin_user.id,
            ))
        await db.flush()
        print("   ✅ Compliance policies created")

        # ── 14. Sample Leave Requests ────────────────────────
        for emp in random.sample(employees[1:], min(20, len(employees) - 1)):
            cl = leave_types.get("CL")
            if cl:
                start = date(2026, random.randint(1, 6), random.randint(1, 28))
                days = random.randint(1, 3)
                db.add(LeaveRequest(
                    employee_id=emp.id,
                    leave_type_id=cl.id,
                    start_date=start,
                    end_date=start + timedelta(days=days - 1),
                    total_days=Decimal(str(days)),
                    reason=random.choice([
                        "Personal work", "Family function", "Health checkup",
                        "Moving to new house", "Wedding ceremony",
                    ]),
                    status=random.choice(["approved", "approved", "pending", "rejected"]),
                ))
        await db.flush()
        print("   ✅ Sample leave requests created")

        # ── 15. Attendance Records (Last 30 days) ────────────
        today = date.today()
        for emp in employees[:20]:  # First 20 employees
            for day_offset in range(30):
                d = today - timedelta(days=day_offset)
                if d.weekday() >= 5:  # Skip weekends
                    continue
                is_late = random.random() < 0.15
                check_in_hour = 9 if not is_late else random.randint(9, 10)
                check_in_min = random.randint(0, 59) if is_late else random.randint(0, 15)
                check_out_hour = random.randint(17, 20)

                db.add(AttendanceRecord(
                    employee_id=emp.id,
                    date=d,
                    check_in=datetime(d.year, d.month, d.day, check_in_hour, check_in_min, tzinfo=timezone.utc),
                    check_out=datetime(d.year, d.month, d.day, check_out_hour, random.randint(0, 59), tzinfo=timezone.utc),
                    status="late" if is_late else "present",
                    work_hours=Decimal(str(check_out_hour - check_in_hour)),
                    is_late=is_late,
                    late_minutes=max(0, (check_in_hour - 9) * 60 + check_in_min - 15) if is_late else 0,
                    is_remote=random.random() < 0.2,
                ))
        await db.flush()
        print("   ✅ Attendance records created")

        # ── 16. Notifications ────────────────────────────────
        notification_templates = [
            {"title": "Welcome to HR Copilot!", "message": "Your account has been set up. Explore your dashboard to get started.", "type": "info", "category": "system"},
            {"title": "Leave Request Approved", "message": "Your casual leave request for 2 days has been approved.", "type": "success", "category": "leaves"},
            {"title": "New Policy Update", "message": "The Work From Home policy has been updated. Please review.", "type": "warning", "category": "compliance"},
            {"title": "Performance Review Due", "message": "Your Q1 performance self-review is due by March 31st.", "type": "info", "category": "performance"},
            {"title": "Training Recommendation", "message": "Based on your skills, we recommend the Advanced Python Programming course.", "type": "info", "category": "training"},
        ]
        for emp in employees[:10]:
            for notif in random.sample(notification_templates, random.randint(2, 4)):
                db.add(Notification(
                    user_id=emp.user_id,
                    title=notif["title"],
                    message=notif["message"],
                    type=notif["type"],
                    category=notif["category"],
                    is_read=random.random() > 0.5,
                ))
        await db.flush()
        print("   ✅ Notifications created")

        await db.commit()
        print("\n🎉 Database seeded successfully!")
        print("\n📋 Login Credentials:")
        print("   ┌─────────────────────────────┬──────────────────────┐")
        print("   │ Email                       │ Password             │")
        print("   ├─────────────────────────────┼──────────────────────┤")
        print("   │ admin@hrcopilot.ai          │ Admin@123            │")
        print("   │ hr@hrcopilot.ai             │ Test@123             │")
        print("   │ recruiter@hrcopilot.ai      │ Test@123             │")
        print("   │ payroll@hrcopilot.ai        │ Test@123             │")
        print("   │ manager@hrcopilot.ai        │ Test@123             │")
        print("   │ employee@hrcopilot.ai       │ Test@123             │")
        print("   └─────────────────────────────┴──────────────────────┘")


if __name__ == "__main__":
    asyncio.run(seed_database())
