from __future__ import annotations

from datetime import datetime
from typing import List

from decision_agent.models import AnalysisResult, CleanedEvidence, DecisionReport, ResearchRequest
from decision_agent.providers.llm import LLMProvider


class ReportAgent:
    def __init__(self, llm: LLMProvider) -> None:
        self.llm = llm

    def build_report(
        self,
        req: ResearchRequest,
        analysis: AnalysisResult,
        evidence: List[CleanedEvidence],
    ) -> DecisionReport:
        summary = self._draft_summary(req, analysis, evidence)
        polished_summary = self.llm.polish_report(summary)

        confidence = self._confidence(evidence)
        token_estimate = self._estimate_tokens(req, evidence, analysis)

        return DecisionReport(
            topic=req.topic,
            region=req.region,
            objective=req.objective,
            generated_at=datetime.utcnow(),
            executive_summary=polished_summary,
            analysis=analysis,
            evidence=evidence,
            confidence=confidence,
            token_estimate=token_estimate,
        )

    @staticmethod
    def _draft_summary(
        req: ResearchRequest,
        analysis: AnalysisResult,
        evidence: List[CleanedEvidence],
    ) -> str:
        top_score = evidence[0].composite_score if evidence else 0.0
        return (
            f"本报告围绕“{req.topic}”在{req.region}市场的可行性进行自动调研。"
            f"系统综合{len(evidence)}条证据，最高综合评分为{top_score:.2f}。"
            f"结论上，市场存在进入窗口，但应以垂直场景和可量化 ROI 为核心，"
            f"通过小步试点验证商业闭环，再决定规模化投入。"
            f"当前建议优先执行：{analysis.recommended_actions[0]}"
        )

    @staticmethod
    def _confidence(evidence: List[CleanedEvidence]) -> float:
        if not evidence:
            return 0.35
        avg = sum(item.composite_score for item in evidence) / len(evidence)
        diversity_bonus = min(len({item.source_name for item in evidence}) / 12.0, 0.12)
        score = min(avg + diversity_bonus, 0.95)
        return round(score, 3)

    @staticmethod
    def _estimate_tokens(
        req: ResearchRequest,
        evidence: List[CleanedEvidence],
        analysis: AnalysisResult,
    ) -> int:
        base = 12000
        query_part = 2500
        evidence_part = len(evidence) * 1800
        analysis_part = (
            len(analysis.market_signals)
            + len(analysis.opportunities)
            + len(analysis.risks)
            + len(analysis.positioning)
            + len(analysis.recommended_actions)
        ) * 400
        request_part = (len(req.topic) + len(req.objective) + len(req.region)) * 50
        return int(base + query_part + evidence_part + analysis_part + request_part)

