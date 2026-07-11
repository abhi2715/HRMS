"""
Performance Agent — AI-powered performance review generation and promotion analysis.

Workflow:
  1. Aggregate performance data (goals, reviews, metrics)
  2. Analyze goal completion rates
  3. Generate AI performance summary
  4. Produce promotion readiness assessment
"""

from __future__ import annotations

import logging
from typing import Any, TypedDict

from src.agents.base import AgentResult, AgentStatus, BaseAgent

logger = logging.getLogger(__name__)


class PerformanceAgentState(TypedDict):
    employee_id: str
    review_period: str
    # Enriched
    goals: list[dict]
    peer_reviews: list[dict]
    metrics: dict
    goal_completion_rate: float
    avg_peer_score: float
    performance_band: str  # "Exceeds", "Meets", "Below", "Needs Improvement"
    promotion_ready: bool
    promotion_confidence: float
    summary: str
    reasoning: list[str]


async def aggregate_data(state: PerformanceAgentState) -> PerformanceAgentState:
    """Node: Collect goals, peer reviews, and performance metrics."""
    logger.info(f"[PerformanceAgent] Aggregating data for {state['employee_id']}")

    # Simulated — production queries Performance repository
    goals = [
        {"title": "Complete API migration", "target": 100, "achieved": 95, "weight": 30},
        {"title": "Reduce bug backlog by 40%", "target": 40, "achieved": 52, "weight": 25},
        {"title": "Mentor 2 junior devs", "target": 2, "achieved": 2, "weight": 20},
        {"title": "Deliver Q2 analytics dashboard", "target": 100, "achieved": 100, "weight": 25},
    ]

    peer_reviews = [
        {"reviewer": "Peer A", "score": 4.2, "comment": "Great collaborator, delivers quality work"},
        {"reviewer": "Peer B", "score": 3.8, "comment": "Strong technically, could improve communication"},
        {"reviewer": "Manager", "score": 4.5, "comment": "Consistently exceeds expectations"},
    ]

    metrics = {
        "tasks_completed": 47,
        "tasks_assigned": 52,
        "avg_task_completion_days": 3.2,
        "code_review_participation": 85,
        "training_hours": 16,
    }

    reasoning = state.get("reasoning", [])
    reasoning.append(f"📊 Aggregated {len(goals)} goals, {len(peer_reviews)} reviews, and key metrics")

    return {**state, "goals": goals, "peer_reviews": peer_reviews, "metrics": metrics, "reasoning": reasoning}


async def analyze_goals(state: PerformanceAgentState) -> PerformanceAgentState:
    """Node: Calculate weighted goal completion rate."""
    logger.info(f"[PerformanceAgent] Analyzing goals")

    goals = state.get("goals", [])
    reasoning = state.get("reasoning", [])

    if not goals:
        return {**state, "goal_completion_rate": 0, "reasoning": reasoning + ["⚠️ No goals found"]}

    weighted_sum = 0
    total_weight = 0
    for g in goals:
        completion = min(100, (g["achieved"] / max(g["target"], 1)) * 100)
        weighted_sum += completion * g["weight"]
        total_weight += g["weight"]

    rate = weighted_sum / max(total_weight, 1)

    reasoning.append(f"🎯 Weighted goal completion: {rate:.1f}%")
    for g in goals:
        pct = min(100, (g["achieved"] / max(g["target"], 1)) * 100)
        emoji = "✅" if pct >= 90 else "🟡" if pct >= 70 else "🔴"
        reasoning.append(f"  {emoji} {g['title']}: {pct:.0f}% (weight: {g['weight']}%)")

    return {**state, "goal_completion_rate": round(rate, 1), "reasoning": reasoning}


async def generate_review(state: PerformanceAgentState) -> PerformanceAgentState:
    """Node: Generate performance band and AI summary."""
    logger.info(f"[PerformanceAgent] Generating review")

    reasoning = state.get("reasoning", [])
    reviews = state.get("peer_reviews", [])
    goal_rate = state.get("goal_completion_rate", 0)

    # Average peer score
    avg_score = sum(r["score"] for r in reviews) / max(len(reviews), 1)

    # Combined score (goals 60%, peer reviews 40%)
    combined = (goal_rate / 100 * 0.6) + (avg_score / 5 * 0.4)

    if combined >= 0.85:
        band = "Exceeds Expectations"
    elif combined >= 0.70:
        band = "Meets Expectations"
    elif combined >= 0.50:
        band = "Below Expectations"
    else:
        band = "Needs Improvement"

    # Generate summary (in production, this would call an LLM)
    summary = (
        f"During the {state.get('review_period', 'review period')}, the employee achieved a "
        f"{goal_rate:.0f}% goal completion rate with an average peer rating of {avg_score:.1f}/5. "
        f"Task completion rate stands at {state.get('metrics', {}).get('tasks_completed', 0)}/"
        f"{state.get('metrics', {}).get('tasks_assigned', 0)}. "
        f"Overall performance band: {band}."
    )

    reasoning.append(f"👥 Average peer score: {avg_score:.1f}/5")
    reasoning.append(f"📈 Combined score: {combined:.0%} → Band: {band}")

    return {
        **state,
        "avg_peer_score": round(avg_score, 1),
        "performance_band": band,
        "summary": summary,
        "reasoning": reasoning,
    }


async def assess_promotion(state: PerformanceAgentState) -> PerformanceAgentState:
    """Node: Evaluate promotion readiness."""
    logger.info(f"[PerformanceAgent] Assessing promotion readiness")

    reasoning = state.get("reasoning", [])
    goal_rate = state.get("goal_completion_rate", 0)
    avg_score = state.get("avg_peer_score", 0)
    band = state.get("performance_band", "")
    metrics = state.get("metrics", {})

    score = 0.0
    # Goal performance (40%)
    score += min(1.0, goal_rate / 100) * 0.4
    # Peer rating (30%)
    score += min(1.0, avg_score / 5) * 0.3
    # Initiative metrics (30%)
    initiative = (metrics.get("code_review_participation", 0) / 100 * 0.5 +
                  min(1.0, metrics.get("training_hours", 0) / 20) * 0.5)
    score += initiative * 0.3

    promotion_ready = score >= 0.75 and band in ("Exceeds Expectations", "Meets Expectations")

    emoji = "🟢" if promotion_ready else "🟡"
    reasoning.append(f"{emoji} Promotion readiness: {score:.0%} — {'READY' if promotion_ready else 'NOT YET'}")

    return {
        **state,
        "promotion_ready": promotion_ready,
        "promotion_confidence": round(score, 2),
        "reasoning": reasoning,
    }


class PerformanceAgent(BaseAgent):
    """AI-powered performance review and promotion assessment agent."""

    def __init__(self):
        super().__init__(
            name="Performance Agent",
            description="Generates AI performance reviews, calculates performance bands, and assesses promotion readiness",
        )
        self.build_graph()

    def build_graph(self):
        self._pipeline = [aggregate_data, analyze_goals, generate_review, assess_promotion]

    async def execute(self, input_data: dict[str, Any]) -> AgentResult:
        self.status = AgentStatus.ACTIVE

        state: PerformanceAgentState = {
            "employee_id": input_data.get("employee_id", ""),
            "review_period": input_data.get("review_period", "H1 2026"),
            "goals": [], "peer_reviews": [], "metrics": {},
            "goal_completion_rate": 0, "avg_peer_score": 0,
            "performance_band": "", "promotion_ready": False,
            "promotion_confidence": 0, "summary": "", "reasoning": [],
        }

        try:
            for step in self._pipeline:
                state = await step(state)

            self.status = AgentStatus.COMPLETED
            return AgentResult(
                agent_name=self.name,
                status=AgentStatus.COMPLETED,
                output={
                    "performance_band": state["performance_band"],
                    "goal_completion_rate": state["goal_completion_rate"],
                    "avg_peer_score": state["avg_peer_score"],
                    "promotion_ready": state["promotion_ready"],
                    "promotion_confidence": state["promotion_confidence"],
                    "summary": state["summary"],
                },
                reasoning=state["reasoning"],
                actions_taken=[
                    "Aggregated goals, reviews, and metrics",
                    "Analyzed weighted goal completion",
                    "Generated performance review and band",
                    "Assessed promotion readiness",
                    f"Band: {state['performance_band']}",
                ],
            )
        except Exception as e:
            self.status = AgentStatus.ERROR
            return AgentResult(
                agent_name=self.name, status=AgentStatus.ERROR,
                output={"error": str(e)}, reasoning=[f"Agent failed: {e}"], actions_taken=[],
            )
