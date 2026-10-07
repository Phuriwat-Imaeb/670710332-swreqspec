from __future__ import annotations

from collections import deque
from datetime import datetime, timezone


class NotificationQueue:
    """Queue สำหรับจ่ายข้อความยืนยันแบบ asynchronous และเก็บรายการส่งซ้ำตาม ASM-03"""

    def __init__(self):
        self._items: deque[dict] = deque()

    def enqueue(self, payload: dict) -> dict:
        item = {
            "status": "pending",
            "created_at": datetime.now(timezone.utc),
            **payload,
        }
        self._items.append(item)
        return item

    def pending(self) -> list[dict]:
        return list(self._items)


notification_queue = NotificationQueue()
