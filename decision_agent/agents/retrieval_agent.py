from __future__ import annotations

from typing import List

from decision_agent.models import SearchHit
from decision_agent.providers.search import SearchProvider


class RetrievalAgent:
    def __init__(self, provider: SearchProvider) -> None:
        self.provider = provider

    def retrieve(self, queries: List[str], per_query_limit: int = 5) -> List[SearchHit]:
        hits: List[SearchHit] = []
        for query in queries:
            items = self.provider.search(query=query, limit=per_query_limit)
            hits.extend(items)
        return hits

