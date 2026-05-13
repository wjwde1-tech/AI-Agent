from __future__ import annotations

from typing import List

from decision_agent.models import AnalysisResult, CleanedEvidence, ResearchRequest


class AnalysisAgent:
    def analyze(self, req: ResearchRequest, evidence: List[CleanedEvidence]) -> AnalysisResult:
        top = evidence[: min(6, len(evidence))]
        source_names = [item.source_name for item in top]
        snippets = " ".join(item.snippet for item in top).lower()

        market_signals = self._market_signals(req, source_names, snippets)
        opportunities = self._opportunities(req, snippets)
        risks = self._risks(req, snippets)
        positioning = self._positioning(req, snippets)
        recommended_actions = self._actions(req, opportunities, risks)

        return AnalysisResult(
            market_signals=market_signals,
            opportunities=opportunities,
            risks=risks,
            positioning=positioning,
            recommended_actions=recommended_actions,
        )

    def _market_signals(self, req: ResearchRequest, sources: List[str], snippets: str) -> List[str]:
        signals = [
            f"围绕“{req.topic}”的公开讨论热度持续，信息来源覆盖媒体、咨询和行业平台。",
            f"样本来源共 {len(set(sources))} 个，说明市场信号不是单点噪音。",
        ]
        if "增长" in snippets or "increase" in snippets:
            signals.append("多条资料提到增长趋势，需求侧存在扩张迹象。")
        if "成本" in snippets or "效率" in snippets:
            signals.append("降本增效相关关键词高频出现，B 端付费意愿可能由 ROI 驱动。")
        return signals[:4]

    def _opportunities(self, req: ResearchRequest, snippets: str) -> List[str]:
        opps = [
            f"在 {req.region} 市场，{req.topic} 仍有针对垂直行业的产品细分空间。",
            "竞品多聚焦通用能力，针对具体业务流程的深度集成是可切入机会。",
            "从试点项目切入并快速形成标杆案例，可降低前期获客成本。",
        ]
        if "compliance" in snippets or "合规" in snippets:
            opps.append("把合规能力产品化可形成差异化护城河。")
        return opps[:4]

    def _risks(self, req: ResearchRequest, snippets: str) -> List[str]:
        risks = [
            "同质化风险较高，若仅提供基础功能容易陷入价格竞争。",
            "对外部模型和数据源依赖度高，可能带来成本波动与服务稳定性问题。",
            "客户决策链条长，POC 到规模化采购存在时间不确定性。",
        ]
        if "regulation" in snippets or "政策" in snippets:
            risks.append(f"{req.region} 相关政策变化可能影响上线节奏。")
        return risks[:4]

    def _positioning(self, req: ResearchRequest, snippets: str) -> List[str]:
        return [
            f"定位为“{req.topic} 决策与执行助手”，强调可量化业务结果而非模型参数。",
            "产品策略采用“标准化底座 + 行业模板 + 轻咨询实施”。",
            "优先面向有明确 KPI 压力的业务部门，缩短价值验证周期。",
        ]

    def _actions(self, req: ResearchRequest, opportunities: List[str], risks: List[str]) -> List[str]:
        return [
            "先完成 2-3 个垂直行业的深度访谈，验证高频痛点与预算区间。",
            "构建 MVP 并绑定关键指标：转化率、响应时效、单次任务成本。",
            "建立分层报价策略，区分试点包、标准包和企业定制包。",
            f"围绕“{req.objective}”设置 8-12 周验证里程碑，按数据决定扩张节奏。",
        ]

