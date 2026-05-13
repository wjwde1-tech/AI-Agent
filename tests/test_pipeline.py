from decision_agent.models import ResearchRequest
from decision_agent.pipeline import ResearchPipeline


def test_pipeline_generates_report() -> None:
    pipeline = ResearchPipeline()
    req = ResearchRequest(
        topic="AI销售外呼助手",
        region="中国",
        objective="判断市场进入时机与差异化机会",
        max_sources=8,
    )
    report = pipeline.run(req)
    assert report.topic == "AI销售外呼助手"
    assert len(report.evidence) > 0
    assert len(report.analysis.opportunities) > 0
    assert report.token_estimate > 10000

