# RTM: จองคิวตรวจสุขภาพ (Booking)
อ้างอิง: spec.md Draft v2 | tasks.md | test-cases.md
สร้างด้วย /verify เมื่อ 2569-10-07 00:30 | test: 4 ผ่าน 1 ไม่ผ่าน

## 1. ตามรอยไปข้างหน้า (requirement ไป โค้ด ไป test)
| ID | AC | task | โค้ด (ไฟล์: ฟังก์ชัน) | test (ผล) | สถานะ |
|---|---|---|---|---|---|
| FR-BKG-01 | ไม่มี AC | T-02 | backend/app/slots/service.py:list_available_slots; backend/app/slots/router.py:get_slots | backend/tests/test_AC_BKG_05.py: ผ่าน (ตรวจความเร็ว ไม่ใช่ 30 วัน/ถี่) | ช่องโหว่ |
| FR-BKG-02 | AC-BKG-02 | T-04 | backend/app/booking/service.py:create_booking | ไม่มี test ใน backend/tests/ | ยังไม่ถึง |
| FR-BKG-03 | AC-BKG-03 | T-05, T-11, T-12 | ไม่มีโค้ดที่ให้ 3 ตัวเลือกเมื่อเต็ม | ไม่มี test ใน backend/tests/ และ frontend/src/__tests__/ | ยังไม่ถึง |
| FR-BKG-04 | AC-BKG-01 | T-03, T-06 | backend/app/booking/service.py:create_booking; backend/app/booking/router.py:create_booking | backend/tests/test_AC_BKG_01.py: ผ่าน (status 201) แต่ไม่มี assert ที่ตรวจ queue_no/remaining | รอ Q-xx |
| FR-BKG-05 | AC-BKG-04 | T-07 | ไม่มีคิวส่งซ้ำ / ไม่มี callback ส่งข้อความ | ไม่มี test ใน backend/tests/ | ยังไม่ถึง |
| FR-BKG-06 | ไม่มี AC | T-10 | backend/app/slots/service.py:list_available_slots; backend/app/slots/router.py:get_slots | ไม่มี test ใน frontend/src/__tests__/ | ช่องโหว่ |
| NFR-PERF-01 | AC-BKG-05 | T-02 | backend/app/slots/service.py:list_available_slots | backend/tests/test_AC_BKG_05.py: ผ่าน (p95 <= 2s) | ครบ |
| NFR-SEC-01 | ไม่มี AC | ไม่มี task | ไม่มีโค้ด TLS / HTTPS / secure transport | ไม่มี test | ยังไม่ถึง |
| NFR-REL-02 | AC-BKG-04 | T-07 | ไม่มี queue retry / reschedule logic | ไม่มี test | ยังไม่ถึง |
| NFR-USE-01 | ไม่มี AC | ไม่มี task | ไม่มีโค้ดวัดประสิทธิภาพ/UX แบบผู้ใช้ใหม่ | ไม่มี test | ยังไม่ถึง |
| CON-TECH-01 | ไม่มี AC | T-01 | backend/app/config.py:DATABASE_URL; backend/app/db/session.py:engine | backend/tests/test_T01_schema.py: ผ่าน | ครบ |
| DOM-PDPA-01 | AC-BKG-06 | T-08 | ไม่มี audit middleware / audit log writer | backend/tests/test_AC_BKG_06.py: ไม่มีไฟล์ | ยังไม่ถึง |
| IF-IDP-01 | ไม่มี AC | T-03 | backend/app/auth/idp.py:get_verified_hn | backend/tests/test_AC_BKG_01.py: ผ่านทาง implied auth dependency | ครบ |
| IF-HIS-01 | ไม่มี AC | T-09 | backend/app/db/models.py:Booking (เก็บเฉพาะ hn) แต่ไม่มี HIS lookup | ไม่มี test | ยังไม่ถึง |
| IF-NOT-01 | ไม่มี AC | T-07 | ไม่มีคิวส่งข้อความ asynchronous / retry queue | ไม่มี test | ยังไม่ถึง |

## 2. ตามรอยย้อนกลับ (โค้ด ไป requirement)
| โค้ด (ไฟล์: ฟังก์ชัน หรือ endpoint) | อ้าง ID | ตรงกับข้อความใน spec ไหม | หมายเหตุ |
|---|---|---|---|
| backend/app/slots/service.py:list_available_slots | FR-BKG-01, FR-BKG-06 | ไม่ครบ | กำหนด `DAYS_AHEAD = 14` แต่ spec ระบุ 30 วันข้างหน้า และไม่มีการทดสอบ 30 วัน |
| backend/app/slots/router.py:get_slots | FR-BKG-01, FR-BKG-06 | ไม่ครบ | เรียก `package_code` ได้จริง แต่ไม่มี AC/ UI ที่ยืนยันการคำนวณช่วงเวลาใหม่ตามแพ็กเกจที่เปลี่ยน |
| backend/app/booking/service.py:create_booking | FR-BKG-04 | ยังไม่ครบ | `queue_no` ใช้ `A{count+1:03d}` โดยเดาเองจาก Q-02 ที่ยังไม่ได้รับคำตอบ |
| backend/app/booking/router.py:create_booking | FR-BKG-04, IF-IDP-01 | ส่วนใหญ่ตรง | ตรวจ auth ผ่าน dependency และคืน queue_no แต่ test ยังไม่ตรวจ payload ที่สำคัญ เช่น หมายเลขคิวและ remaining |
| backend/app/auth/idp.py:get_verified_hn | IF-IDP-01 | ตรง | ตรวจ Header `Authorization` และปฏิเสธเมื่อไม่มี token อย่างชัดเจน |
| backend/app/config.py:DATABASE_URL | CON-TECH-01 | ตรงบรรทัดหลัก | ตั้งค่า PostgreSQL ในระบบจริง แต่ค่าเริ่มต้นเก็บ SQLite เพื่อความสะดวกในการทดสอบที่ Codespace |
| backend/app/db/models.py:Booking | IF-HIS-01, DOM-PDPA-01 | ไม่ครบ | เก็บ `hn` อย่างเดียว แต่ไม่มี HIS lookup และไม่มี audit middleware ที่บันทึกทุก access |
| frontend/src/api/client.js:api.getSlots / api.createBooking | FR-BKG-01, FR-BKG-04 | ไม่ครบ | สัญญา API มีอยู่ แต่ไม่มีหน้าจอจริงและไม่มี test สำหรับผลลัพธ์ที่สำคัญ |

## 3. ข้อค้นพบ
ชนิด: AC ไม่มี test / test อ่อน / โค้ดไม่มี FR / FR ไม่มี AC / เดา Q-xx / ละเมิด Constraint / ตัวเลขไม่ตรง spec / อ้าง ID ผิดเรื่อง
ทีมตัดสิน: แก้โค้ด / แก้ spec / เพิ่ม Q-xx / ไม่ใช่ปัญหา (พร้อมเหตุผล 1 บรรทัด)

| F-ID | ชนิด | อยู่ที่ | ขัดกับ | รายละเอียด | ทีมตัดสิน |
|---|---|---|---|---|---|
| F-001 | ตัวเลขไม่ตรง spec | backend/app/slots/service.py:DAYS_AHEAD = 14 | FR-BKG-01 | spec ระบุ "ภายใน 30 วันข้างหน้า" แต่โค้ดแสดงแค่ 14 วัน ทำให้ข้อมูลไม่ครบตาม spec |  |
| F-002 | FR ไม่มี AC | specs/001-booking/spec.md / backend/app/slots/service.py | FR-BKG-06 | spec มี FR-BKG-06 แต่ไม่มี AC/ test ที่ตรวจว่าเมื่อเปลี่ยนแพ็กเกจ ควรคำนวณช่วงว่างใหม่ตามแพ็กเกจที่เลือก |  |
| F-003 | เดา Q-xx | backend/app/booking/service.py:next_queue_no | FR-BKG-04, Q-02 | โค้ดใช้ `A001` แบบเดาเอง ขณะที่ Q-02 ยังไม่ได้คำตอบจากเจ้าหน้าที่เวชระเบียน จึงเป็นการตัดสินใจแทนทีม |  |
| F-004 | ละเมิด Constraint | ไม่มีไฟล์ middleware / audit log writer | DOM-PDPA-01 | โค้ดมีตาราง `audit_logs` แต่ไม่มี code ที่บันทึกทุกการเข้าถึงข้อมูลการจอง ทำให้ constraint ไม่เป็นจริงในระบบ |  |
| F-005 | โค้ดไม่มี FR | backend/app/booking/service.py:create_booking | FR-BKG-05, IF-NOT-01 | ไม่มี retry queue / message async handling แม้ spec บอกให้ส่งข้อความยืนยันผ่านคิวและคงบันทึกการจองแม้ส่งไม่สำเร็จ |  |
| F-006 | AC ไม่มี test | specs/001-booking/test-cases.md / backend/tests/ | AC-BKG-03, AC-BKG-04, AC-BKG-06 | มี AC หลายข้อ แต่ tasks ที่ตรวจเป็น "พร้อมทำ" หรือ "ยังไม่ถึง" และไม่มี code/test ที่ตรวจจริง |  |
| F-007 | test อ่อน | backend/tests/test_AC_BKG_01.py:test_AC_BKG_01 | AC-BKG-01 | test ตรวจแค่ `status_code == 201` ไม่ดูว่า `remaining` ลดลงจริง, `queue_no` มีค่า และบันทึกถูกต้องตาม Then |  |

## 4. แก้แล้ว
| F-ID | แก้อย่างไร | รู้ได้อย่างไร |
|---|---|---|
