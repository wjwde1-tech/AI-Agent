from __future__ import annotations

from decision_agent.agents.analysis_agent import AnalysisAgent
from decision_agent.agents.cleaning_agent import CleaningAgent
from decision_agent.agents.query_agent import QueryAgent
from decision_agent.agents.report_agent import ReportAgent
from decision_agent.agents.retrieval_agent import RetrievalAgent
from decision_agent.config import settings
from decision_agent.models import DecisionReport, ResearchRequest
from decision_agent.providers.llm import OpenAIResponsesProvider, RuleBasedLLMProvider
from decision_agent.providers.search import BraveSearchProvider, MockSearchProvider


class ResearchPipeline:
    def __init__(self) -> None:
        self.query_agent = QueryAgent()
        self.retrieval_agent = RetrievalAgent(provider=self._build_search_provider())
        self.cleaning_agent = CleaningAgent()
        self.analysis_agent = AnalysisAgent()
        self.report_agent = ReportAgent(llm=self._build_llm_provider())

    def run(self, req: ResearchRequest) -> DecisionReport:
        queries = self.query_agent.build_queries(req)
        hits = self.retrieval_agent.retrieve(queries=queries, per_query_limit=6)
        cleaned = self.cleaning_agent.clean_and_score(
            hits=hits,
            topic=req.topic,
            max_sources=req.max_sources,
        )
        analysis = self.analysis_agent.analyze(req=req, evidence=cleaned)
        return self.report_agent.build_report(req=req, analysis=analysis, evidence=cleaned)

    @staticmethod
    def _build_search_provider():
        if settings.search_provider.lower() == "brave":
            return BraveSearchProvider(api_key=settings.brave_search_api_key)
        return MockSearchProvider()

    @staticmethod
    def _build_llm_provider():
        if settings.llm_provider.lower() == "openai":
            return OpenAIResponsesProvider(
                api_key=settings.openai_api_key,
                model=settings.openai_model,
            )
        return RuleBasedLLMProvider()

