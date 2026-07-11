"""
Payroll Agent — Autonomous payroll processing with anomaly detection.

Workflow:
  1. Fetch employee salary structure
  2. Calculate deductions (PF, ESI, TDS, PT)
  3. Apply overtime & bonuses
  4. Detect anomalies (unusual overtime, salary spikes)
  5. Generate payslip summary
"""

from __future__ import annotations

import logging
from typing import Any, TypedDict

from src.agents.base import AgentResult, AgentStatus, BaseAgent

logger = logging.getLogger(__name__)


class PayrollAgentState(TypedDict):
    employee_id: str
    month: str
    year: int
    # Enriched
    base_salary: float
    hra: float
    special_allowance: float
    gross_salary: float
    pf_deduction: float
    esi_deduction: float
    tds_deduction: float
    professional_tax: float
    overtime_pay: float
    bonus: float
    total_deductions: float
    net_salary: float
    anomalies: list[str]
    reasoning: list[str]


async def fetch_salary_structure(state: PayrollAgentState) -> PayrollAgentState:
    """Node: Fetch employee's salary structure from HR records."""
    logger.info(f"[PayrollAgent] Fetching salary for employee {state['employee_id']}")

    # Simulated — production queries the Payroll repository
    base_salary = 85000.0
    hra = base_salary * 0.40
    special_allowance = base_salary * 0.15

    reasoning = state.get("reasoning", [])
    reasoning.append(f"💰 Fetched salary structure: Base ₹{base_salary:,.0f}, HRA ₹{hra:,.0f}")

    return {
        **state,
        "base_salary": base_salary,
        "hra": hra,
        "special_allowance": special_allowance,
        "gross_salary": base_salary + hra + special_allowance,
        "reasoning": reasoning,
    }


async def calculate_deductions(state: PayrollAgentState) -> PayrollAgentState:
    """Node: Calculate statutory deductions (PF, ESI, TDS, Professional Tax)."""
    logger.info(f"[PayrollAgent] Calculating deductions")

    gross = state.get("gross_salary", 0)
    base = state.get("base_salary", 0)

    # PF: 12% of basic salary (capped at ₹15,000 basic)
    pf_base = min(base, 15000)
    pf = pf_base * 0.12

    # ESI: 0.75% of gross (applicable if gross <= ₹21,000)
    esi = gross * 0.0075 if gross <= 21000 else 0

    # TDS: Simplified slab-based calculation (new regime FY2026-27)
    annual_income = gross * 12
    if annual_income <= 700000:
        tds_annual = 0
    elif annual_income <= 1000000:
        tds_annual = (annual_income - 700000) * 0.10
    elif annual_income <= 1200000:
        tds_annual = 30000 + (annual_income - 1000000) * 0.15
    elif annual_income <= 1500000:
        tds_annual = 60000 + (annual_income - 1200000) * 0.20
    else:
        tds_annual = 120000 + (annual_income - 1500000) * 0.30
    tds = tds_annual / 12

    # Professional Tax (Karnataka slab)
    pt = 200 if gross > 15000 else 0

    total_deductions = pf + esi + tds + pt

    reasoning = state.get("reasoning", [])
    reasoning.append(
        f"📋 Deductions: PF ₹{pf:,.0f} | ESI ₹{esi:,.0f} | TDS ₹{tds:,.0f} | PT ₹{pt:,.0f}"
    )

    return {
        **state,
        "pf_deduction": round(pf, 2),
        "esi_deduction": round(esi, 2),
        "tds_deduction": round(tds, 2),
        "professional_tax": round(pt, 2),
        "total_deductions": round(total_deductions, 2),
        "reasoning": reasoning,
    }


async def apply_overtime_bonus(state: PayrollAgentState) -> PayrollAgentState:
    """Node: Apply overtime hours and any bonuses."""
    logger.info(f"[PayrollAgent] Applying overtime & bonus")

    # Simulated overtime (production reads attendance records)
    overtime_hours = 8
    hourly_rate = state.get("base_salary", 0) / (22 * 8)  # 22 working days, 8 hours
    overtime_pay = overtime_hours * hourly_rate * 1.5  # 1.5x rate

    bonus = 0  # No bonus this month

    reasoning = state.get("reasoning", [])
    reasoning.append(f"⏰ Overtime: {overtime_hours}hrs × ₹{hourly_rate * 1.5:,.0f}/hr = ₹{overtime_pay:,.0f}")

    return {
        **state,
        "overtime_pay": round(overtime_pay, 2),
        "bonus": round(bonus, 2),
        "reasoning": reasoning,
    }


async def detect_anomalies(state: PayrollAgentState) -> PayrollAgentState:
    """Node: Detect payroll anomalies using rule-based checks."""
    logger.info(f"[PayrollAgent] Running anomaly detection")

    anomalies = []
    reasoning = state.get("reasoning", [])

    # Check 1: Overtime exceeds 20% of base
    if state.get("overtime_pay", 0) > state.get("base_salary", 0) * 0.20:
        anomalies.append("excessive_overtime")
        reasoning.append("⚠️ ANOMALY: Overtime pay exceeds 20% of base salary")

    # Check 2: Net salary deviation from last month (simulated)
    gross = state.get("gross_salary", 0) + state.get("overtime_pay", 0) + state.get("bonus", 0)
    net = gross - state.get("total_deductions", 0)
    historical_avg_net = 100000  # Simulated last 3-month average
    deviation = abs(net - historical_avg_net) / historical_avg_net
    if deviation > 0.15:
        anomalies.append("salary_deviation")
        reasoning.append(f"⚠️ ANOMALY: Net salary deviates {deviation:.0%} from 3-month average")

    # Check 3: Negative net salary
    if net < 0:
        anomalies.append("negative_net_salary")
        reasoning.append("🔴 CRITICAL: Net salary is negative after deductions")

    if not anomalies:
        reasoning.append("✅ No payroll anomalies detected")

    return {**state, "anomalies": anomalies, "net_salary": round(net, 2), "reasoning": reasoning}


class PayrollAgent(BaseAgent):
    """Autonomous payroll processing agent with anomaly detection."""

    def __init__(self):
        super().__init__(
            name="Payroll Agent",
            description="Processes payroll calculations with statutory deductions, overtime, and anomaly detection",
        )
        self.build_graph()

    def build_graph(self):
        self._pipeline = [
            fetch_salary_structure,
            calculate_deductions,
            apply_overtime_bonus,
            detect_anomalies,
        ]

    async def execute(self, input_data: dict[str, Any]) -> AgentResult:
        self.status = AgentStatus.ACTIVE
        logger.info(f"[{self.name}] Processing payroll for {input_data.get('employee_id')}")

        state: PayrollAgentState = {
            "employee_id": input_data.get("employee_id", ""),
            "month": input_data.get("month", "July"),
            "year": input_data.get("year", 2026),
            "base_salary": 0, "hra": 0, "special_allowance": 0, "gross_salary": 0,
            "pf_deduction": 0, "esi_deduction": 0, "tds_deduction": 0,
            "professional_tax": 0, "overtime_pay": 0, "bonus": 0,
            "total_deductions": 0, "net_salary": 0, "anomalies": [], "reasoning": [],
        }

        try:
            for step in self._pipeline:
                state = await step(state)

            self.status = AgentStatus.COMPLETED
            return AgentResult(
                agent_name=self.name,
                status=AgentStatus.COMPLETED,
                output={
                    "payslip": {
                        "gross_salary": state["gross_salary"],
                        "overtime_pay": state["overtime_pay"],
                        "bonus": state["bonus"],
                        "total_deductions": state["total_deductions"],
                        "net_salary": state["net_salary"],
                    },
                    "deductions": {
                        "pf": state["pf_deduction"],
                        "esi": state["esi_deduction"],
                        "tds": state["tds_deduction"],
                        "professional_tax": state["professional_tax"],
                    },
                    "anomalies": state["anomalies"],
                },
                reasoning=state["reasoning"],
                actions_taken=[
                    "Fetched salary structure",
                    "Calculated statutory deductions (PF, ESI, TDS, PT)",
                    "Applied overtime and bonus",
                    "Ran anomaly detection",
                    f"Net salary: ₹{state['net_salary']:,.0f}",
                ],
            )
        except Exception as e:
            self.status = AgentStatus.ERROR
            logger.error(f"[{self.name}] Error: {e}")
            return AgentResult(
                agent_name=self.name, status=AgentStatus.ERROR,
                output={"error": str(e)}, reasoning=[f"Agent failed: {e}"], actions_taken=[],
            )
