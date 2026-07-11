"""
Agent Orchestrator — Central registry and execution engine for all HR agents.
Provides the API layer for agent invocation and status tracking.
"""

from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from src.agents.base import AgentResult, AgentStatus
from src.agents.leave_agent import LeaveApprovalAgent
from src.agents.recruitment_agent import RecruitmentAgent
from src.agents.payroll_agent import PayrollAgent
from src.agents.attendance_agent import AttendanceAgent
from src.agents.performance_agent import PerformanceAgent
from src.agents.compliance_agent import ComplianceAgent

logger = logging.getLogger(__name__)


# ── Agent Registry ───────────────────────────────────────────

class AgentOrchestrator:
    """Manages all AI agents and provides a unified execution interface."""

    def __init__(self):
        self.agents = {}
        self._register_agents()

    def _register_agents(self):
        """Register all available agents."""
        self.agents["leave_approval"] = LeaveApprovalAgent()
        self.agents["recruitment"] = RecruitmentAgent()
        self.agents["payroll"] = PayrollAgent()
        self.agents["attendance"] = AttendanceAgent()
        self.agents["performance"] = PerformanceAgent()
        self.agents["compliance"] = ComplianceAgent()

    def get_agent_status(self) -> list[dict]:
        return [agent.get_status() for agent in self.agents.values()]

    async def execute_agent(self, agent_id: str, input_data: dict[str, Any]) -> AgentResult:
        agent = self.agents.get(agent_id)
        if not agent:
            raise ValueError(f"Agent '{agent_id}' not found")
        return await agent.execute(input_data)


# Singleton orchestrator
orchestrator = AgentOrchestrator()


# ── API Schemas ──────────────────────────────────────────────

class AgentExecuteRequest(BaseModel):
    agent_id: str = Field(..., description="ID of the agent to execute")
    input_data: dict[str, Any] = Field(default_factory=dict, description="Input data for the agent")


class AgentStatusResponse(BaseModel):
    name: str
    description: str
    status: str


# ── API Router ───────────────────────────────────────────────

router = APIRouter(prefix="/agents", tags=["AI Agents"])


@router.get("/status", response_model=list[AgentStatusResponse], summary="Get all agent statuses")
async def get_agent_statuses():
    return orchestrator.get_agent_status()


@router.post("/execute", summary="Execute an AI agent")
async def execute_agent(request: AgentExecuteRequest):
    try:
        result = await orchestrator.execute_agent(request.agent_id, request.input_data)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Agent execution failed: {e}")
        raise HTTPException(status_code=500, detail=f"Agent execution failed: {str(e)}")


@router.get("/available", summary="List available agents")
async def list_agents():
    return {
        "agents": [
            {
                "id": agent_id,
                "name": agent.name,
                "description": agent.description,
                "status": agent.status.value,
            }
            for agent_id, agent in orchestrator.agents.items()
        ]
    }
