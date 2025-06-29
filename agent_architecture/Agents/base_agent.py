"""
This module contains the base class for all agents.
"""
from abc import ABC, abstractmethod
import logging
from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class AgentMessage:
    """
    Data class for agent messages.
    """
    agent_id: str
    content: str
    metadata: Dict[str, Any]
    timestamp: float


class BaseAgent(ABC):
    """
    This is the base class for all translation based agents.
    """
    def __init__(self, agent_id: str, config: Dict[str, Any] = None):
        self.agent_id = agent_id
        self.config = config or {}
        self.logger = logging.getLogger(f"agent.{agent_id}")
        
    @abstractmethod
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process the current state and return updates"""
        pass
    
    def log_action(self, action: str, details: Dict[str, Any] = None):
        """Log agent actions for monitoring"""
        self.logger.info(f"{self.agent_id}: {action}", extra=details or {})
    
    def validate_input(self, state: Dict[str, Any]) -> bool:
        """Validate input state before processing"""
        required_fields = getattr(self, 'required_fields', [])
        return all(field in state for field in required_fields)