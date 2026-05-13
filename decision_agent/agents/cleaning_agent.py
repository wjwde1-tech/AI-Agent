from __future__ import annotations

from datetime import datetime
from typing import Dict, List
from urllib.parse import urlparse

from decision_agent.models import CleanedEvidence, SearchHit


class CleaningAgent:
    def clean_and_score(self, hits: List[SearchHit], topic: str, max_sources: int) -> List[CleanedEvidence]:
        deduped: Dict[str, SearchHit] = {}
        for hit in hits:
            key = self._canonicalize_url(hit.url)
            if not key:
                continue
            if key not in deduped:
                deduped[key] = hit

        scored: List[CleanedEvidence] = []
        for hit in deduped.values():
            credibility = self._credibility_score(hit.url, hit.source_name)
            freshness = self._freshness_score(hit.published_at)
            relevance = self._relevance_score(hit, topic)
            composite = 0.45 * credibility + 0.25 * freshness + 0.30 * relevance
            scored.append(
                CleanedEvidence(
                    title=hit.title,
                    url=hit.url,
                    snippet=hit.snippet,
                    source_name=hit.source_name or urlparse(hit.url).netloc,
                    credibility_score=round(credibility, 3),
                    freshness_score=round(freshness, 3),
                    relevance_score=round(relevance, 3),
                    composite_score=round(composite, 3),
                    notes=self._build_note(credibility, freshness, relevance),
                )
            )

        scored.sort(key=lambda item: item.composite_score, reverse=True)
        return scored[:max_sources]

    @staticmethod
    def _canonicalize_url(url: str) -> str:
        if not url:
            return ""
        parsed = urlparse(url.strip())
        host = parsed.netloc.lower().replace("www.", "")
        return f"{host}{parsed.path}".rstrip("/")

    @staticmethod
    def _credibility_score(url: str, source_name: str) -> float:
        host = urlparse(url).netloc.lower()
        src = source_name.lower()
        if host.endswith(".gov.cn") or host.endswith(".gov"):
            return 0.95
        if host.endswith(".edu") or host.endswith(".edu.cn"):
            return 0.90
        high_quality = ["reuters", "bloomberg", "wsj", "36kr", "hbr", "mckinsey", "statista"]
        if any(token in host or token in src for token in high_quality):
            return 0.85
        if host.endswith(".org"):
            return 0.78
        if host.endswith(".com") or host.endswith(".cn"):
            return 0.68
        return 0.55

    @staticmethod
    def _freshness_score(published_at: str | None) -> float:
        if not published_at:
            return 0.5
        text = (published_at or "").strip()
        # Brave may return relative age like "2 days ago"; local corpus may use YYYY-MM-DD.
        if "day" in text or "hour" in text or "week" in text:
            return 0.9
        try:
            dt = datetime.strptime(text[:10], "%Y-%m-%d")
            days = max((datetime.utcnow() - dt).days, 0)
            if days <= 90:
                return 0.9
            if days <= 365:
                return 0.75
            if days <= 730:
                return 0.6
            return 0.45
        except ValueError:
            return 0.5

    @staticmethod
    def _relevance_score(hit: SearchHit, topic: str) -> float:
        text = f"{hit.title} {hit.snippet}".lower()
        topic_terms = [term for term in topic.lower().split() if term.strip()]
        if not topic_terms:
            return 0.5
        matches = sum(1 for term in topic_terms if term in text)
        ratio = matches / max(len(topic_terms), 1)
        return min(0.4 + ratio * 0.6, 1.0)

    @staticmethod
    def _build_note(credibility: float, freshness: float, relevance: float) -> str:
        labels = []
        labels.append("可信度高" if credibility >= 0.8 else "可信度中等")
        labels.append("信息较新" if freshness >= 0.75 else "信息时效一般")
        labels.append("主题相关性强" if relevance >= 0.75 else "相关性中等")
        return "；".join(labels)

