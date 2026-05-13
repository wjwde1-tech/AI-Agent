from __future__ import annotations

import json
from pathlib import Path
from typing import List, Protocol

import httpx

from decision_agent.models import SearchHit


class SearchProvider(Protocol):
    def search(self, query: str, limit: int = 8) -> List[SearchHit]:
        ...


class MockSearchProvider:
    """Offline provider using local sample corpus for deterministic demo."""

    def __init__(self, corpus_path: str = "data/sample_corpus.json") -> None:
        path = Path(corpus_path)
        self._records = json.loads(path.read_text(encoding="utf-8"))

    def search(self, query: str, limit: int = 8) -> List[SearchHit]:
        query_terms = [term.lower() for term in query.split() if term.strip()]
        scored = []
        for rec in self._records:
            text = f"{rec['title']} {rec['snippet']} {rec['source_name']}".lower()
            score = sum(1 for term in query_terms if term in text)
            scored.append((score, rec))
        scored.sort(key=lambda item: item[0], reverse=True)
        hits = []
        for _, rec in scored[:limit]:
            hits.append(SearchHit(**rec))
        return hits


class BraveSearchProvider:
    """Real web provider using Brave Search API."""

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def search(self, query: str, limit: int = 8) -> List[SearchHit]:
        if not self.api_key:
            raise RuntimeError("BRAVE_SEARCH_API_KEY is not set.")

        url = "https://api.search.brave.com/res/v1/web/search"
        headers = {
            "Accept": "application/json",
            "X-Subscription-Token": self.api_key,
        }
        params = {"q": query, "count": limit}
        with httpx.Client(timeout=20.0) as client:
            resp = client.get(url, headers=headers, params=params)
            resp.raise_for_status()
            payload = resp.json()

        raw_results = payload.get("web", {}).get("results", [])
        hits: List[SearchHit] = []
        for item in raw_results:
            hits.append(
                SearchHit(
                    title=item.get("title", ""),
                    url=item.get("url", ""),
                    snippet=item.get("description", ""),
                    source_name=item.get("profile", {}).get("name", ""),
                    published_at=item.get("age", ""),
                )
            )
        return hits

