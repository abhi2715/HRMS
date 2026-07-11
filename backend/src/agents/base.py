"""
LangGraph Agent Base — Foundation for all HR Copilot agents.

Each agent follows a consistent architecture:
  1. State definition (TypedDict)
  2. Tool definitions (node functions)
  3. Graph construction (StateGraph)
  4. Compiled graph execution
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, TypedDict

logger = logging.getLogger(__name__)


class AgentStatus(str, Enum):
    IDLE = "idle"
    ACTIVE = "active"
    ERROR = "error"
    COMPLETED = "completed"


class AgentResult(TypedDict):
    agent_name: str
    status: AgentStatus
    output: dict[str, Any]
    reasoning: list[str]
    actions_taken: list[str]


class BaseAgent(ABC):
    """Abstract base class for all LangGraph-powered HR agents."""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.status = AgentStatus.IDLE
        self._graph = None

    @abstractmethod
    def build_graph(self):
        """Build the LangGraph StateGraph for this agent."""
        ...

    @abstractmethod
    async def execute(self, input_data: dict[str, Any]) -> AgentResult:
        """Execute the agent's workflow with given input data."""
        ...

    def get_status(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "status": self.status.value,
        }
