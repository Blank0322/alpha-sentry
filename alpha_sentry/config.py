from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    tg_api_id: int
    tg_api_hash: str
    target_channel_id: int
    gemini_api_key: str
    push_user_key: str
    push_api_token: str
    proxy_host: str = "127.0.0.1"
    proxy_port: int = 7890
    wake_up_offset: int = 10


def load_settings() -> Settings:
    def req(key: str) -> str:
        val = os.getenv(key)
        if not val:
            raise RuntimeError(f"Missing env var: {key}")
        return val

    return Settings(
        tg_api_id=int(req("TG_API_ID")),
        tg_api_hash=req("TG_API_HASH"),
        target_channel_id=int(req("TARGET_CHANNEL_ID")),
        gemini_api_key=req("GEMINI_API_KEY"),
        push_user_key=req("PUSH_USER_KEY"),
        push_api_token=req("PUSH_API_TOKEN"),
        proxy_host=os.getenv("PROXY_HOST", "127.0.0.1"),
        proxy_port=int(os.getenv("PROXY_PORT", "7890")),
        wake_up_offset=int(os.getenv("WAKE_UP_OFFSET", "10")),
    )
