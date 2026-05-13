from __future__ import annotations

import argparse
import json

from decision_agent.models import ResearchRequest
from decision_agent.pipeline import ResearchPipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AI Auto Research Decision Agent CLI")
    parser.add_argument("--topic", required=True, help="Business topic")
    parser.add_argument("--region", default="中国", help="Target market region")
    parser.add_argument("--objective", required=True, help="Decision objective")
    parser.add_argument("--max-sources", type=int, default=12, help="Maximum evidence count")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    req = ResearchRequest(
        topic=args.topic,
        region=args.region,
        objective=args.objective,
        max_sources=args.max_sources,
    )

    pipeline = ResearchPipeline()
    report = pipeline.run(req)
    print(json.dumps(report.model_dump(mode="json"), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

