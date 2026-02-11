# Audit Loop (On-chain + KOL + LLM)

This module adds a full-stack audit loop on top of the existing execution sentry:

```text
Swap signals (web3) + KOL signals -> LLM fusion audit -> severity/action output
```

## Components

- `alpha_sentry/onchain.py`
  - optional web3.py connector (`EVM_RPC_URL`)
  - placeholder polling hook for recent swaps
- `alpha_sentry/audit_flow.py`
  - combines swap + KOL payload
  - asks Gemini for one structured decision
- `scripts/run_audit_loop.py`
  - runnable loop (`--once` for smoke check)

## Run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python scripts/run_audit_loop.py --once
```

## Notes

- Current on-chain parser is scaffold-level (connection-first, decoder second).
- Next step: map concrete DEX Swap event ABIs and normalize USD sizing.
