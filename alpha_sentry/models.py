from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SwapEvent:
    chain: str
    tx_hash: str
    block_number: int
    dex: str
    token_in: str
    token_out: str
    amount_usd: float
    wallet: str | None = None


@dataclass(frozen=True)
class KolSignal:
    source: str
    author: str
    text: str
    url: str | None = None
    importance: float = 0.0


@dataclass(frozen=True)
class AuditDecision:
    severity: str  # low/medium/high/critical
    confidence: float
    action: str
    rationale: str
