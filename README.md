# S Residence Website System

เว็บไซต์สำหรับธุรกิจอพาร์ตเมนต์ให้เช่า **S Residence (Sukhumvit 101, Bangkok)** ที่ออกแบบให้เน้นการติดต่อและนัดดูห้องอย่างรวดเร็ว พร้อมระบบบันทึกลีดจริงผ่านฟอร์มเชื่อมต่อ Flask + MySQL

## Business Overview
S Residence เป็นอพาร์ตเมนต์ให้เช่าที่สุขุมวิท 101 ซอยปุณณวิถี 9 โดยข้อมูลธุรกิจที่เว็บไซต์ใช้มีดังนี้:
- ระยะทางจาก BTS ปุณณวิถีประมาณ 800 เมตร
- ค่าวินมอเตอร์ไซค์ประมาณ 10 บาท
- ห้องแบบเดียว ขนาด 25 ตร.ม. พร้อมระเบียงส่วนตัว
- เฟอร์นิเจอร์: โต๊ะวางทีวี, โต๊ะเครื่องแป้ง, เตียง, ที่นอน, ตู้เสื้อผ้า
- ราคาเช่า: ตึก A = 6,500 บาท/เดือน, ตึก B = 7,500 บาท/เดือน
- เวลาดูห้อง: ทุกวัน 10:00–18:00 ยกเว้นวันเสาร์
- โทร: 061-451-8888
- แผนที่: https://goo.gl/maps/AFzSj5dnsjn3LQNQ6

## Features
- Thai-first conversion-focused landing experience
- Poster-inspired UI ด้วย navy + white + yellow
- Responsive sections ครบ: hero, highlights, about, room details, pricing, furniture, gallery, location, CTA, inquiry form
- Client-side form validation + anti-duplicate ส่งซ้ำทันที
- Flask REST API สำหรับสุขภาพระบบและรับ inquiry
- Server-side validation + sanitize ก่อนบันทึก
- MySQL schema พร้อมใช้งานและรองรับสถานะ inquiry
- โครงสร้างโปรเจกต์พร้อมขยายเป็น admin dashboard ได้ในอนาคต

## Tech Stack
- Frontend: HTML, CSS, JavaScript
- Backend: Python (Flask)
- Database: MySQL

## Project Structure
```text
project-root/
│
├── frontend/
│   ├── index.html
│   ├── styles.css
│   ├── script.js
│   └── assets/
│       ├── images/
│       └── icons/
│
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── db.py
│   ├── requirements.txt
│   ├── .env.example
│   ├── routes/
│   │   └── inquiries.py
│   ├── utils/
│   │   └── validators.py
│   └── README.md
│
├── database/
│   └── init.sql
│
├── .gitignore
└── README.md
```

## Setup Guide

### 1) Clone and enter project
```bash
git clone <your-repo-url>
cd web_condo
```

### 2) MySQL Setup
1. เปิด MySQL (เช่นผ่าน XAMPP)
2. รันไฟล์ SQL:
```bash
mysql -u root < database/init.sql
```

### 3) Backend Setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

ค่าที่กำหนดไว้ล่วงหน้าใน `.env` (พร้อมใช้งาน local):
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=""
DB_NAME=s_residence_db
```

### 4) Run Backend
```bash
python app.py
```
Backend endpoint จะพร้อมที่ `http://127.0.0.1:5000`

### 5) Serve Frontend
เปิดอีก terminal:
```bash
cd frontend
python -m http.server 5500
```
จากนั้นเข้า `http://127.0.0.1:5500`

## API Summary

### `GET /api/health`
ตรวจสอบสถานะ backend

**Response 200**
```json
{
  "status": "ok",
  "service": "s-residence-backend"
}
```

### `POST /api/inquiries`
บันทึกคำขอนัดดูห้อง

**Request Body**
```json
{
  "full_name": "ชื่อผู้ติดต่อ",
  "phone": "0614518888",
  "email": "user@example.com",
  "preferred_building": "A",
  "preferred_date": "2026-04-01",
  "preferred_time": "14:00",
  "message": "ต้องการนัดดูห้อง",
  "consent": true
}
```

### `GET /api/inquiries?limit=20`
ดึงรายการ inquiry (รองรับต่อยอดทำหลังบ้าน)

## Future Upgrade Ideas
- Admin login / RBAC
- Inquiry dashboard + filters
- Room availability tracking
- Multi-room-type support
- CMS สำหรับจัดการรูปและคอนเทนต์
- LINE notification integration
- Email notification workflow
- Booking approval flow
- Tenant records and lifecycle management

## Troubleshooting
- หากเชื่อมต่อ DB ไม่ได้: ตรวจสอบว่า MySQL รันอยู่และใช้ DB_NAME `s_residence_db`
- หาก CORS block: ตั้งค่า `CORS_ORIGINS` ใน `backend/.env`
- หาก POST form ไม่สำเร็จ: ตรวจสอบว่า backend รันอยู่ที่พอร์ต 5000 และ frontend เรียก URL เดียวกันใน `frontend/script.js`
