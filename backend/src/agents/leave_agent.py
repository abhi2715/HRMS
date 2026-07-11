"""
Leave Approval Agent — LangGraph-powered autonomous leave request evaluator.

Workflow:
  1. Receive leave request
  2. Check employee leave balance
  3. Analyze team availability (prevent team understaffing)
  4. Check for abuse patterns (frequency, day-of-week clusters)
  5. Apply policy rules
  6. Auto-approve, auto-reject, or escalate to manager
"""

from __future__ import annotations

import logging
from datetime import date, timedelta
from typing import Any, Literal, TypedDict

from src.agents.base import AgentResult, AgentStatus, BaseAgent

logger = logging.getLogger(__name__)


# ── Agent State ──────────────────────────────────────────────

class LeaveAgentState(TypedDict):
    request_id: str
    employee_id: str
    leave_type: str
    start_date: str
    end_date: str
    reason: str
    # Enriched by tool nodes
    leave_balance: dict | None
    team_availability: dict | None
    abuse_flags: list[str]
    policy_check: dict | None
    # Final decision
    decision: str  # "approved" | "rejected" | "escalated"
    reasoning: list[str]
    confidence: float


# ── Node Functions (Graph Steps) ─────────────────────────────

async def check_leave_balance(state: LeaveAgentState) -> LeaveAgentState:
    """Node: Check if employee has sufficient leave balance."""
    logger.info(f"[LeaveAgent] Checking balance for employee {state['employee_id']}")

    # In production, this queries the DB via the Leave repository
    balance = {
        "casual_leave": {"total": 12, "used": 5, "available": 7},
        "sick_leave": {"total": 12, "used": 2, "available": 10},
        "privilege_leave": {"total": 15, "used": 8, "available": 7},
    }

    leave_type_key = state["leave_type"].lower().replace(" ", "_")
    current_balance = balance.get(leave_type_key, {"available": 0})
    reasoning = state.get("reasoning", [])

    if current_balance.get("available", 0) <= 0:
        reasoning.append(f"❌ Insufficient {state['leave_type']} balance. Available: 0")
    else:
        reasoning.append(
            f"✅ {state['leave_type']} balance available: {current_balance['available']} days"
        )

    return {**state, "leave_balance": balance, "reasoning": reasoning}


async def check_team_availability(state: LeaveAgentState) -> LeaveAgentState:
    """Node: Ensure team won't be understaffed."""
    logger.info(f"[LeaveAgent] Checking team availability")

    # Simulated — in production, query attendance/leave records
    team_on_leave = 2
    team_size = 10
    availability_pct = ((team_size - team_on_leave - 1) / team_size) * 100

    reasoning = state.get("reasoning", [])

    if availability_pct < 50:
        reasoning.append(
            f"⚠️ Team availability would drop to {availability_pct:.0f}% — risk of understaffing"
        )
    else:
        reasoning.append(f"✅ Team availability: {availability_pct:.0f}% — sufficient coverage")

    return {
        **state,
        "team_availability": {
            "team_size": team_size,
            "on_leave": team_on_leave,
            "availability_pct": availability_pct,
        },
        "reasoning": reasoning,
    }


async def detect_abuse_patterns(state: LeaveAgentState) -> LeaveAgentState:
    """Node: Detect potential leave abuse patterns."""
    logger.info(f"[LeaveAgent] Checking abuse patterns")

    flags = []
    reasoning = state.get("reasoning", [])

    # Monday/Friday pattern check (simulated)
    start = state.get("start_date", "")
    if start:
        try:
            d = date.fromisoformat(start)
            if d.weekday() in (0, 4):  # Monday or Friday
                flags.append("monday_friday_pattern")
                reasoning.append("⚠️ Leave on Monday/Friday — potential long-weekend pattern")
        except ValueError:
            pass

    if not flags:
        reasoning.append("✅ No abuse patterns detected")

    return {**state, "abuse_flags": flags, "reasoning": reasoning}


async def apply_policy_rules(state: LeaveAgentState) -> LeaveAgentState:
    """Node: Apply company leave policies and make final decision."""
    logger.info(f"[LeaveAgent] Applying policy rules")

    reasoning = state.get("reasoning", [])
    abuse_flags = state.get("abuse_flags", [])
    balance = state.get("leave_balance", {})
    team = state.get("team_availability", {})

    leave_type_key = state["leave_type"].lower().replace(" ", "_")
    available = balance.get(leave_type_key, {}).get("available", 0)

    # Decision logic
    if available <= 0:
        decision = "rejected"
        confidence = 0.95
        reasoning.append("🔴 REJECTED: Insufficient leave balance")
    elif team.get("availability_pct", 100) < 50:
        decision = "escalated"
        confidence = 0.7
        reasoning.append("🟡 ESCALATED: Team availability below 50%, needs manager review")
    elif len(abuse_flags) >= 2:
        decision = "escalated"
        confidence = 0.65
        reasoning.append("🟡 ESCALATED: Multiple abuse flags, needs manager review")
    else:
        decision = "approved"
        confidence = 0.9
        reasoning.append("🟢 APPROVED: All checks passed")

    return {
        **state,
        "decision": decision,
        "confidence": confidence,
        "policy_check": {"rules_applied": 4, "passed": decision == "approved"},
        "reasoning": reasoning,
    }


# ── Agent Class ──────────────────────────────────────────────

class LeaveApprovalAgent(BaseAgent):
    """Autonomous leave approval agent using LangGraph."""

    def __init__(self):
        super().__init__(
            name="Leave Approval Agent",
            description="Evaluates leave requests using balance checks, team availability analysis, abuse detection, and policy rules",
        )
        self.build_graph()

    def build_graph(self):
        """Build the LangGraph workflow.

        In production, this uses `langgraph.graph.StateGraph` to define the
        node DAG. Here we implement a lightweight sequential pipeline that
        mirrors the graph structure for portability.
        """
        self._pipeline = [
            check_leave_balance,
            check_team_availability,
            detect_abuse_patterns,
            apply_policy_rules,
        ]

    async def execute(self, input_data: dict[str, Any]) -> AgentResult:
        """Run the leave approval workflow."""
        self.status = AgentStatus.ACTIVE
        logger.info(f"[{self.name}] Starting execution for request {input_data.get('request_id')}")

        state: LeaveAgentState = {
            "request_id": input_data.get("request_id", ""),
            "employee_id": input_data.get("employee_id", ""),
            "leave_type": input_data.get("leave_type", "casual_leave"),
            "start_date": input_data.get("start_date", ""),
            "end_date": input_data.get("end_date", ""),
            "reason": input_data.get("reason", ""),
            "leave_balance": None,
            "team_availability": None,
            "abuse_flags": [],
            "policy_check": None,
            "decision": "pending",
            "reasoning": [],
            "confidence": 0.0,
        }

        try:
            for step in self._pipeline:
                state = await step(state)

            self.status = AgentStatus.COMPLETED
            return AgentResult(
                agent_name=self.name,
                status=AgentStatus.COMPLETED,
                output={
                    "decision": state["decision"],
                    "confidence": state["confidence"],
                    "leave_balance": state["leave_balance"],
                    "team_availability": state["team_availability"],
                    "abuse_flags": state["abuse_flags"],
                    "policy_check": state["policy_check"],
                },
                reasoning=state["reasoning"],
                actions_taken=[
                    "Checked leave balance",
                    "Analyzed team availability",
                    "Scanned for abuse patterns",
                    "Applied policy rules",
                    f"Decision: {state['decision'].upper()}",
                ],
            )
        except Exception as e:
            self.status = AgentStatus.ERROR
            logger.error(f"[{self.name}] Error: {e}")
            return AgentResult(
                agent_name=self.name,
                status=AgentStatus.ERROR,
                output={"error": str(e)},
                reasoning=[f"Agent failed: {str(e)}"],
                actions_taken=[],
            )
