from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .storage import TriageResult


class Urgency(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


@dataclass(frozen=True)
class ActionPlan:
    urgency: Urgency
    eta_minutes: int
    action: str
    checklist: list[str]


def build_action_plan(result: TriageResult, raw_text: str) -> ActionPlan | None:
    """Map triage output into an execution-oriented plan.

    This is intentionally rule-based and auditable.
    """
    if not result.is_actionable:
        return None

    text = (raw_text or "").lower()
    kind = (result.kind or "").lower()

    # lightweight intent routing
    if any(k in text for k in ["listing", "launch", "tge", "snapshot"]) or kind in {"launch", "listing"}:
        return ActionPlan(
            urgency=Urgency.high,
            eta_minutes=5,
            action="Prepare execution checklist immediately",
            checklist=[
                "Confirm exact timestamp/source link",
                "Check venue liquidity and fees",
                "Define max slippage and max notional",
                "Prepare order template (no blind market order)",
                "Set invalidation condition",
            ],
        )

    if any(k in text for k in ["airdrop", "points", "campaign", "task"]) or kind in {"airdrop", "campaign"}:
        return ActionPlan(
            urgency=Urgency.medium,
            eta_minutes=30,
            action="Queue task and verify eligibility",
            checklist=[
                "Verify official domain and anti-phishing",
                "Check wallet/account requirements",
                "Estimate effort vs expected reward",
                "Set reminder before deadline",
            ],
        )

    return ActionPlan(
        urgency=Urgency.medium,
        eta_minutes=15,
        action="Manual review before any action",
        checklist=[
            "Validate source authenticity",
            "Cross-check with secondary source",
            "Write one-sentence thesis + one invalidation",
        ],
    )
