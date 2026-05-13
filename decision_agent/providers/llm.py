from __future__ import annotations

import json
from typing import Protocol

import httpx


class LLMProvider(Protocol):
    def polish_report(self, draft: str) -> str:
        ...


class RuleBasedLLMProvider:
    """Fallback provider when no external LLM key is configured."""

    def polish_report(self, draft: str) -> str:
        return draft


class OpenAIResponsesProvider:
    """Optional provider using OpenAI Responses API over HTTPS."""

    def __init__(self, api_key: str, model: str = "gpt-4.1-mini") -> None:
        self.api_key = api_key
        self.model = model

    def polish_report(self, draft: str) -> str:
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is not set.")

        body = {
            "model": self.model,
            "input": [
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "input_text",
                            "text": (
                                "You are a business analyst. Improve clarity and structure "
                                "while preserving all facts and keeping language concise."
                            ),
                        }
                    ],
                },
                {
                    "role": "user",
                    "content": [{"type": "input_text", "text": draft}],
                },
            ],
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        with httpx.Client(timeout=30.0) as client:
            resp = client.post(
                "https://api.openai.com/v1/responses",
                headers=headers,
                data=json.dumps(body),
            )
            resp.raise_for_status()
            payload = resp.json()

        output_text = payload.get("output_text")
        if output_text:
            return output_text

        # Compatibility fallback in case output_text is absent.
        out = payload.get("output", [])
        chunks = []
        for entry in out:
            for content in entry.get("content", []):
                text = content.get("text")
                if text:
                    chunks.append(text)
        return "\n".join(chunks).strip() or draft

