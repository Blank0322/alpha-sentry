# Alpha-Sentry (Execution Sentry)

Real-time signal ingestion → LLM triage → **execution checklist generation**.

This repository is a cleaned, public-friendly version of a personal monitoring tool. Sensitive artifacts (`.session`, logs, local DB, secrets) are intentionally excluded.

## Positioning

Not a full auto-trading bot.

Alpha-Sentry is an **execution sentry**:
- catch time-sensitive signals early,
- classify urgency,
- output a structured action plan,
- keep a human approval gate before any execution.

## Pipeline

```text
Telegram Ingest -> Dedupe -> SQLite Log -> LLM Triage -> Action Plan -> Alert
On-chain Swap Poll + KOL Signals -> LLM Audit Fusion -> Severity/Action
```

## Repository map

- `alpha_sentry/`
  - `config.py` settings loader
  - `storage.py` sqlite models + persistence
  - `llm.py` Gemini triage wrapper
  - `alerts.py` pushover client
  - `execution.py` rule-based execution plan builder
- `scripts/run.py` live listener
- `scripts/simulate_execution.py` local demo for action-plan routing
- `docs/ARCHITECTURE.md`
- `docs/PLAYBOOK.md`

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python scripts/run.py
```

## Demo (no credentials needed)

```bash
python scripts/simulate_execution.py
```

## Safety

- Never commit `.session` files.
- Never auto-execute trades without explicit human confirmation.
- Keep source links in logs for post-mortem audit.
