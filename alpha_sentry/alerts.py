from __future__ import annotations

import aiohttp


class PushoverClient:
    def __init__(self, token: str, user: str):
        self.token = token
        self.user = user

    async def send(self, title: str, message: str, *, priority: int = 0, sound: str = "vibrate") -> None:
        url = "https://api.pushover.net/1/messages.json"
        payload = {
            "token": self.token,
            "user": self.user,
            "title": title,
            "message": message,
            "priority": priority,
            "sound": sound,
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=payload) as resp:
                if resp.status != 200:
                    body = await resp.text()
                    raise RuntimeError(f"Pushover failed: {resp.status} {body}")
