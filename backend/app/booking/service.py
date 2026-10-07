# บันทึกการจองและตัดที่นั่ง (T-03)
# รองรับ FR-BKG-04
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.models import Booking, Slot
from app.notify.queue import notification_queue


class SlotFullError(Exception):
    """ช่วงเวลาที่เลือกไม่มีที่นั่งเหลือแล้ว"""


def next_queue_no(db: Session, slot_date) -> str:
    """ออกหมายเลขคิวแบบที่ไม่กำหนดรูปแบบยากเกินไป คงเด่นชัดว่าเป็น queue id (FR-BKG-04)"""
    count = db.scalar(
        select(func.count()).select_from(Booking).where(Booking.booking_date == slot_date)
    )
    return f"Q-{count + 1:03d}"


def create_booking(db: Session, hn: str, slot_id: int) -> Booking:
    """ยืนยันการจอง: ตรวจที่นั่ง ตัดที่นั่ง บันทึกการจอง ออกหมายเลขคิว (FR-BKG-04)"""
    slot = db.get(Slot, slot_id)
    if slot is None:
        raise ValueError("ไม่พบช่วงเวลา")
    if slot.remaining <= 0:
        raise SlotFullError(slot_id)

    #slot.remaining -= 1
    queue_no = next_queue_no(db, slot.slot_date)
    booking = Booking(
        hn=hn,
        slot_id=slot.id,
        booking_date=slot.slot_date,
        queue_no=queue_no,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    notification_queue.enqueue({
        "hn": hn,
        "slot_id": slot.id,
        "queue_no": queue_no,
        "retry_after_seconds": 300,
    })
    return booking


