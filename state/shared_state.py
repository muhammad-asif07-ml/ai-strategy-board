from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class BoardOpinion(BaseModel):
    agent: str
    opinion: str
    confidence: float


class StrategyState(BaseModel):
    # -------- INPUTS --------
    business_goal: str
    market_context: Optional[str] = None
    budget: Optional[float] = None
    risk_tolerance: Optional[str] = None

    # -------- AGENT OUTPUTS --------
    board_opinions: List[BoardOpinion] = Field(default_factory=list)
    final_recommendation: Optional[str] = None

    # -------- TOOL OUTPUTS (🔥 NEW) --------
    tool_outputs: Dict[str, Any] = Field(default_factory=dict)

    # -------- HUMAN LOOP --------
    human_decision: Optional[str] = None
    human_notes: Optional[str] = None

    # -------- SYSTEM --------
    history: List[Dict[str, Any]] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
