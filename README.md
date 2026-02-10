# Alpha-Sentry

Real-time signal ingestion → dedupe → LLM triage → alerting.

This repo is a cleaned, public-friendly version of a personal monitoring tool. **Secrets, session files, and local logs are intentionally excluded.**

## What it does

- Listens to a Telegram channel (via Telethon)
- Deduplicates + stores messages locally (SQLite)
- Uses an LLM (Gemini) to classify whether a message is actionable
- Sends alerts (Pushover) immediately or schedules a wake-up reminder

## Architecture (high level)

```text
Telegram → Ingest → Dedupe → Persist → LLM Triage → Alert Router → (Immediate | Scheduled)
```

## Quick start

1) Create a virtualenv and install deps:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

2) Copy env template:

```bash
cp .env.example .env
```

3) Run:

```bash
python scripts/run.py
```

## Notes

- You must provide your own Telegram API ID/HASH and create a session locally.
- Do not commit `.session` files.
