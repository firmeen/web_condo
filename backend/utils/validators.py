import html
import re
from datetime import datetime, date

ALLOWED_BUILDINGS = {"A", "B", "No preference", ""}


def sanitize_text(value: str, max_length: int = 255) -> str:
    if value is None:
        return ""
    cleaned = html.escape(str(value).strip())
    return cleaned[:max_length]


def parse_date(value: str):
    if not value:
        return None

    try:
        parsed = datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None

    if parsed < date.today():
        return None
    return parsed


def parse_time(value: str):
    if not value:
        return None

    if not re.fullmatch(r"^([01]\d|2[0-3]):([0-5]\d)$", value):
        return None
    return value


def validate_inquiry_payload(payload):
    errors = {}

    full_name = sanitize_text(payload.get("full_name"), max_length=255)
    phone = sanitize_text(payload.get("phone"), max_length=50)
    email = sanitize_text(payload.get("email"), max_length=255)
    preferred_building = sanitize_text(payload.get("preferred_building"), max_length=50)
    preferred_time = sanitize_text(payload.get("preferred_time"), max_length=50)
    message = sanitize_text(payload.get("message"), max_length=2000)
    consent = bool(payload.get("consent", False))

    if len(full_name) < 2:
        errors["full_name"] = "กรุณากรอกชื่อ-นามสกุลให้ครบถ้วน"

    normalized_phone = re.sub(r"[\s()-]", "", phone)
    if not re.fullmatch(r"^\+?[0-9]{8,15}$", normalized_phone):
        errors["phone"] = "กรุณากรอกเบอร์โทรศัพท์ให้ถูกต้อง"

    if email and not re.fullmatch(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
        errors["email"] = "รูปแบบอีเมลไม่ถูกต้อง"

    if preferred_building not in ALLOWED_BUILDINGS:
        errors["preferred_building"] = "กรุณาเลือกตึกที่ถูกต้อง"

    parsed_date = parse_date(payload.get("preferred_date", ""))
    if payload.get("preferred_date") and parsed_date is None:
        errors["preferred_date"] = "วันที่เข้าชมต้องเป็นวันนี้หรืออนาคต"

    parsed_time = parse_time(preferred_time)
    if preferred_time and parsed_time is None:
        errors["preferred_time"] = "รูปแบบเวลาไม่ถูกต้อง (HH:MM)"

    if not consent:
        errors["consent"] = "ต้องยินยอมให้ติดต่อกลับก่อนส่งข้อมูล"

    return {
        "errors": errors,
        "data": {
            "full_name": full_name,
            "phone": normalized_phone,
            "email": email or None,
            "preferred_building": preferred_building or None,
            "preferred_date": parsed_date,
            "preferred_time": parsed_time,
            "message": message or None,
            "consent": consent,
        },
    }
