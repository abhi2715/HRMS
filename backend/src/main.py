"""
Autonomous HR Copilot — FastAPI Application Entry Point

Enterprise AI-Powered Human Resource Management System
"""

import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from src.auth.router import router as auth_router
from src.employees.router import router as employees_router
from src.leaves.router import router as leaves_router
from src.attendance.router import router as attendance_router
from src.recruitment.router import router as recruitment_router
from src.payroll.router import router as payroll_router
from src.performance.router import router as performance_router
from src.training.router import router as training_router
from src.compliance.router import router as compliance_router
from src.agents.orchestrator import router as agents_router
from src.rag.chatbot import router as chat_router
from src.dashboard.router import router as dashboard_router
from src.core.config import get_settings
from src.core.exceptions import (
    AppException,
    app_exception_handler,
    http_exception_handler,
    unhandled_exception_handler,
)
from src.core.middleware import setup_middleware

settings = get_settings()

# ── Logging Setup ────────────────────────────────────────────
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("hrms")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: startup and shutdown events."""
    logger.info("🚀 Starting Autonomous HR Copilot...")
    logger.info(f"   Environment: {settings.ENVIRONMENT}")
    logger.info(f"   Debug: {settings.DEBUG}")
    logger.info(f"   Database: {settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}")
    logger.info(f"   LLM Provider: {settings.LLM_PROVIDER}")

    # Import all models after all modules have loaded to prevent circular imports
    # while ensuring SQLAlchemy relationship strings are resolved before queries run
    from src.core.database import _import_all_models
    _import_all_models()

    yield

    logger.info("🛑 Shutting down HR Copilot...")


# ── FastAPI App ──────────────────────────────────────────────
app = FastAPI(
    title="Autonomous HR Copilot",
    description=(
        "Enterprise AI-Powered Human Resource Management System. "
        "Featuring autonomous AI agents for recruitment, payroll, leave management, "
        "attendance monitoring, compliance, and employee support."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# ── Middleware ───────────────────────────────────────────────
setup_middleware(app)

# ── Exception Handlers ──────────────────────────────────────
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

# ── API Routers ──────────────────────────────────────────────
app.include_router(auth_router, prefix=settings.API_V1_PREFIX)
app.include_router(employees_router, prefix=settings.API_V1_PREFIX)
app.include_router(leaves_router, prefix=settings.API_V1_PREFIX)
app.include_router(attendance_router, prefix=settings.API_V1_PREFIX)
app.include_router(recruitment_router, prefix=settings.API_V1_PREFIX)
app.include_router(payroll_router, prefix=settings.API_V1_PREFIX)
app.include_router(performance_router, prefix=settings.API_V1_PREFIX)
app.include_router(training_router, prefix=settings.API_V1_PREFIX)
app.include_router(compliance_router, prefix=settings.API_V1_PREFIX)
app.include_router(dashboard_router, prefix=settings.API_V1_PREFIX)
app.include_router(agents_router, prefix=settings.API_V1_PREFIX)
app.include_router(chat_router, prefix=settings.API_V1_PREFIX)


# ── Health Check ─────────────────────────────────────────────
@app.get("/health", tags=["System"])
async def health_check():
    """System health check endpoint."""
    return JSONResponse(
        content={
            "status": "healthy",
            "service": "hr-copilot",
            "version": "1.0.0",
            "environment": settings.ENVIRONMENT,
        }
    )


@app.get("/", tags=["System"])
async def root():
    """Root endpoint — API information."""
    return {
        "name": "Autonomous HR Copilot",
        "version": "1.0.0",
        "description": "Enterprise AI-Powered HRMS",
        "docs": "/docs",
        "health": "/health",
    }
