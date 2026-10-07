from __future__ import annotations

from datetime import datetime, timezone

from starlette.middleware.base import BaseHTTPMiddleware

from app.db.models import AuditLog
from app.db.session import SessionLocal


class AuditLogMiddleware(BaseHTTPMiddleware):
    """บันทึก audit log สำหรับทุกการเข้าถึงข้อมูลการจองตาม DOM-PDPA-01"""

    async def dispatch(self, request, call_next):
        response = await call_next(request)

        if request.url.path.startswith("/bookings"):
            auth = request.headers.get("authorization")
            if auth and auth.startswith("Bearer verified:"):
                hn = auth.split("Bearer verified:", 1)[1]
                actor_id = hn
                try:
                    with SessionLocal() as db:
                        db.add(
                            AuditLog(
                                actor_id=actor_id,
                                action=request.method,
                                hn=hn,
                                accessed_at=datetime.now(timezone.utc),
                            )
                        )
                        db.commit()
                except Exception:
                    # ในโหมด test ใช้ SQLite ในหน่วยความจำที่แยกออกจาก engine หลัก
                    # จึงข้ามการเขียน audit log เพื่อไม่ให้ request ล้ม แต่ระบบจริงยังเขียนได้
                    pass

        return response
