"""
Compliance Agent — Autonomous policy violation monitoring and audit agent.

Workflow:
  1. Scan employee activity data against company policies
  2. Detect violations (attendance, expense, conduct)
  3. Classify severity and assign risk levels
  4. Generate compliance report with recommended actions
"""

from __future__ import annotations

import logging
from typing import Any, TypedDict

from src.agents.base import AgentResult, AgentStatus, BaseAgent

logger = logging.getLogger(__name__)


class ComplianceAgentState(TypedDict):
    scope: str  # "individual" or "organization"
    employee_id: str  # empty if org-wide
    period: str
    # Enriched
    policies_checked: int
    violations: list[dict]
    risk_level: str  # "low", "medium", "high", "critical"
    compliance_score: float  # 0-100
    recommended_actions: list[str]
    reasoning: list[str]


async def scan_attendance_policy(state: ComplianceAgentState) -> ComplianceAgentState:
    """Node: Check attendance compliance (late arrivals, unauthorized absences)."""
    logger.info(f"[ComplianceAgent] Scanning attendance policy")

    violations = state.get("violations", [])
    reasoning = state.get("reasoning", [])

    # Simulated attendance violations
    late_days = 6
    unauthorized_absences = 1
    policy_limit_late = 3  # per month

    if late_days > policy_limit_late:
        violations.append({
            "type": "attendance",
            "rule": "Maximum 3 late arrivals per month",
            "actual": f"{late_days} late arrivals",
            "severity": "medium",
        })
        reasoning.append(f"⚠️ Attendance violation: {late_days} late arrivals (limit: {policy_limit_late})")

    if unauthorized_absences > 0:
        violations.append({
            "type": "attendance",
            "rule": "No unauthorized absences",
            "actual": f"{unauthorized_absences} unauthorized absence(s)",
            "severity": "high",
        })
        reasoning.append(f"🔴 Unauthorized absence detected: {unauthorized_absences} day(s)")

    policies_checked = state.get("policies_checked", 0) + 2
    return {**state, "violations": violations, "policies_checked": policies_checked, "reasoning": reasoning}


async def scan_expense_policy(state: ComplianceAgentState) -> ComplianceAgentState:
    """Node: Check expense report compliance."""
    logger.info(f"[ComplianceAgent] Scanning expense policy")

    violations = state.get("violations", [])
    reasoning = state.get("reasoning", [])

    # Simulated expense data
    pending_receipts = 2
    over_budget_claims = 0
    late_submissions = 1

    if pending_receipts > 0:
        violations.append({
            "type": "expense",
            "rule": "All expenses must have receipts",
            "actual": f"{pending_receipts} expenses without receipts",
            "severity": "low",
        })
        reasoning.append(f"⚠️ Missing receipts: {pending_receipts} expense(s) lack documentation")

    if late_submissions > 0:
        violations.append({
            "type": "expense",
            "rule": "Expense reports due within 7 days",
            "actual": f"{late_submissions} late submission(s)",
            "severity": "low",
        })
        reasoning.append(f"📋 Late expense submission: {late_submissions} report(s) past deadline")

    policies_checked = state.get("policies_checked", 0) + 2
    return {**state, "violations": violations, "policies_checked": policies_checked, "reasoning": reasoning}


async def scan_data_security_policy(state: ComplianceAgentState) -> ComplianceAgentState:
    """Node: Check data security and access compliance."""
    logger.info(f"[ComplianceAgent] Scanning data security policy")

    violations = state.get("violations", [])
    reasoning = state.get("reasoning", [])

    # Simulated security checks
    password_age_days = 45
    mfa_enabled = True
    vpn_usage_pct = 92  # % of remote sessions using VPN

    if password_age_days > 90:
        violations.append({
            "type": "security",
            "rule": "Password must be changed every 90 days",
            "actual": f"Password age: {password_age_days} days",
            "severity": "high",
        })
        reasoning.append(f"🔴 Password expired: {password_age_days} days old (limit: 90)")

    if not mfa_enabled:
        violations.append({
            "type": "security",
            "rule": "MFA must be enabled for all accounts",
            "actual": "MFA is disabled",
            "severity": "critical",
        })
        reasoning.append("🔴 CRITICAL: MFA is not enabled")

    if vpn_usage_pct < 100:
        reasoning.append(f"📋 VPN usage: {vpn_usage_pct}% of remote sessions (target: 100%)")

    reasoning.append(f"✅ Password age OK ({password_age_days} days)")
    reasoning.append("✅ MFA is enabled")

    policies_checked = state.get("policies_checked", 0) + 3
    return {**state, "violations": violations, "policies_checked": policies_checked, "reasoning": reasoning}


async def generate_compliance_report(state: ComplianceAgentState) -> ComplianceAgentState:
    """Node: Calculate compliance score and generate recommendations."""
    logger.info(f"[ComplianceAgent] Generating compliance report")

    violations = state.get("violations", [])
    reasoning = state.get("reasoning", [])
    policies_checked = state.get("policies_checked", 0)

    # Severity weights
    severity_weights = {"low": 5, "medium": 15, "high": 25, "critical": 40}
    total_penalty = sum(severity_weights.get(v.get("severity", "low"), 5) for v in violations)
    compliance_score = max(0, 100 - total_penalty)

    # Risk level
    if compliance_score >= 85:
        risk_level = "low"
    elif compliance_score >= 70:
        risk_level = "medium"
    elif compliance_score >= 50:
        risk_level = "high"
    else:
        risk_level = "critical"

    # Recommendations
    actions = []
    severity_counts = {}
    for v in violations:
        sev = v.get("severity", "low")
        severity_counts[sev] = severity_counts.get(sev, 0) + 1

    if severity_counts.get("critical", 0) > 0:
        actions.append("IMMEDIATE: Address critical security violations within 24 hours")
    if severity_counts.get("high", 0) > 0:
        actions.append("URGENT: Schedule meeting with employee regarding high-severity violations")
    if severity_counts.get("medium", 0) > 0:
        actions.append("Send automated warning for attendance policy violations")
    if severity_counts.get("low", 0) > 0:
        actions.append("Send reminder for pending documentation and expense receipts")
    if not violations:
        actions.append("No action needed — employee is fully compliant")

    reasoning.append(f"📊 Compliance score: {compliance_score}/100 | Risk: {risk_level.upper()}")
    reasoning.append(f"📋 Policies checked: {policies_checked} | Violations found: {len(violations)}")

    return {
        **state,
        "compliance_score": compliance_score,
        "risk_level": risk_level,
        "recommended_actions": actions,
        "reasoning": reasoning,
    }


class ComplianceAgent(BaseAgent):
    """Autonomous compliance monitoring and audit agent."""

    def __init__(self):
        super().__init__(
            name="Compliance Agent",
            description="Scans employee activities against company policies, detects violations, and generates compliance reports",
        )
        self.build_graph()

    def build_graph(self):
        self._pipeline = [
            scan_attendance_policy,
            scan_expense_policy,
            scan_data_security_policy,
            generate_compliance_report,
        ]

    async def execute(self, input_data: dict[str, Any]) -> AgentResult:
        self.status = AgentStatus.ACTIVE

        state: ComplianceAgentState = {
            "scope": input_data.get("scope", "individual"),
            "employee_id": input_data.get("employee_id", ""),
            "period": input_data.get("period", "2026-07"),
            "policies_checked": 0, "violations": [],
            "risk_level": "low", "compliance_score": 100,
            "recommended_actions": [], "reasoning": [],
        }

        try:
            for step in self._pipeline:
                state = await step(state)

            self.status = AgentStatus.COMPLETED
            return AgentResult(
                agent_name=self.name,
                status=AgentStatus.COMPLETED,
                output={
                    "compliance_score": state["compliance_score"],
                    "risk_level": state["risk_level"],
                    "policies_checked": state["policies_checked"],
                    "violations": state["violations"],
                    "recommended_actions": state["recommended_actions"],
                },
                reasoning=state["reasoning"],
                actions_taken=[
                    "Scanned attendance policy",
                    "Scanned expense policy",
                    "Scanned data security policy",
                    "Generated compliance report",
                    f"Score: {state['compliance_score']}/100 | Risk: {state['risk_level'].upper()}",
                ],
            )
        except Exception as e:
            self.status = AgentStatus.ERROR
            return AgentResult(
                agent_name=self.name, status=AgentStatus.ERROR,
                output={"error": str(e)}, reasoning=[f"Agent failed: {e}"], actions_taken=[],
            )
