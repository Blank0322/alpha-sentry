from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import datetime

import aiosqlite


@dataclass(frozen=True)
class TriageResult:
    is_actionable: bool
    kind: str | None = None
    reason: str | None = None
    launch_time: str | None = None


def msg_hash(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()


async def init_db(path: str) -> None:
    async with aiosqlite.connect(path) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                msg_hash TEXT UNIQUE,
                content TEXT,
                channel_id INTEGER,
                is_actionable BOOLEAN,
                kind TEXT,
                reason TEXT,
                launch_time TEXT,
                created_at TEXT
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                msg_hash TEXT,
                alert_type TEXT,
                scheduled_time TEXT,
                sent_at TEXT
            )
            """
        )
        await db.commit()


async def save_message(path: str, *, channel_id: int, content: str, triage: TriageResult) -> None:
    h = msg_hash(content)
    async with aiosqlite.connect(path) as db:
        await db.execute(
            """
            INSERT OR IGNORE INTO messages
            (msg_hash, content, channel_id, is_actionable, kind, reason, launch_time, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                h,
                content[:2000],
                channel_id,
                int(triage.is_actionable),
                triage.kind,
                triage.reason,
                triage.launch_time,
                datetime.utcnow().isoformat(),
            ),
        )
        await db.commit()


async def save_alert(path: str, *, msg_hash: str, alert_type: str, scheduled_time: str | None = None) -> None:
    async with aiosqlite.connect(path) as db:
        await db.execute(
            """INSERT INTO alerts (msg_hash, alert_type, scheduled_time, sent_at) VALUES (?, ?, ?, ?)""",
            (msg_hash, alert_type, scheduled_time, datetime.utcnow().isoformat()),
        )
        await db.commit()
