<!-- README.md -->
# FDE Pulse & Chat Intelligence Agent

An enterprise multi-agent intelligence system built for the **AI in 5 Days** assessment.
It analyzes weekly communications from `spaces/AAQAlvoeMDA` (AI GTM Tech - All Team),
distilling technical discussions into high-impact executive reports for leadership.

## Architectural Highlights
- **Multi-Agent Orchestration**: Coordinator pattern with Flash (triage) and Pro (synthesis).
- **AgentOps Compliance**: OpenTelemetry tracing, structured JSON logging, and PII redacting.
- **Safety**: Human-in-the-Loop review gate before report distribution.

## Setup & Running
1. Clone repository: `git clone <repo-url> && cd <repo>`
2. Create virtual environment: `python3 -m venv venv && source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Set credentials: `cp .env.example .env` (add your GEMINI_API_KEY)
5. Run test suite: `pytest tests/test_eval.py`
6. Run agent: `python main.py`
