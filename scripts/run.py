from __future__ import annotations

import asyncio
import os

import socks
from telethon import TelegramClient, events
from dotenv import load_dotenv

from alpha_sentry.alerts import PushoverClient
from alpha_sentry.config import load_settings
from alpha_sentry.llm import build_client, triage
from alpha_sentry.storage import init_db, save_alert, save_message, msg_hash

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "alpha_sentry.db")


def main():
    load_dotenv()
    s = load_settings()

    model = build_client(s.gemini_api_key)
    push = PushoverClient(token=s.push_api_token, user=s.push_user_key)

    client = TelegramClient(
        "alpha_sentry",
        s.tg_api_id,
        s.tg_api_hash,
        proxy=(socks.SOCKS5, s.proxy_host, s.proxy_port),
        auto_reconnect=True,
        request_retries=10,
        timeout=30,
    )

    async def _run():
        await init_db(DB_PATH)

        @client.on(events.NewMessage(chats=s.target_channel_id))
        async def handler(event):
            text = (event.raw_text or "").strip()
            if not text:
                return
            res = await triage(model, text)
            await save_message(DB_PATH, channel_id=s.target_channel_id, content=text, triage=res)

            if res.is_actionable:
                await push.send("Alpha-Sentry", f"{res.kind or 'signal'}\n{res.reason or ''}\n\n{text[:400]}", priority=1)
                await save_alert(DB_PATH, msg_hash=msg_hash(text), alert_type="immediate")

        await client.start()
        await client.run_until_disconnected()

    asyncio.run(_run())


if __name__ == "__main__":
    main()
