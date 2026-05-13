from __future__ import annotations

import json

from decision_agent.models import ResearchRequest
from decision_agent.pipeline import ResearchPipeline


def main() -> None:
    req = ResearchRequest(
        topic="AI销售外呼助手",
        region="中国",
        objective="判断市场进入时机与差异化机会",
        max_sources=8,
    )
    report = ResearchPipeline().run(req)
    print(json.dumps(report.model_dump(mode="json"), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

