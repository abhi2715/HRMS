# 🤖 Autonomous HR Copilot

**An Enterprise AI-Powered Human Resource Management System using Agentic AI**

[![Next.js](https://img.shields.io/badge/Next.js-15-black?logo=next.js)](https://nextjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python)](https://python.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.6-3178C6?logo=typescript)](https://typescriptlang.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker)](https://docker.com)

---

## 🎯 Overview

HR Copilot is a **production-grade HRMS** where intelligent AI agents autonomously handle routine HR operations — from leave approvals and payroll processing to candidate screening and compliance monitoring. Instead of replacing HR teams, it amplifies their capabilities with 6 specialized AI agents.

### Why This Exists

| Traditional HRMS | HR Copilot |
|---|---|
| Manual leave approvals (2-3 day turnaround) | AI auto-approves in <2 seconds with policy compliance |
| Resume screening takes 15-30 min per candidate | AI scores and ranks candidates instantly |
| Payroll anomalies caught during audits | Real-time anomaly detection every pay cycle |
| Compliance violations discovered retroactively | Proactive monitoring with weekly automated scans |
| Static dashboards, no predictions | Predictive analytics: attrition, hiring needs, cost forecasts |

---

## 🏗️ Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                        FRONTEND (Next.js 15)                   │
│  React 19 · TypeScript · Tailwind CSS · Shadcn UI · Recharts  │
└──────────────────────────┬─────────────────────────────────────┘
                           │ REST API (HTTPS)
┌──────────────────────────▼─────────────────────────────────────┐
│                       BACKEND (FastAPI)                         │
│  ┌─────────┐ ┌──────────┐ ┌────────────┐ ┌──────────────────┐ │
│  │  Auth   │ │ Modules  │ │  AI Agents │ │  RAG Chatbot     │ │
│  │  JWT    │ │ 9 CRUD   │ │  6 Agents  │ │  Vector Search   │ │
│  │  RBAC   │ │ modules  │ │  LangGraph │ │  LLM Integration │ │
│  └────┬────┘ └────┬─────┘ └─────┬──────┘ └───────┬──────────┘ │
│       │           │             │                 │            │
│  ┌────▼───────────▼─────────────▼─────────────────▼──────────┐ │
│  │              Repository Layer (SQLAlchemy 2.0)            │ │
│  └───────────────────────────┬───────────────────────────────┘ │
└──────────────────────────────┼─────────────────────────────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
    ┌─────▼─────┐       ┌─────▼─────┐       ┌─────▼─────┐
    │PostgreSQL │       │  Qdrant   │       │   Redis   │
    │  (Data)   │       │ (Vectors) │       │  (Cache)  │
    └───────────┘       └───────────┘       └───────────┘
          │
    ┌─────▼─────┐
    │    n8n    │
    │(Workflows)│
    └───────────┘
```

---

## ✨ Features

### 📊 12 HR Modules
| Module | Key Features |
|--------|-------------|
| **Dashboard** | KPI cards, growth charts, department distribution, AI insights |
| **Employees** | Full lifecycle management, search, filters, bulk operations |
| **Recruitment** | AI-powered screening, pipeline tracking, candidate ranking |
| **Leave Management** | AI auto-approval, balance tracking, abuse detection |
| **Attendance** | Biometric integration, fraud detection, pattern analysis |
| **Payroll** | Salary processing, statutory deductions (PF/ESI/TDS), anomaly detection |
| **Performance** | OKRs, 360° reviews, promotion readiness assessment |
| **Training** | Course catalog, skill development tracking, AI recommendations |
| **Compliance** | Policy management, violation monitoring, audit trails |
| **Analytics** | Predictive analytics, attrition forecasting, workforce planning |
| **AI Copilot** | Chat interface, agent management, real-time reasoning display |
| **Settings** | Profile, security, notifications, appearance, company config |

### 🤖 6 Autonomous AI Agents
| Agent | Pipeline Steps | Decision Types |
|-------|---------------|----------------|
| **Leave Approval** | Balance → Team Availability → Abuse Detection → Policy Rules | Approve / Reject / Escalate |
| **Recruitment** | Parse Resume → Match Skills → Score Candidate | Strongly Recommend → Not Recommend |
| **Payroll** | Salary Structure → Deductions → Overtime → Anomaly Detection | Process / Flag Anomaly |
| **Attendance** | Fetch Records → Fraud Detection → Pattern Analysis | Risk Score 0-100% |
| **Performance** | Aggregate Data → Goal Analysis → Review Generation → Promotion Assessment | Performance Band + Promotion Readiness |
| **Compliance** | Attendance Policy → Expense Policy → Security Policy → Report | Compliance Score + Risk Level |

### 💬 RAG-Powered HR Chatbot
- Embedded HR policies (Leave, Attendance, Code of Conduct, Compensation)
- Vector similarity search via Qdrant
- Multi-provider LLM support (OpenAI / Gemini / Mock)
- Source-cited answers with confidence scores

### ⚡ 8 n8n Automation Workflows
- Leave approval notifications (email + Slack)
- New hire onboarding automation
- Monthly payroll processing
- Daily attendance reports
- Birthday & anniversary celebrations
- Weekly compliance scans
- Automated resume screening
- Quarterly performance review cycles

---

## 🚀 Quick Start

### Prerequisites
- **Docker & Docker Compose** (recommended)
- OR: Node.js 20+, Python 3.12+, PostgreSQL 16

### Option 1: Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/hr-copilot.git
cd hr-copilot

# Start all services
docker compose up -d

# Services will be available at:
# Frontend:  http://localhost:3000
# Backend:   http://localhost:8000
# API Docs:  http://localhost:8000/docs
# n8n:       http://localhost:5678
# Qdrant:    http://localhost:6333
```

### Option 2: Local Development

```bash
# Backend
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app --reload --port 8000

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

### Default Credentials
| Role | Email | Password |
|------|-------|----------|
| Admin | rajesh.kumar@hrcopilot.io | admin123 |
| Employee | arjun.sharma@hrcopilot.io | demo123 |

> ⚠️ **Change these immediately in production!**

---

## 🛠 Tech Stack

### Frontend
| Technology | Purpose |
|-----------|---------|
| Next.js 15 | React framework with App Router |
| React 19 | UI library |
| TypeScript | Type safety |
| Tailwind CSS | Utility-first styling |
| Shadcn UI | Accessible component library |
| Framer Motion | Animations |
| Recharts | Data visualization |
| Zustand | State management |

### Backend
| Technology | Purpose |
|-----------|---------|
| FastAPI | Async Python web framework |
| SQLAlchemy 2.0 | Async ORM |
| Pydantic v2 | Data validation |
| Alembic | Database migrations |
| python-jose | JWT authentication |
| passlib[bcrypt] | Password hashing |

### AI & ML
| Technology | Purpose |
|-----------|---------|
| LangGraph | Agentic AI state machines |
| Qdrant | Vector database for RAG |
| OpenAI / Gemini | LLM providers |
| Sentence Transformers | Text embeddings |

### Infrastructure
| Technology | Purpose |
|-----------|---------|
| PostgreSQL 16 | Primary database |
| Redis 7 | Caching & message broker |
| Docker Compose | Container orchestration |
| n8n | Workflow automation |

---

## 📁 Project Structure

```
HRMS/
├── frontend/                    # Next.js 15 Application
│   ├── src/
│   │   ├── app/
│   │   │   ├── (dashboard)/     # Protected dashboard routes
│   │   │   │   ├── dashboard/   # Main dashboard + all module pages
│   │   │   │   └── layout.tsx   # Sidebar + main layout
│   │   │   ├── login/           # Authentication page
│   │   │   └── page.tsx         # Landing page
│   │   ├── components/          # Reusable UI components
│   │   ├── lib/                 # API client, utils, auth store
│   │   └── styles/              # Global CSS
│   ├── Dockerfile
│   └── package.json
│
├── backend/                     # FastAPI Application
│   ├── src/
│   │   ├── agents/              # 🤖 AI Agents (LangGraph)
│   │   │   ├── base.py          #   Base agent class
│   │   │   ├── leave_agent.py   #   Leave approval agent
│   │   │   ├── recruitment_agent.py
│   │   │   ├── payroll_agent.py
│   │   │   ├── attendance_agent.py
│   │   │   ├── performance_agent.py
│   │   │   ├── compliance_agent.py
│   │   │   └── orchestrator.py  #   Agent registry & API
│   │   ├── rag/                 # 💬 RAG Chatbot
│   │   │   ├── vector_store.py  #   Qdrant integration
│   │   │   └── chatbot.py       #   HR support chatbot
│   │   ├── auth/                # Authentication & RBAC
│   │   ├── employees/           # Employee management
│   │   ├── leaves/              # Leave management
│   │   ├── attendance/          # Attendance tracking
│   │   ├── recruitment/         # Recruitment pipeline
│   │   ├── payroll/             # Payroll processing
│   │   ├── performance/         # Performance reviews
│   │   ├── training/            # Training management
│   │   ├── compliance/          # Compliance monitoring
│   │   ├── core/                # Config, DB, security, middleware
│   │   ├── scripts/             # Seed data scripts
│   │   └── main.py              # Application entry point
│   ├── alembic/                 # Database migrations
│   ├── Dockerfile
│   └── requirements.txt
│
├── n8n-workflows/               # ⚡ Automation templates
│   └── workflow_templates.json
│
├── docker-compose.yml           # 🐳 Full-stack orchestration
└── README.md
```

---

## 🔌 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register new user |
| POST | `/api/v1/auth/login` | Login and get JWT tokens |
| POST | `/api/v1/auth/refresh` | Refresh access token |
| GET | `/api/v1/auth/me` | Get current user profile |

### AI Agents
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/agents/available` | List all available agents |
| GET | `/api/v1/agents/status` | Get agent statuses |
| POST | `/api/v1/agents/execute` | Execute an agent |

### RAG Chatbot
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/chat/` | Chat with HR support bot |
| POST | `/api/v1/chat/seed` | Load policies into vector store |
| GET | `/api/v1/chat/health` | Chatbot health check |

### CRUD Modules
Each module (employees, leaves, attendance, recruitment, payroll, performance, training, compliance) follows:
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/{module}/` | List with pagination & filters |
| POST | `/api/v1/{module}/` | Create new record |
| GET | `/api/v1/{module}/{id}` | Get by ID |
| PUT | `/api/v1/{module}/{id}` | Update record |
| DELETE | `/api/v1/{module}/{id}` | Delete record |

> 📖 **Full interactive docs**: http://localhost:8000/docs

---

## 🧪 Environment Variables

```env
# Backend (.env)
ENVIRONMENT=development
DEBUG=true

# Database
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=hrms_admin
POSTGRES_PASSWORD=hrms_secret_2026
POSTGRES_DB=hrms_db

# Auth
JWT_SECRET_KEY=your-super-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7

# AI
LLM_PROVIDER=mock  # openai | gemini | mock
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...

# Vector DB
QDRANT_HOST=localhost
QDRANT_PORT=6333

# Cache
REDIS_URL=redis://localhost:6379/0
```

---

## 📄 License

This project is built for educational and portfolio purposes. 

---

<p align="center">
  Built with ❤️ using Agentic AI, LangGraph, FastAPI, and Next.js
</p>
