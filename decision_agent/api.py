from __future__ import annotations

from fastapi import FastAPI

from decision_agent.models import DecisionReport, ResearchRequest
from decision_agent.pipeline import ResearchPipeline

app = FastAPI(title="AI Auto Research Decision Agent")
pipeline = ResearchPipeline()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/report", response_model=DecisionReport)
def build_report(req: ResearchRequest) -> DecisionReport:
    return pipeline.run(req)

