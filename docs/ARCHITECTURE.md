# Architecture

Alpha-Sentry is a small agentic pipeline:

1. **Ingest**: Telethon listens to a target channel.
2. **Persist**: store raw text and triage results in SQLite.
3. **Triage**: Gemini classifies whether a message is actionable.
4. **Alert**: Pushover notification for actionable items.

Design goals:
- avoid duplicate alerts
- keep failure modes observable (logs + DB)
- never commit credentials or `.session` files
