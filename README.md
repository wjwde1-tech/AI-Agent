# AI Auto Research and Decision Report Agent (MVP)

This project is a runnable MVP for your "Direction 4"申报方向:

- Multi-agent pipeline
- Automatic market research
- Evidence cleaning and credibility scoring
- Decision-focused report generation
- CLI + HTTP API for demo

## 1) Project structure

```text
.
├── decision_agent/
│   ├── agents/
│   │   ├── analysis_agent.py
│   │   ├── cleaning_agent.py
│   │   ├── query_agent.py
│   │   ├── report_agent.py
│   │   └── retrieval_agent.py
│   ├── providers/
│   │   ├── llm.py
│   │   └── search.py
│   ├── api.py
│   ├── config.py
│   ├── models.py
│   └── pipeline.py
├── data/
│   └── sample_corpus.json
├── tests/
│   └── test_pipeline.py
├── .env.example
├── cli.py
└── requirements.txt
```

## 2) Core architecture

The pipeline uses four agents:

1. `QueryAgent`: Expand one business question into multiple search queries.
2. `RetrievalAgent`: Fetch candidate sources from a search provider.
3. `CleaningAgent`: Deduplicate sources and score credibility.
4. `AnalysisAgent` + `ReportAgent`: Build findings and generate final decision report.

## 3) Quick start

### 3.1 Install dependencies

```bash
pip install -r requirements.txt
```

### 3.2 Configure environment

Copy `.env.example` to `.env` and fill keys if you want real APIs:

- `BRAVE_SEARCH_API_KEY` (optional, for real web search)
- `OPENAI_API_KEY` (optional, for LLM polishing)

Without keys, the project still runs with built-in mock providers.

### 3.3 Run CLI demo

```bash
python cli.py --topic "AI销售外呼助手" --region "中国" --objective "判断市场进入时机与差异化机会"
```

### 3.4 Run HTTP API

```bash
uvicorn decision_agent.api:app --reload --port 8000
```

POST request:

```bash
curl -X POST "http://127.0.0.1:8000/report" \
  -H "Content-Type: application/json" \
  -d "{\"topic\":\"AI销售外呼助手\",\"region\":\"中国\",\"objective\":\"判断市场进入时机与差异化机会\"}"
```

## 4) Provider strategy

- Search provider:
  - `MockSearchProvider` (default, local sample corpus)
  - `BraveSearchProvider` (real web search)
- LLM provider:
  - `RuleBasedLLMProvider` (default, no API key needed)
  - `OpenAIResponsesProvider` (optional)

## 5) Extension ideas

1. Add more search providers (SerpAPI, Tavily, internal data lake).
2. Add financial estimation agent (TAM/SAM/SOM + unit economics).
3. Add report templates for "创业计划书", "立项评审", "投资备忘录".
4. Add multilingual output and PDF export.

