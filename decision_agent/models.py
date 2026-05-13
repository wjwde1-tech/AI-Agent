from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ResearchRequest(BaseModel):
    topic: str = Field(..., description="Business topic to research.")
    region: str = Field(default="中国", description="Target market region.")
    objective: str = Field(..., description="Decision objective.")
    max_sources: int = Field(default=12, ge=3, le=30)


class SearchHit(BaseModel):
    title: str
    url: str
    snippet: str = ""
    source_name: str = ""
    published_at: Optional[str] = None


class CleanedEvidence(BaseModel):
    title: str
    url: str
    snippet: str
    source_name: str
    credibility_score: float = Field(ge=0.0, le=1.0)
    freshness_score: float = Field(ge=0.0, le=1.0)
    relevance_score: float = Field(ge=0.0, le=1.0)
    composite_score: float = Field(ge=0.0, le=1.0)
    notes: str = ""


class AnalysisResult(BaseModel):
    market_signals: List[str]
    opportunities: List[str]
    risks: List[str]
    positioning: List[str]
    recommended_actions: List[str]


class DecisionReport(BaseModel):
    topic: str
    region: str
    objective: str
    generated_at: datetime
    executive_summary: str
    analysis: AnalysisResult
    evidence: List[CleanedEvidence]
    confidence: float = Field(ge=0.0, le=1.0)
    token_estimate: int

