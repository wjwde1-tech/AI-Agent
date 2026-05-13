from __future__ import annotations

from typing import List

from decision_agent.models import ResearchRequest


class QueryAgent:
    """Expand user intent into multiple retrieval queries."""

    def build_queries(self, req: ResearchRequest) -> List[str]:
        topic = req.topic.strip()
        region = req.region.strip()
        objective = req.objective.strip()
        return [
            f"{topic} {region} 市场规模 增长率",
            f"{topic} {region} 竞品 对比",
            f"{topic} 用户痛点 解决方案",
            f"{topic} 商业模式 收费 模型",
            f"{topic} 风险 合规 政策",
            f"{objective} {topic} 可行性",
        ]

