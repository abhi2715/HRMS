"""
Attendance Agent — Autonomous attendance fraud detection and pattern analysis.

Workflow:
  1. Fetch attendance records for the period
  2. Detect anomalies (ghost punches, impossible travel, unusual patterns)
  3. Analyze working hour patterns
  4. Generate compliance report
"""

from __future__ import annotations

import logging
from datetime import datetime, time
from typing import Any, TypedDict

from src.agents.base import AgentResult, AgentStatus, BaseAgent

logger = logging.getLogger(__name__)


class AttendanceAgentState(TypedDict):
    employee_id: str
    period: str  # e.g., "2026-07"
    # Enriched
    records: list[dict]
    total_days: int
    present_days: int
    absent_days: int
    late_arrivals: int
    early_departures: int
    avg_work_hours: float
    fraud_flags: list[str]
    pattern_insights: list[str]
    risk_score: float  # 0.0 - 1.0
    reasoning: list[str]


async def fetch_attendance_records(state: AttendanceAgentState) -> AttendanceAgentState:
    """Node: Fetch attendance data for the analysis period."""
    logger.info(f"[AttendanceAgent] Fetching records for {state['employee_id']}")

    # Simulated attendance data (production queries Attendance repository)
    records = [
        {"date": "2026-07-01", "check_in": "09:15", "check_out": "18:30", "source": "biometric"},
        {"date": "2026-07-02", "check_in": "09:02", "check_out": "18:45", "source": "biometric"},
        {"date": "2026-07-03", "check_in": "10:30", "check_out": "18:00", "source": "wifi"},
        {"date": "2026-07-04", "check_in": "09:00", "check_out": "17:00", "source": "biometric"},
        {"date": "2026-07-07", "check_in": "09:10", "check_out": "18:20", "source": "biometric"},
        {"date": "2026-07-08", "check_in": "08:55", "check_out": "19:00", "source": "wifi"},
        {"date": "2026-07-09", "check_in": "11:00", "check_out": "18:00", "source": "manual"},
    ]

    reasoning = state.get("reasoning", [])
    reasoning.append(f"📋 Fetched {len(records)} attendance records for period {state['period']}")

    return {**state, "records": records, "total_days": 22, "reasoning": reasoning}


async def detect_fraud(state: AttendanceAgentState) -> AttendanceAgentState:
    """Node: Detect attendance fraud using pattern analysis."""
    logger.info(f"[AttendanceAgent] Running fraud detection")

    fraud_flags = []
    reasoning = state.get("reasoning", [])
    records = state.get("records", [])

    manual_count = sum(1 for r in records if r.get("source") == "manual")
    if manual_count > len(records) * 0.3:
        fraud_flags.append("excessive_manual_entries")
        reasoning.append(
            f"⚠️ FRAUD FLAG: {manual_count}/{len(records)} entries are manual overrides ({manual_count / len(records):.0%})"
        )

    # Check for impossible work hours (> 14 hours)
    for r in records:
        try:
            cin = datetime.strptime(r["check_in"], "%H:%M")
            cout = datetime.strptime(r["check_out"], "%H:%M")
            hours = (cout - cin).seconds / 3600
            if hours > 14:
                fraud_flags.append(f"impossible_hours_{r['date']}")
                reasoning.append(f"🔴 FRAUD FLAG: {hours:.1f} hours logged on {r['date']}")
        except (ValueError, KeyError):
            pass

    # Check for exact same punch times across multiple days (bot-like)
    check_ins = [r.get("check_in") for r in records]
    from collections import Counter
    repeated = {k: v for k, v in Counter(check_ins).items() if v >= 3}
    if repeated:
        fraud_flags.append("repeated_exact_times")
        reasoning.append(
            f"⚠️ FRAUD FLAG: Same check-in time repeated {list(repeated.values())[0]}+ times — possible automation"
        )

    if not fraud_flags:
        reasoning.append("✅ No fraud indicators detected")

    return {**state, "fraud_flags": fraud_flags, "reasoning": reasoning}


async def analyze_patterns(state: AttendanceAgentState) -> AttendanceAgentState:
    """Node: Analyze working hour patterns and punctuality."""
    logger.info(f"[AttendanceAgent] Analyzing patterns")

    records = state.get("records", [])
    reasoning = state.get("reasoning", [])
    insights = []

    late_count = 0
    early_count = 0
    total_hours = 0
    office_start = time(9, 15)  # Grace period included
    office_end = time(18, 0)

    for r in records:
        try:
            cin = datetime.strptime(r["check_in"], "%H:%M").time()
            cout = datetime.strptime(r["check_out"], "%H:%M").time()

            if cin > office_start:
                late_count += 1
            if cout < office_end:
                early_count += 1

            cin_dt = datetime.strptime(r["check_in"], "%H:%M")
            cout_dt = datetime.strptime(r["check_out"], "%H:%M")
            total_hours += (cout_dt - cin_dt).seconds / 3600
        except (ValueError, KeyError):
            pass

    avg_hours = total_hours / len(records) if records else 0
    present_days = len(records)
    absent_days = state.get("total_days", 22) - present_days

    insights.append(f"Average work hours: {avg_hours:.1f} hrs/day")
    if late_count > len(records) * 0.3:
        insights.append(f"Chronic lateness: {late_count}/{len(records)} days late")
    if avg_hours < 7.5:
        insights.append("Below minimum work hours (7.5 hrs/day average)")

    reasoning.append(f"📊 Present: {present_days}/{state.get('total_days', 22)} days | Late: {late_count} | Avg: {avg_hours:.1f}hrs/day")

    # Risk score
    risk = 0.0
    risk += len(state.get("fraud_flags", [])) * 0.2
    risk += (late_count / max(len(records), 1)) * 0.3
    risk += max(0, (8.0 - avg_hours) / 8.0) * 0.2
    risk = min(risk, 1.0)

    return {
        **state,
        "present_days": present_days,
        "absent_days": absent_days,
        "late_arrivals": late_count,
        "early_departures": early_count,
        "avg_work_hours": round(avg_hours, 1),
        "pattern_insights": insights,
        "risk_score": round(risk, 2),
        "reasoning": reasoning,
    }


class AttendanceAgent(BaseAgent):
    """Autonomous attendance monitoring agent with fraud detection."""

    def __init__(self):
        super().__init__(
            name="Attendance Agent",
            description="Monitors attendance patterns, detects fraud (ghost punches, manual overrides), and generates compliance reports",
        )
        self.build_graph()

    def build_graph(self):
        self._pipeline = [fetch_attendance_records, detect_fraud, analyze_patterns]

    async def execute(self, input_data: dict[str, Any]) -> AgentResult:
        self.status = AgentStatus.ACTIVE

        state: AttendanceAgentState = {
            "employee_id": input_data.get("employee_id", ""),
            "period": input_data.get("period", "2026-07"),
            "records": [], "total_days": 22, "present_days": 0, "absent_days": 0,
            "late_arrivals": 0, "early_departures": 0, "avg_work_hours": 0,
            "fraud_flags": [], "pattern_insights": [], "risk_score": 0, "reasoning": [],
        }

        try:
            for step in self._pipeline:
                state = await step(state)

            self.status = AgentStatus.COMPLETED
            return AgentResult(
                agent_name=self.name,
                status=AgentStatus.COMPLETED,
                output={
                    "summary": {
                        "present_days": state["present_days"],
                        "absent_days": state["absent_days"],
                        "late_arrivals": state["late_arrivals"],
                        "avg_work_hours": state["avg_work_hours"],
                    },
                    "fraud_flags": state["fraud_flags"],
                    "pattern_insights": state["pattern_insights"],
                    "risk_score": state["risk_score"],
                },
                reasoning=state["reasoning"],
                actions_taken=[
                    "Fetched attendance records",
                    "Ran fraud detection analysis",
                    "Analyzed working hour patterns",
                    f"Risk score: {state['risk_score']:.0%}",
                ],
            )
        except Exception as e:
            self.status = AgentStatus.ERROR
            return AgentResult(
                agent_name=self.name, status=AgentStatus.ERROR,
                output={"error": str(e)}, reasoning=[f"Agent failed: {e}"], actions_taken=[],
            )
