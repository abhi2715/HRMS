"""
HR Support Chatbot — RAG-powered conversational AI for employee HR queries.

Architecture:
  1. Employee asks a question (e.g., "What is the maternity leave policy?")
  2. The query is embedded and searched against the HR policy vector store
  3. Retrieved context chunks are assembled into a prompt
  4. An LLM generates a grounded answer with source citations
"""

from __future__ import annotations

import logging
import os
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from src.rag.vector_store import vector_store

logger = logging.getLogger(__name__)

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "mock")  # "openai", "gemini", "mock"


# ── LLM Integration ─────────────────────────────────────────

class LLMClient:
    """Abstraction over LLM providers for chat completion."""

    def __init__(self, provider: str = LLM_PROVIDER):
        self.provider = provider

    async def generate(self, system_prompt: str, user_query: str, context: str) -> str:
        """Generate a response using the configured LLM provider."""
        if self.provider == "openai":
            return await self._openai_generate(system_prompt, user_query, context)
        elif self.provider == "gemini":
            return await self._gemini_generate(system_prompt, user_query, context)
        elif self.provider == "groq":
            return await self._groq_generate(system_prompt, user_query, context)
        else:
            return self._mock_generate(system_prompt, user_query, context)

    async def _openai_generate(self, system_prompt: str, user_query: str, context: str) -> str:
        """Generate using OpenAI API."""
        try:
            import openai
            client = openai.AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {user_query}"},
                ],
                temperature=0.3,
                max_tokens=1024,
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            logger.error(f"OpenAI error: {e}")
            return self._mock_generate(system_prompt, user_query, context)

    async def _gemini_generate(self, system_prompt: str, user_query: str, context: str) -> str:
        """Generate using Google Gemini API."""
        try:
            import google.generativeai as genai
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = await model.generate_content_async(
                f"{system_prompt}\n\nContext:\n{context}\n\nQuestion: {user_query}"
            )
            return response.text or ""
        except Exception as e:
            logger.error(f"Gemini error: {e}")
            return self._mock_generate(system_prompt, user_query, context)

    async def _groq_generate(self, system_prompt: str, user_query: str, context: str) -> str:
        """Generate using Groq API."""
        try:
            from groq import AsyncGroq
            client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
            response = await client.chat.completions.create(
                model=os.getenv("GROQ_MODEL", "llama3-8b-8192"),
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {user_query}"},
                ],
                temperature=0.3,
                max_tokens=1024,
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            logger.error(f"Groq error: {e}")
            return self._mock_generate(system_prompt, user_query, context)

    def _mock_generate(self, system_prompt: str, user_query: str, context: str) -> str:
        """Mock LLM for development/demo without API keys."""
        if not context.strip():
            return (
                "I don't have specific information about that in our HR knowledge base yet. "
                "Please contact the HR department directly at hr@company.com for assistance."
            )

        # Extract key sentences from context for a grounded response
        sentences = [s.strip() for s in context.split(".") if len(s.strip()) > 20]
        relevant = sentences[:3]

        return (
            f"Based on our company policies, here's what I found:\n\n"
            f"{'  '.join(relevant)}.\n\n"
            f"📌 *This answer is based on {len(relevant)} relevant policy sections. "
            f"For official clarification, please consult your HR representative.*"
        )


# ── HR Policy Seed Data ──────────────────────────────────────

HR_POLICIES = [
    {
        "title": "Leave Policy",
        "content": """
        Leave Policy - Effective January 2026.
        
        Casual Leave: Employees are entitled to 12 days of casual leave per calendar year. 
        Casual leave cannot be carried forward to the next year. A maximum of 3 consecutive 
        casual leave days can be taken at a time. Casual leave requests must be submitted at 
        least 2 working days in advance except in emergencies.
        
        Sick Leave: Employees are entitled to 12 days of sick leave per year. Medical 
        certificate is mandatory for sick leave exceeding 2 consecutive days. Unused sick 
        leave can be carried forward up to a maximum of 30 days. Sick leave cannot be 
        encashed.
        
        Privilege Leave (Earned Leave): Employees earn 15 days of privilege leave per year, 
        credited quarterly (3.75 days per quarter). Privilege leave can be carried forward 
        up to 45 days. Leave encashment is available for accumulated privilege leave beyond 
        30 days at the time of separation. Minimum 5 days advance notice required.
        
        Maternity Leave: Female employees are entitled to 26 weeks of paid maternity leave 
        as per the Maternity Benefit Act 2017. This applies to women who have worked for at 
        least 80 days in the 12 months preceding the expected delivery date. Maternity leave 
        can be taken up to 8 weeks before the expected delivery date. Adoptive and 
        commissioning mothers are entitled to 12 weeks of maternity leave.
        
        Paternity Leave: Male employees are entitled to 5 days of paid paternity leave 
        within 1 month of the child's birth. This leave is non-transferable and 
        non-encashable.
        
        Compensatory Off: Employees who work on public holidays or weekends are entitled to 
        a compensatory off within 30 days. COs expire if not availed within 30 days.
        """,
    },
    {
        "title": "Attendance Policy",
        "content": """
        Attendance Policy - Effective January 2026.
        
        Working Hours: Standard working hours are 9:00 AM to 6:00 PM, Monday to Friday. 
        A grace period of 15 minutes is allowed for check-in. Total required working 
        hours per day: 8 hours (excluding 1-hour lunch break).
        
        Late Arrivals: Employees arriving after 9:15 AM will be marked as late. More 
        than 3 late arrivals in a month will trigger an automated warning. Persistent 
        lateness (more than 6 times in a month) may result in a half-day leave deduction.
        
        Remote Work: Employees may work from home up to 2 days per week with manager 
        approval. WFH must be logged in the HRMS by 9:00 AM on the WFH day. All 
        meetings must be attended via video with camera on during WFH days.
        
        Overtime: Overtime requires prior written approval from the reporting manager. 
        Overtime is compensated at 1.5x the hourly rate for weekdays and 2x for weekends 
        and holidays. Monthly overtime cannot exceed 48 hours as per labor regulations.
        """,
    },
    {
        "title": "Code of Conduct",
        "content": """
        Code of Conduct - Effective January 2026.
        
        Professional Behavior: All employees must maintain professional conduct in the 
        workplace. Harassment, discrimination, or bullying of any kind is strictly 
        prohibited and will result in immediate disciplinary action.
        
        Dress Code: Business casual attire is expected Monday through Thursday. Fridays 
        are casual dress days. Client-facing meetings require formal business attire.
        
        Confidentiality: Employees must not share proprietary company information, client 
        data, or trade secrets with unauthorized parties. Violation may result in 
        termination and legal action. All employees must sign an NDA upon joining.
        
        Conflict of Interest: Employees must disclose any potential conflicts of interest 
        to their manager and the HR department. Outside employment requires written approval 
        from the company. Moonlighting without approval is grounds for termination.
        
        Social Media: Employees must not share confidential company information on social 
        media. Any public commentary about the company must comply with the Social Media 
        Guidelines document.
        """,
    },
    {
        "title": "Compensation & Benefits",
        "content": """
        Compensation and Benefits Policy - Effective April 2026.
        
        Salary Structure: Employee compensation consists of Basic Salary (40% of CTC), 
        House Rent Allowance (50% of Basic), Special Allowance (remaining amount), and 
        statutory benefits (PF, ESI, Gratuity).
        
        Provident Fund: Both employee and employer contribute 12% of basic salary to the 
        Employee Provident Fund. The EPF contribution is capped at a basic salary of 
        ₹15,000 per month.
        
        Health Insurance: Company provides group health insurance covering the employee, 
        spouse, and up to 2 children. Sum insured: ₹5,00,000 per family. Coverage 
        includes hospitalization, pre and post-hospitalization expenses, and annual 
        health check-ups.
        
        Annual Increment: Performance-based annual increments are processed in April. 
        Increment range: 5% to 25% based on performance band. High performers 
        (Exceeds Expectations) may receive additional stock options or bonuses.
        
        Reimbursements: Internet Reimbursement up to ₹1,500/month. Phone Reimbursement 
        up to ₹1,000/month. Book/Learning allowance up to ₹5,000/quarter. These require 
        bills to be submitted within 30 days.
        """,
    },
]


# ── Chatbot Service ──────────────────────────────────────────

SYSTEM_PROMPT = """You are the HR Support Assistant for the company's HRMS portal. 
Your role is to answer employee queries about HR policies, leave rules, attendance, 
compensation, and company guidelines.

Rules:
1. ONLY answer based on the provided context from company policies.
2. If the context doesn't contain relevant information, say so clearly.
3. Be concise but thorough. Use bullet points for clarity.
4. Always cite which policy section your answer is based on.
5. For sensitive matters (disciplinary, termination), recommend contacting HR directly.
6. Format your response in a friendly, professional tone."""


class HRChatbot:
    """RAG-powered HR support chatbot."""

    def __init__(self):
        self.llm = LLMClient()
        self._policies_loaded = False

    async def initialize(self):
        """Load HR policies into the vector store."""
        if self._policies_loaded:
            return

        for policy in HR_POLICIES:
            await vector_store.add_document(
                text=policy["content"],
                metadata={"title": policy["title"], "type": "policy"},
            )
            logger.info(f"Loaded policy: {policy['title']}")

        self._policies_loaded = True
        logger.info(f"HR chatbot initialized with {len(HR_POLICIES)} policies")

    async def chat(self, query: str) -> dict[str, Any]:
        """Process a user query using RAG."""
        await self.initialize()

        # Step 1: Semantic search for relevant context
        results = await vector_store.search(query, top_k=3)

        # Step 2: Assemble context
        context_parts = []
        sources = []
        for r in results:
            context_parts.append(r["text"])
            title = r.get("metadata", {}).get("title", "Unknown Policy")
            if title not in sources:
                sources.append(title)

        context = "\n\n---\n\n".join(context_parts)

        # Step 3: Generate response
        response = await self.llm.generate(SYSTEM_PROMPT, query, context)

        return {
            "response": response,
            "sources": sources,
            "chunks_retrieved": len(results),
            "confidence": max((r.get("score", 0) for r in results), default=0),
        }


# Singleton
hr_chatbot = HRChatbot()


# ── API Schemas ──────────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=2, max_length=2000, description="The employee's question")


class ChatResponse(BaseModel):
    response: str
    sources: list[str]
    chunks_retrieved: int
    confidence: float


# ── API Router ───────────────────────────────────────────────

router = APIRouter(prefix="/chat", tags=["AI Chatbot"])


@router.post("/", response_model=ChatResponse, summary="Chat with HR Support Bot")
async def chat(request: ChatRequest):
    """RAG-powered HR policy chatbot endpoint."""
    try:
        result = await hr_chatbot.chat(request.message)
        return result
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=f"Chat service error: {str(e)}")


@router.post("/seed", summary="Load HR policies into vector store")
async def seed_policies():
    """Manually trigger policy embedding into the vector store."""
    await hr_chatbot.initialize()
    return {
        "status": "ok",
        "policies_loaded": len(HR_POLICIES),
        "vector_store_connected": vector_store.is_connected,
        "total_documents": vector_store.document_count,
    }


@router.get("/health", summary="Chatbot health check")
async def chatbot_health():
    return {
        "status": "ok",
        "vector_store_connected": vector_store.is_connected,
        "total_documents": vector_store.document_count,
        "llm_provider": LLM_PROVIDER,
        "policies_loaded": hr_chatbot._policies_loaded,
    }
