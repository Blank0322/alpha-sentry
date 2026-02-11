from __future__ import annotations

import json

from .models import AuditDecision, KolSignal, SwapEvent


PROMPT = """You are a crypto audit co-pilot.
Given on-chain swap signal(s) and KOL signal(s), produce one JSON object:
{
  "severity": "low|medium|high|critical",
  "confidence": 0.0-1.0,
  "action": "short imperative action",
  "rationale": "<=160 chars"
}
Do not output anything except JSON.
"""


def build_payload(swaps: list[dict], kols: list[dict]) -> str:
    return json.dumps({"swaps": swaps[:20], "kols": kols[:20]}, ensure_ascii=False)


def llm_audit(gemini_api_key: str, swaps: list[dict], kols: list[dict]) -> AuditDecision | None:
    if not gemini_api_key:
        return None

    # lazy import so non-LLM smoke checks can run without full deps
    from .llm import build_client

    model = build_client(gemini_api_key)
    resp = model.generate_content(PROMPT + "\n" + build_payload(swaps, kols))
    try:
        d = json.loads(resp.text.strip())
    except Exception:
        return None

    sev = str(d.get("severity", "low")).lower()
    if sev not in {"low", "medium", "high", "critical"}:
        sev = "low"

    conf = float(d.get("confidence", 0.0) or 0.0)
    conf = max(0.0, min(1.0, conf))

    return AuditDecision(
        severity=sev,
        confidence=conf,
        action=str(d.get("action", "manual review"))[:120],
        rationale=str(d.get("rationale", ""))[:160],
    )
