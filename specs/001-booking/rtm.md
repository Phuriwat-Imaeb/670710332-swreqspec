# RTM: จองคิวตรวจสุขภาพ (Booking)
อ้างอิง: spec.md Draft v2 | tasks.md | test-cases.md
สร้างด้วย /verify เมื่อ 2569-10-07 | test: backend 4 ผ่าน 0 ไม่ผ่าน; frontend 3 ผ่าน 0 ไม่ผ่าน

## 1. ตามรอยไปข้างหน้า (requirement ไป โค้ด ไป test)
| ID | AC | task | โค้ด (ไฟล์: ฟังก์ชัน) | test (ผล) | สถานะ |
|---|---|---|---|---|---|
| FR-BKG-01 | AC-BKG-05 (ตรวจความเร็ว ไม่ได้ตรวจช่วงว่าง/30 วัน) | T-02 เสร็จ | backend/app/slots/service.py:list_available_slots; frontend/src/pages/SlotPicker.jsx | backend/tests/test_AC_BKG_05.py ผ่าน แต่ไม่ตรวจช่วง 30 วัน/จำนวนที่นั่ง; ไม่มี AC ที่ตรวจพฤติกรรมนี้ | ช่องโหว่ |
| FR-BKG-02 | AC-BKG-02 | T-04 พร้อมทำ | backend/app/booking/service.py:create_booking | ไม่มี test สำหรับ AC-BKG-02 | ยังไม่ถึง |
| FR-BKG-03 | AC-BKG-03 | T-05 พร้อมทำ; T-11 เสร็จ รอทีมตรวจ; T-12 พร้อมทำ | backend/app/booking/router.py:create_booking; frontend/src/pages/ConfirmBooking.jsx | frontend/src/__tests__/AC-BKG-03.test.jsx ผ่าน แต่ตรวจเฉพาะข้อความและจำนวนปุ่ม ไม่ตรวจเนื้อหาวัน/เวลา/ความใกล้ที่สุด | ช่องโหว่ |
| FR-BKG-04 | AC-BKG-01 | T-03 เสร็จ; T-06 รอ Q-02 | backend/app/booking/service.py:create_booking; backend/app/booking/router.py:create_booking | backend/tests/test_AC_BKG_01.py ผ่านแต่ตรวจเพียง status 201; ไม่ตรวจการบันทึก การตัดที่นั่ง หรือเลขคิว | ช่องโหว่ |
| FR-BKG-05 | AC-BKG-04 | T-07 พร้อมทำ | backend/app/booking/service.py:create_booking; backend/app/notify/queue.py:enqueue | ไม่มี test ของ AC-BKG-04; ยังไม่มี worker ส่ง/ส่งซ้ำ | ยังไม่ถึง |
| FR-BKG-06 | ไม่มี AC | T-02 เสร็จ; T-10 เสร็จ รอทีมตรวจ | backend/app/slots/service.py:list_available_slots; frontend/src/pages/SlotPicker.jsx | frontend/src/__tests__/SlotPicker.test.jsx ผ่าน (เปลี่ยนแพ็กเกจแล้วข้อมูลเปลี่ยน) แต่ spec ไม่มี AC สำหรับ FR นี้ | ช่องโหว่ |
| NFR-PERF-01 | AC-BKG-05 | T-02 เสร็จ | backend/app/slots/service.py:list_available_slots | backend/tests/test_AC_BKG_05.py ผ่าน แต่ยิง 200 request ต่อเนื่อง ไม่ได้ทดสอบผู้ใช้พร้อมกัน 200 คน | ช่องโหว่ |
| NFR-SEC-01 | ไม่มี AC | ไม่มี task | ไม่มีการตั้งค่า/ยืนยัน TLS ใน backend/app | ไม่มี test TLS | ยังไม่ถึง |
| NFR-REL-02 | AC-BKG-04 | T-07 พร้อมทำ | backend/app/notify/queue.py:NotificationQueue | ไม่มี test ของ AC-BKG-04; `retry_after_seconds` เป็นข้อมูลในคิว ไม่มีตัวทำ retry | ยังไม่ถึง |
| NFR-USE-01 | ไม่มี AC | ไม่มี task | ไม่มีการทดสอบ usability ตามเกณฑ์ผู้ใช้ใหม่ | ไม่มี test | ยังไม่ถึง |
| CON-TECH-01 | ไม่มี AC | T-01 เสร็จ | backend/app/config.py:DATABASE_URL; backend/app/db/session.py:engine | test schema ผ่านบน SQLite; ไม่ยืนยันการเชื่อมต่อ PostgreSQL จริง | ช่องโหว่ |
| DOM-PDPA-01 | AC-BKG-06 | T-01 เสร็จ; T-08 พร้อมทำ | backend/app/audit/middleware.py:AuditLogMiddleware.dispatch; backend/app/db/models.py:AuditLog | ไม่มี test AC-BKG-06; middleware กลืน error และไม่มีการควบคุมการเก็บอย่างน้อย 1 ปี | ช่องโหว่ |
| IF-IDP-01 | ไม่มี AC | T-03 เสร็จ | backend/app/auth/idp.py:get_verified_hn; backend/app/booking/router.py:create_booking | backend/tests/test_AC_BKG_01.py ผ่านด้วย token ที่มี prefix ตามที่จำลอง แต่ไม่ได้ตรวจผลจากระบบ IDP จริง | ช่องโหว่ |
| IF-HIS-01 | ไม่มี AC | T-01 เสร็จ; T-09 พร้อมทำ | backend/app/booking/router.py:BookingRequest/create_booking; backend/app/db/models.py:Booking | test schema ตรวจว่าไม่มีคอลัมน์ national_id แต่ request รับและ logger เขียน national_id ได้; ไม่มี HIS lookup | ช่องโหว่ |
| IF-NOT-01 | ไม่มี AC | T-07 พร้อมทำ | backend/app/notify/queue.py:NotificationQueue.enqueue | ไม่มี test; คิวเป็น in-memory และไม่มีตัวส่ง SMS/LINE แบบ asynchronous | ยังไม่ถึง |

## 2. ตามรอยย้อนกลับ (โค้ด ไป requirement)
| โค้ด (ไฟล์: ฟังก์ชัน หรือ endpoint) | อ้าง ID | ตรงกับข้อความใน spec ไหม | หมายเหตุ |
|---|---|---|---|
| backend/app/main.py:lifespan/app | CON-TECH-01 | บางส่วน | สร้างตาราง; engine ใช้ DATABASE_URL แต่ค่าเริ่มต้นเป็น SQLite |
| backend/app/slots/router.py:get_slots | FR-BKG-01, FR-BKG-06 | บางส่วน | GET /slots รับ package_code/date_from และคืนเวลา/remaining; ไม่มี date field ในรายการ UI |
| backend/app/slots/service.py:list_available_slots | FR-BKG-01, FR-BKG-06 | บางส่วน | กรองแพ็กเกจและ remaining > 0 ในช่วง start ถึง start + 30 วัน |
| backend/app/booking/router.py:create_booking | FR-BKG-04, IF-IDP-01, IF-HIS-01 | ไม่ครบ | POST /bookings ใช้ auth dependency แต่ request รับ national_id และ logger บันทึกค่านั้น |
| backend/app/booking/service.py:create_booking | FR-BKG-04, FR-BKG-03, FR-BKG-05, IF-NOT-01 | ไม่ครบ | เช็กที่นั่งว่าง แต่บรรทัดตัดที่นั่งถูกคอมเมนต์; แจ้งเตือนเข้า in-memory queue หลัง commit |
| backend/app/booking/service.py:next_queue_no | FR-BKG-04 | ไม่ตรง/รอ Q-02 | สร้างรูปแบบ `Q-001` ด้วยตัวเองทั้งที่ Q-02 ยังไม่ตอบ |
| backend/app/auth/idp.py:get_verified_hn | IF-IDP-01 | ไม่ครบ | ตรวจเพียง prefix `Bearer verified:` ไม่ตรวจ token กับระบบยืนยันตัวตนจริง |
| backend/app/audit/middleware.py:AuditLogMiddleware.dispatch | DOM-PDPA-01 | ไม่ครบ | เขียน log สำหรับ path /bookings แต่กลืน error; ไม่มีการบังคับเก็บไม่น้อยกว่า 1 ปี |
| backend/app/notify/queue.py:NotificationQueue.enqueue/pending | FR-BKG-05, IF-NOT-01, NFR-REL-02 | ยังไม่ถึง | เป็น deque ในหน่วยความจำ ไม่มีผู้ส่งหรือกลไก retry; T-07 ยังพร้อมทำ |
| frontend/src/App.jsx:App | FR-BKG-01, FR-BKG-03 | ไม่ครบ | ส่ง slot ให้หน้ายืนยันด้วยวันที่วันนี้และเวลา 09:00 ที่กำหนดคงที่ แทนข้อมูลช่วงที่เลือก |
| frontend/src/api/client.js:api.getSlots | FR-BKG-01, FR-BKG-06 | บางส่วน | เรียก GET /slots ตาม package/date แต่มี cancelBooking DELETE ที่อยู่นอก scope |
| frontend/src/api/client.js:api.createBooking | FR-BKG-03, FR-BKG-04 | ไม่ครบ | POST /bookings; UI คาดหวัง alternatives แต่ backend route ไม่ได้คืน alternatives เมื่อ 409 |
| frontend/src/api/client.js:api.cancelBooking | ไม่มี ID | ไม่ตรง | ส่ง DELETE /bookings/{id}; การยกเลิกอยู่ใน Out of scope แม้ backend ไม่มี endpoint แล้ว |
| frontend/src/pages/SlotPicker.jsx:SlotPicker | FR-BKG-01, FR-BKG-06 | ไม่ครบ | เปลี่ยนแพ็กเกจแล้วโหลดใหม่ แต่ข้อความเป็น “ว่าง N” และไม่แสดงวันที่ของแต่ละช่วง |
| frontend/src/pages/ConfirmBooking.jsx:ConfirmBooking | FR-BKG-03, FR-BKG-04 | บางส่วน | ข้อความเต็มและจำนวนสูงสุด 3 ตัวเลือกตรง; ไม่มี package ในรายละเอียดและไม่ตรวจความถูกต้อง/ลำดับ alternatives |
| frontend/src/__tests__/AC-BKG-03.test.jsx:test AC-BKG-03 | AC-BKG-03 | ไม่ครบ | ตรวจ alert text และจำนวนปุ่มเท่านั้น ไม่ assert วันเวลา/ความใกล้ที่สุด/ไม่มีการจองซ้อน |
| frontend/src/__tests__/SlotPicker.test.jsx:test FR-BKG-06 | FR-BKG-06 | บางส่วน | ยืนยันว่ารายการเวลาเปลี่ยนหลังเลือกแพ็กเกจ แต่ไม่มี AC รองรับ |
| backend/tests/test_AC_BKG_01.py:test_AC_BKG_01 | AC-BKG-01 | อ่อน | ตรวจเพียง HTTP 201; suite ยังผ่านทั้งที่การตัดที่นั่งถูกคอมเมนต์ |
| backend/tests/test_AC_BKG_05.py:test_AC_BKG_05 | AC-BKG-05 | อ่อน | ยิง request ต่อเนื่อง ไม่ใช่พร้อมกันตาม Then |
| backend/tests/test_T01_schema.py:test_T01_* | CON-TECH-01, IF-HIS-01, DOM-PDPA-01 | บางส่วน | ตรวจ schema บน SQLite และไม่มีคอลัมน์ national_id; ไม่ยืนยัน PostgreSQL หรือ logging/retention |

## 3. ข้อค้นพบ
ชนิด: AC ไม่มี test / test อ่อน / โค้ดไม่มี FR / FR ไม่มี AC / เดา Q-xx / ละเมิด Constraint / ตัวเลขไม่ตรง spec / อ้าง ID ผิดเรื่อง / ของแถม / ไม่ตรง mockup / mockup เกิน spec
ทีมตัดสิน: แก้โค้ด / แก้ spec / เพิ่ม Q-xx / ไม่ใช่ปัญหา (พร้อมเหตุผล 1 บรรทัด)

| F-ID | ชนิด | อยู่ที่ | ขัดกับ | รายละเอียด | ทีมตัดสิน |
|---|---|---|---|---|---|
| F-002 | FR ไม่มี AC | specs/001-booking/spec.md / frontend/src/pages/SlotPicker.jsx | FR-BKG-06 | FR-BKG-06 ไม่มี AC ใน spec; test หน้าจอมีอยู่แต่ไม่ได้ทดแทน acceptance criteria ที่ทีมอนุมัติ |  |
| F-003 | เดา Q-xx | backend/app/booking/service.py:next_queue_no | FR-BKG-04, Q-02 | ยังคำนวณ `Q-{count+1:03d}` เอง ทั้งที่ Q-02 ยังไม่ตอบและ plan ระบุว่ายังไม่สร้างวิธีออกเลข |  |
| F-004 | ละเมิด Constraint | backend/app/audit/middleware.py:AuditLogMiddleware.dispatch | DOM-PDPA-01 | middleware กลืนข้อผิดพลาดในการเขียน log และไม่มีการบังคับเก็บ log ไม่น้อยกว่า 1 ปี จึงยืนยันการบันทึกครบทุกครั้งไม่ได้ |  |
| F-007 | test อ่อน | backend/tests/test_AC_BKG_01.py:test_AC_BKG_01 | AC-BKG-01 | ตรวจแค่ `status_code == 201` ไม่ตรวจบันทึก หมายเลขคิว หรือ remaining; จึงไม่จับการตัดที่นั่งที่หายไป |  |
| F-008 | โค้ดไม่มี FR | backend/app/booking/service.py:create_booking | FR-BKG-04 | บรรทัด `slot.remaining -= 1` ถูกคอมเมนต์ ทำให้จองสำเร็จโดยไม่ตัดที่นั่ง; pytest ผ่านเพราะ test ตรวจเพียง status 201 |  |
| F-009 | ละเมิด Constraint | backend/app/booking/router.py:BookingRequest/create_booking | IF-HIS-01 | request model รับ `national_id` และ logger เขียนค่าเต็มลง log แม้ constraint กำหนดให้ใช้ HN ภายในและไม่เก็บเลขบัตรประชาชน |  |
| F-010 | ละเมิด Constraint | backend/app/auth/idp.py:get_verified_hn | IF-IDP-01 | ยอมรับ token จาก prefix `Bearer verified:` โดยไม่ตรวจผลยืนยันตัวตนจากระบบ IDP; implementation ระบุเองว่าเป็นการจำลอง ทั้งที่ T-03 ถูกทำเสร็จแล้ว |  |
| F-011 | ของแถม | frontend/src/api/client.js:api.cancelBooking | Out of scope: ยกเลิกคิว | ยังมีฟังก์ชันส่ง DELETE /bookings/{id} ทั้งที่การยกเลิกอยู่ใน Out of scope; backend ไม่มี endpoint นี้แล้ว |  |
| F-012 | test อ่อน | frontend/src/__tests__/AC-BKG-03.test.jsx | AC-BKG-03 | test ตรวจข้อความและจำนวนปุ่ม แต่ไม่ตรวจวัน/เวลาในตัวเลือก ความใกล้ 09.00 น. หรือไม่มีการจองซ้อน ทั้งที่ T-11 เสร็จรอทีมตรวจ |  |
| F-013 | test อ่อน | backend/tests/test_AC_BKG_05.py:test_AC_BKG_05 | AC-BKG-05, NFR-PERF-01 | วัด 200 request แบบเรียงต่อกัน ไม่ได้ทดสอบผู้ใช้พร้อมกัน 200 คนตาม Given |  |
| F-014 | FR ไม่มี AC | specs/001-booking/spec.md:AC-BKG-05 | FR-BKG-01 | FR-BKG-01 ต้องแสดงช่วงเวลาว่างภายใน 30 วันพร้อมที่นั่งคงเหลือ แต่ AC-BKG-05 ตรวจเฉพาะ p95 จึงไม่มี AC ที่ตรวจ FR นี้โดยตรง |  |
| F-015 | ไม่ตรง mockup | frontend/src/pages/SlotPicker.jsx:SlotPicker | UI-BKG-01, FR-BKG-01 | UI ที่ต้องตรงกำหนดคำว่า “เหลือ N ที่”; ปัจจุบันแสดง “ว่าง N” และไม่แสดงวันที่กำกับแต่ละช่วงเวลา |  |
| F-016 | mockup เกิน spec | specs/001-booking/mockups/UI-BKG-01-select-slot.html | spec.md: หน้าจอ (UI) | mockup มีตัวเลือก “แจ้งเตือนก่อนวันตรวจ 1 วัน” แต่ไม่มี FR/ข้อกำหนด UI รองรับ; ไม่ควรถือเป็นงานที่ขาด ให้ทีมถาม PO |  |
| F-017 | test อ่อน | backend/tests/test_T01_schema.py | CON-TECH-01 | test สร้าง schema บน SQLite ตามแผนทดสอบ แต่ไม่ยืนยันว่า runtime เชื่อม PostgreSQL ตาม constraint; ต้องตรวจ environment ระบบจริง |  |
| Q-03 | Open Question | spec.md: Constraints / IF-HIS-01 | IF-HIS-01, DOM-PDPA-01 | ถามฝ่าย IT ของโรงพยาบาล: Log ของระบบเก็บเลขบัตรประชาชนได้ไหม หรือ IF-HIS-01 ต้องครอบคลุม log ด้วย? |  |
| Q-04 | Open Question | spec.md: FR-BKG-01, FR-BKG-06 | FR-BKG-01, FR-BKG-06 | ถามพยาบาลคัดกรอง: เกณฑ์ยอมรับของ "แสดง 30 วัน" และ "เปลี่ยนแพ็กเกจแล้วคำนวณช่วงว่างใหม่" ควรเป็นอย่างไร? |  |

## 4. แก้แล้ว
| F-ID | แก้อย่างไร | รู้ได้อย่างไร |
|---|---|---|
| F-001 | ปรับ DAYS_AHEAD จาก 14 เป็น 30 ตาม FR-BKG-01 | ตรวจ backend/app/slots/service.py พบ DAYS_AHEAD = 30; ยังมี Q-04 เรื่องเกณฑ์ acceptance ของช่วงวัน |
| F-005 | ปิดข้อค้นพบเดิมที่นับงาน T-07 ซึ่งยังพร้อมทำเป็นข้อค้นพบ; รายงานสถานะเป็น “ยังไม่ถึง” แทน | ตรวจ tasks.md พบ T-07 พร้อมทำ; queue ที่เพิ่มเป็นเพียง in-memory enqueue ยังไม่มี sender/retry ตามรายการที่ยังต้องทำ |
| F-006 | ปิดข้อค้นพบเดิมที่นับ AC ของ task ยังไม่เสร็จเป็น “AC ไม่มี test”; รายงานตามสถานะ task | ตรวจ tasks.md: T-05/T-07/T-08 พร้อมทำ และพบ frontend test AC-BKG-03 แล้ว; จึงไม่เข้าเกณฑ์ข้อค้นพบตาม verify prompt |
