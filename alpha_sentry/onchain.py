from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class EvmConfig:
    rpc_url: str
    chain: str = "ethereum"


def load_evm_config() -> EvmConfig | None:
    rpc = os.getenv("EVM_RPC_URL", "").strip()
    if not rpc:
        return None
    return EvmConfig(rpc_url=rpc, chain=os.getenv("EVM_CHAIN", "ethereum"))


def poll_recent_swaps(max_events: int = 20):
    """Best-effort placeholder for Web3.py swap polling.

    We keep this minimal and dependency-light for now.
    If Web3.py is installed and RPC is configured, this function can be extended
    to fetch logs for common DEX router/pool contracts.
    """
    cfg = load_evm_config()
    if cfg is None:
        return []

    try:
        from web3 import Web3  # optional dependency
    except Exception:
        return []

    w3 = Web3(Web3.HTTPProvider(cfg.rpc_url))
    if not w3.is_connected():
        return []

    # Placeholder: only return heartbeat metadata until ABI/event mapping is wired.
    latest = w3.eth.block_number
    return [
        {
            "chain": cfg.chain,
            "tx_hash": "",
            "block_number": int(latest),
            "dex": "unmapped",
            "token_in": "",
            "token_out": "",
            "amount_usd": 0.0,
            "wallet": None,
            "note": "web3 connected; swap decoder not mapped yet",
        }
    ][:max_events]
