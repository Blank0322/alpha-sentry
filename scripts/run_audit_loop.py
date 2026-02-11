from __future__ import annotations

import argparse
import os
import sys
import time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from dotenv import load_dotenv

from alpha_sentry.audit_flow import llm_audit
from alpha_sentry.onchain import poll_recent_swaps


def mock_kol_events() -> list[dict]:
    return [
        {
            "source": "x",
            "author": "@example_kol",
            "text": "Large smart money rotating into LST beta; watching YT legs.",
            "url": "https://x.com/example/status/1",
            "importance": 0.72,
        }
    ]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--once", action="store_true")
    p.add_argument("--interval", type=float, default=2.0)
    args = p.parse_args()

    load_dotenv()
    key = os.getenv("GEMINI_API_KEY", "").strip()

    while True:
        swaps = poll_recent_swaps(max_events=20)
        kols = mock_kol_events()

        decision = llm_audit(key, swaps=swaps, kols=kols) if key else None

        print("[audit-loop]")
        print(f"- swaps: {len(swaps)}")
        print(f"- kol_signals: {len(kols)}")
        if decision is None:
            print("- decision: (no llm decision; missing key or parse fail)")
        else:
            print(
                f"- decision: severity={decision.severity}, confidence={decision.confidence:.2f}, action={decision.action}"
            )
            print(f"- rationale: {decision.rationale}")

        if args.once:
            break
        time.sleep(max(args.interval, 0.2))


if __name__ == "__main__":
    main()
