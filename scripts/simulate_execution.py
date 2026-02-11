from __future__ import annotations

from alpha_sentry.execution import build_action_plan
from alpha_sentry.storage import TriageResult


SAMPLES = [
    (
        "Exchange listing at 14:00 UTC. Official announcement + trading pair details.",
        TriageResult(is_actionable=True, kind="listing", reason="time-sensitive listing"),
    ),
    (
        "New points campaign starts this week, limited slots and eligibility rules.",
        TriageResult(is_actionable=True, kind="campaign", reason="deadline-based task"),
    ),
    (
        "General market discussion, no concrete action.",
        TriageResult(is_actionable=False, kind="other", reason="non-actionable"),
    ),
]


def main() -> None:
    for idx, (text, triage) in enumerate(SAMPLES, 1):
        plan = build_action_plan(triage, text)
        print(f"\n[{idx}] triage={triage}")
        if not plan:
            print(" -> no execution plan")
            continue
        print(f" -> urgency={plan.urgency}, eta={plan.eta_minutes}m")
        print(f" -> action={plan.action}")
        for i, item in enumerate(plan.checklist, 1):
            print(f"    {i}. {item}")


if __name__ == "__main__":
    main()
