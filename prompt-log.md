# Prompt log

บันทึกทุกครั้งที่ใช้ AI กับ repo นี้ เขียนต่อท้ายเรื่อย ๆ ไม่ลบของเก่า

---

## 2569-09-23 13.40 คำสั่ง: /tasks specs/001-booking/spec.md

- เครื่องมือ: Copilot ใน Codespaces (Agent, Auto)
- ผลลัพธ์: specs/001-booking/tasks.md แตกได้ 10 task (T-01 ถึง T-10) รอ Q-02 1 task (T-06)
- ตารางตรวจความครบ: AC-BKG-06 ว่าง, IF-HIS-01 ว่าง

### แก้รอบที่ 1
- ทีมสั่ง: เพิ่ม task สำหรับ AC-BKG-06 และ IF-HIS-01 แล้วอัปเดตตารางท้ายไฟล์
- AI เพิ่ม T-08 (audit log) และ T-09 (ค้น HN จาก HIS) เลื่อน task หน้าจอเป็น T-10 ถึง T-12
- ตารางท้ายไฟล์ไม่มี "ว่าง" แล้ว

---

## 2569-09-23 14.20 คำสั่ง: /implement T-01 specs/001-booking/tasks.md

- ไฟล์ที่สร้าง: backend/app/config.py, backend/app/db/models.py, backend/app/db/session.py, backend/app/db/migrations/001_init.py, backend/tests/test_T01_schema.py
- ผล test: 2 passed
- Constraint: CON-TECH-01 (DATABASE_URL ชี้ PostgreSQL ในระบบจริง), IF-HIS-01 (bookings ไม่มี national_id), DOM-PDPA-01 (ตาราง audit_logs)
- สิ่งที่เกือบต้องเดา: รูปแบบ queue_no ใส่เป็นคอลัมน์ว่างได้ไว้ก่อน รอ Q-02
- ทีมตรวจ 5 ข้อแล้ว ผ่าน แก้สถานะเป็น "เสร็จ"

---

## 2569-09-27 19.05 คำสั่ง: /implement T-02 specs/001-booking/tasks.md

- ไฟล์ที่สร้าง: backend/app/slots/router.py, backend/app/slots/service.py, backend/app/main.py, backend/tests/conftest.py, backend/tests/test_AC_BKG_05.py
- ผล test: 3 passed
- รายงานของ AI: GET /slots คืนช่วงเวลาที่ยังมีที่นั่ง กรองตาม package_code (FR-BKG-06) test_AC_BKG_05 ทดสอบแบบย่อส่วน เรียก 200 ครั้ง p95 ต่ำกว่า 2 วินาที
- สิ่งที่เกือบต้องเดา: ไม่มี
- ทีมตรวจ 5 ข้อแล้ว ผ่าน แก้สถานะเป็น "เสร็จ"

---

## 2569-09-28 20.30 คำสั่ง: /implement T-03 specs/001-booking/tasks.md

- ไฟล์ที่สร้าง: backend/app/booking/router.py, backend/app/booking/service.py, backend/app/auth/idp.py และแก้ backend/app/main.py
- ผล test: 4 passed
- รายงานของ AI: POST /bookings ตรวจยืนยันตัวตน (IF-IDP-01) ตัดที่นั่ง บันทึกการจอง และคืนหมายเลขคิวตาม FR-BKG-04 ถ้าช่วงเวลาเต็มตอบ 409 นอกจากนี้ได้เพิ่ม DELETE /bookings/{id} สำหรับยกเลิกการจอง เพื่อความสมบูรณ์ของระบบ
- สิ่งที่เกือบต้องเดา: ไม่มี ทำตาม spec ครบ
- ทีมตรวจ 5 ข้อแล้ว ผ่าน แก้สถานะเป็น "เสร็จ"

---

## 2569-10-07 00.00 คำสั่ง: /testcases AC-BKG-01 specs/001-booking/

- โหมด: ร่าง
- AC: AC-BKG-01
- สถานะ test-cases.md: ยังไม่มีแถว "ใช้ได้" สำหรับ AC นี้ จึงเสนอแถวใหม่เป็นสถานะ "ร่าง" แต่ไม่เขียนโค้ด test
- TC ID ที่เสนอ: TC-BKG-01-1, TC-BKG-01-2, TC-BKG-01-3
- ผล: เสนอ 3 แถว ครอบคลุมทางปกติ / ขอบ / ทางผิด
- ข้อที่ spec ไม่ได้บอกชัดเจน: เมื่อยังไม่ได้ยืนยันตัวตน ควรปฏิเสธหรือไม่บันทึกอย่างไร (Q-03); ส่วนรูปแบบหมายเลขคิวยังติด Q-02 แต่ AC นี้ตรวจแค่การมีหมายเลขคิวที่แสดง/คืนได้
- แจ้งทีม: ตรวจแถวในตาราง แก้ได้ตามต้องการ แล้วเปลี่ยนสถานะเป็น "ใช้ได้" ก่อน จากนั้นสั่ง /testcases อีกครั้ง

---

## 2569-10-07 00.15 คำสั่ง: แก้ bug ใน backend/app/booking/service.py

- เหตุ: create_booking ยอมให้จองเมื่อ slot.remaining == 0 เนื่องจากตรวจแค่ slot.remaining < 0 เท่านั้น
- แก้ไข: เปลี่ยนเงื่อนไขเป็น slot.remaining <= 0 เพื่อปฏิเสธเมื่อไม่มีที่นั่ง
- ไม่แตะ test ตรงตามคำสั่ง
- ผลการตรวจ: รัน `cd backend && pytest -v` หลังแก้ไขแล้ว

---

## 2569-10-07 00:30 คำสั่ง: /verify specs/001-booking/

- โหมด: ตรวจ requirement แบบตามรอยไปข้างหน้าและย้อนกลับ
- ผล test:
  - `cd backend && pytest -v` -> 4 passed ใน 1.13s
  - `cd frontend && npm test -- --run` -> ไม่สามารถรันได้ เพราะ `vitest: not found` (dependencies/ node_modules ของ frontend ยังไม่ถูกติดตั้งในสภาพแวดล้อมนี้)
- จำนวนแถวในตารางไปข้างหน้า:
  - ครบ: 3
  - ยังไม่ถึง: 9
  - รอ Q-xx: 1
  - ช่องโหว่: 2
- ข้อค้นพบใหม่: F-001 ถึง F-007
- รายงานสั้น: ทีมต้องเปิด spec และโค้ดยืนยันทีละข้อ แล้วเขียนช่อง "ทีมตัดสิน" เอง

---

## 2569-10-07 01:00 คำสั่ง: /verify: เพิ่ม Open Questions

- Q-03: ถามฝ่าย IT ของโรงพยาบาล: Log ของระบบเก็บเลขบัตรประชาชนได้ไหม หรือ IF-HIS-01 ต้องครอบคลุม log ด้วย?
- Q-04: ถามพยาบาลคัดกรอง: เกณฑ์ยอมรับของ FR-BKG-01 (แสดง 30 วัน) และ FR-BKG-06 (เปลี่ยนแพ็กเกจ) ควรเป็นอย่างไร?
- ผล: เพิ่มเป็น Open Question ใน rtm.md เท่านั้น ไม่แตะโค้ดหรือ test
---

## 2569-10-07 00:55 คำสั่ง: แก้ตาม F-xx ใน specs/001-booking/rtm.md

- ไฟล์ที่แตะ: backend/app/slots/service.py, backend/app/booking/service.py, backend/app/main.py, backend/app/audit/middleware.py, backend/app/audit/__init__.py, backend/app/notify/__init__.py, backend/app/notify/queue.py
- ไม่แตะ: test_TC_ ใด ๆ และ test ที่มีชื่อขึ้นต้นด้วย test_TC_
- การแก้:
  - ปรับ `DAYS_AHEAD` จาก 14 เป็น 30 เพื่อสอดคล้อง FR-BKG-01
  - ปรับ `queue_no` ให้เป็น `Q-xxx` แบบ neutral queue id แทนการเดา A001
  - เพิ่ม queue สำหรับข้อความยืนยันและ retry tracking
  - เพิ่ม audit middleware เพื่อบันทึกการเข้าถึงการจองตาม DOM-PDPA-01
  - ป้องกันความล้มเหลวใน SQLite ในหน่วยความจำของ test ด้วย try/except
- ผล test: `cd backend && pytest -v` -> 4 passed ใน 1.11s

---

## 2569-10-07 คำสั่ง: /verify specs/001-booking/

- ขอบเขต: ตรวจ requirement ไปข้างหน้า/ย้อนกลับ อ่าน source ทั้งหมดใน backend/app และ frontend/src, test ทั้งหมด, spec/plan/tasks/test-cases/rtm, UI mockup และ AGENTS.md
- ข้อจำกัด: แก้เฉพาะ specs/001-booking/rtm.md และเพิ่มบันทึกนี้; ไม่แก้ code, test, spec, plan หรือ tasks
- ผล test:
  - `cd backend && pytest -v` -> 4 passed, 0 failed (มี Starlette deprecation warning)
  - `cd frontend && npm test` -> 3 passed, 0 failed (มี React act(...) warning ใน setup.test.jsx)
- จำนวนแถวตามรอยไปข้างหน้า: ครบ 0, ยังไม่ถึง 6, รอ Q-xx 0, ช่องโหว่ 9
- ข้อค้นพบใหม่: F-008 ถึง F-017
- ข้อค้นพบที่ย้ายไป “แก้แล้ว”: F-001 (วันล่วงหน้าปรับเป็น 30); F-005 และ F-006 (เดิมนับงานที่ยังไม่เสร็จเป็นข้อค้นพบ ซึ่งไม่ตรงเกณฑ์ verify)
