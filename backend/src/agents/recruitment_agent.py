"""
Recruitment Agent — LangGraph-powered autonomous candidate screening agent.

Workflow:
  1. Parse resume (extract skills, experience, education)
  2. Match skills against job requirements
  3. Score candidate (weighted scoring)
  4. Generate shortlist recommendation
"""

from __future__ import annotations

import logging
from typing import Any, TypedDict

from src.agents.base import AgentResult, AgentStatus, BaseAgent

logger = logging.getLogger(__name__)


class RecruitmentAgentState(TypedDict):
    candidate_name: str
    resume_text: str
    job_requirements: list[str]
    experience_required: int
    # Enriched
    extracted_skills: list[str]
    extracted_experience: int
    education: str
    skill_match_score: float
    experience_score: float
    overall_score: float
    recommendation: str
    reasoning: list[str]


async def parse_resume(state: RecruitmentAgentState) -> RecruitmentAgentState:
    """Node: Extract structured data from resume text."""
    logger.info(f"[RecruitmentAgent] Parsing resume for {state['candidate_name']}")

    # In production, this calls an LLM for NER extraction
    resume = state.get("resume_text", "").lower()

    # Simple keyword extraction (production would use LLM)
    tech_keywords = [
        "python", "javascript", "typescript", "react", "nextjs", "fastapi",
        "postgresql", "redis", "docker", "kubernetes", "aws", "gcp", "azure",
        "machine learning", "deep learning", "langchain", "sql", "git",
        "java", "node.js", "golang", "rust", "terraform",
    ]
    extracted = [kw for kw in tech_keywords if kw in resume]

    # Experience extraction (simplified)
    exp_years = 0
    for word in resume.split():
        if word.isdigit() and 0 < int(word) <= 30:
            exp_years = max(exp_years, int(word))

    education = "Unknown"
    if "phd" in resume or "doctorate" in resume:
        education = "PhD"
    elif "mtech" in resume or "masters" in resume or "m.s." in resume:
        education = "Masters"
    elif "btech" in resume or "bachelors" in resume or "b.e." in resume:
        education = "Bachelors"

    reasoning = state.get("reasoning", [])
    reasoning.append(f"📄 Extracted {len(extracted)} skills from resume")
    reasoning.append(f"📅 Detected {exp_years} years of experience")
    reasoning.append(f"🎓 Education level: {education}")

    return {
        **state,
        "extracted_skills": extracted,
        "extracted_experience": exp_years,
        "education": education,
        "reasoning": reasoning,
    }


async def match_skills(state: RecruitmentAgentState) -> RecruitmentAgentState:
    """Node: Score candidate skills against job requirements."""
    logger.info(f"[RecruitmentAgent] Matching skills")

    required = set(s.lower() for s in state.get("job_requirements", []))
    extracted = set(state.get("extracted_skills", []))

    if required:
        matched = required & extracted
        score = len(matched) / len(required)
    else:
        score = 0.0

    reasoning = state.get("reasoning", [])
    reasoning.append(
        f"🎯 Skill match: {len(required & extracted)}/{len(required)} requirements met ({score:.0%})"
    )

    return {**state, "skill_match_score": round(score, 2), "reasoning": reasoning}


async def score_candidate(state: RecruitmentAgentState) -> RecruitmentAgentState:
    """Node: Calculate overall candidate score."""
    logger.info(f"[RecruitmentAgent] Scoring candidate")

    skill_score = state.get("skill_match_score", 0)
    exp_required = state.get("experience_required", 0)
    exp_actual = state.get("extracted_experience", 0)

    exp_score = min(1.0, exp_actual / max(exp_required, 1))

    edu_scores = {"PhD": 1.0, "Masters": 0.85, "Bachelors": 0.7, "Unknown": 0.5}
    edu_score = edu_scores.get(state.get("education", "Unknown"), 0.5)

    # Weighted scoring
    overall = (skill_score * 0.5) + (exp_score * 0.3) + (edu_score * 0.2)

    if overall >= 0.8:
        recommendation = "strongly_recommend"
    elif overall >= 0.6:
        recommendation = "recommend"
    elif overall >= 0.4:
        recommendation = "maybe"
    else:
        recommendation = "not_recommend"

    reasoning = state.get("reasoning", [])
    reasoning.append(
        f"📊 Overall score: {overall:.0%} (Skills: {skill_score:.0%}, "
        f"Experience: {exp_score:.0%}, Education: {edu_score:.0%})"
    )
    reasoning.append(f"{'🟢' if overall >= 0.6 else '🟡' if overall >= 0.4 else '🔴'} "
                     f"Recommendation: {recommendation.replace('_', ' ').upper()}")

    return {
        **state,
        "experience_score": round(exp_score, 2),
        "overall_score": round(overall, 2),
        "recommendation": recommendation,
        "reasoning": reasoning,
    }


class RecruitmentAgent(BaseAgent):
    """Autonomous candidate screening and scoring agent."""

    def __init__(self):
        super().__init__(
            name="Recruitment Agent",
            description="Screens resumes, matches skills against job requirements, and generates candidate rankings",
        )
        self.build_graph()

    def build_graph(self):
        self._pipeline = [parse_resume, match_skills, score_candidate]

    async def execute(self, input_data: dict[str, Any]) -> AgentResult:
        self.status = AgentStatus.ACTIVE
        logger.info(f"[{self.name}] Screening candidate: {input_data.get('candidate_name')}")

        state: RecruitmentAgentState = {
            "candidate_name": input_data.get("candidate_name", ""),
            "resume_text": input_data.get("resume_text", ""),
            "job_requirements": input_data.get("job_requirements", []),
            "experience_required": input_data.get("experience_required", 0),
            "extracted_skills": [],
            "extracted_experience": 0,
            "education": "Unknown",
            "skill_match_score": 0.0,
            "experience_score": 0.0,
            "overall_score": 0.0,
            "recommendation": "pending",
            "reasoning": [],
        }

        try:
            for step in self._pipeline:
                state = await step(state)

            self.status = AgentStatus.COMPLETED
            return AgentResult(
                agent_name=self.name,
                status=AgentStatus.COMPLETED,
                output={
                    "candidate_name": state["candidate_name"],
                    "recommendation": state["recommendation"],
                    "overall_score": state["overall_score"],
                    "skill_match_score": state["skill_match_score"],
                    "experience_score": state["experience_score"],
                    "extracted_skills": state["extracted_skills"],
                    "education": state["education"],
                },
                reasoning=state["reasoning"],
                actions_taken=[
                    "Parsed resume and extracted structured data",
                    "Matched skills against job requirements",
                    "Calculated weighted candidate score",
                    f"Recommendation: {state['recommendation'].replace('_', ' ').upper()}",
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
