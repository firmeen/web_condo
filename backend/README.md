# Backend - S Residence

Flask API สำหรับรับและจัดเก็บคำขอนัดดูห้องลง MySQL

## Quick Start
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```

## Environment Defaults
```env
DEBUG=false
HOST=0.0.0.0
PORT=5000
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=""
DB_NAME=s_residence_db
CORS_ORIGINS=*
```

## Routes
- `GET /api/health`
- `POST /api/inquiries`
- `GET /api/inquiries?limit=20`
