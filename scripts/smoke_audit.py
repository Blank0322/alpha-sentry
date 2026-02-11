from __future__ import annotations

import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from alpha_sentry.onchain import poll_recent_swaps
from alpha_sentry.audit_flow import build_payload


def main() -> None:
    swaps = poll_recent_swaps(max_events=5)
    payload = build_payload(swaps, [{"source": "x", "author": "@kol", "text": "sample", "importance": 0.1}])
    print("smoke_ok")
    print(f"swaps={len(swaps)}")
    print(f"payload_len={len(payload)}")


if __name__ == "__main__":
    main()
