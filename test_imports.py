import traceback
import importlib

modules = [
    "src.agents.router",
    "src.auth.router",
    "src.benefits.router",
    "src.candidates.router",
    "src.compliance.router",
    "src.core.router",
    "src.departments.router",
    "src.employees.router",
    "src.job_postings.router",
    "src.leave.router",
    "src.onboarding.router",
    "src.payroll.router",
    "src.performance.router",
    "src.projects.router",
    "src.recruitment.router",
    "src.reports.router",
    "src.settings.router",
    "src.training.router",
    "src.workflows.router"
]

for m in modules:
    try:
        importlib.import_module(m)
        print(f"OK {m}")
    except Exception as e:
        print(f"ERROR {m}: {e}")
