from __future__ import annotations

import json
from dataclasses import asdict

import google.generativeai as genai

from .storage import TriageResult


PROMPT = """You are an execution-oriented crypto analyst.
Return JSON ONLY with keys:
- is_actionable (boolean)
- kind (string, optional)
- reason (string, short)
- launch_time (string, optional; if a concrete time is mentioned)

Text:
"""


def build_client(api_key: str):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("models/gemini-flash-latest")


async def triage(model, text: str) -> TriageResult:
    # SDK is sync; keep interface async for integration
    resp = model.generate_content(PROMPT + text[:1200])
    raw = resp.text.strip()
    try:
        data = json.loads(raw)
    except Exception:
        return TriageResult(False, kind=None, reason="LLM parse failed")

    return TriageResult(
        bool(data.get("is_actionable")),
        data.get("kind"),
        data.get("reason"),
        data.get("launch_time"),
    )
