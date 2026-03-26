from flask import Blueprint, jsonify, request
from mysql.connector import Error

from db import get_db_cursor
from utils.validators import validate_inquiry_payload

inquiries_bp = Blueprint("inquiries", __name__)


@inquiries_bp.get("/health")
def health_check():
    return jsonify({"status": "ok", "service": "s-residence-backend"}), 200


@inquiries_bp.post("/inquiries")
def create_inquiry():
    payload = request.get_json(silent=True) or {}
    validation_result = validate_inquiry_payload(payload)

    if validation_result["errors"]:
        return (
            jsonify(
                {
                    "message": "ข้อมูลไม่ถูกต้อง กรุณาตรวจสอบอีกครั้ง",
                    "errors": validation_result["errors"],
                }
            ),
            422,
        )

    inquiry_data = validation_result["data"]

    query = """
        INSERT INTO inquiries (
            full_name, phone, email, preferred_building,
            preferred_date, preferred_time, message, consent, status
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'new')
    """
    values = (
        inquiry_data["full_name"],
        inquiry_data["phone"],
        inquiry_data["email"],
        inquiry_data["preferred_building"],
        inquiry_data["preferred_date"],
        inquiry_data["preferred_time"],
        inquiry_data["message"],
        inquiry_data["consent"],
    )

    try:
        with get_db_cursor(dictionary=True) as (_, cursor):
            cursor.execute(query, values)
            inquiry_id = cursor.lastrowid
    except Error:
        return (
            jsonify({"message": "ระบบไม่สามารถบันทึกข้อมูลได้ในขณะนี้ กรุณาลองใหม่อีกครั้ง"}),
            500,
        )

    return (
        jsonify(
            {
                "message": "บันทึกคำขอนัดดูห้องเรียบร้อยแล้ว",
                "data": {
                    "id": inquiry_id,
                    "status": "new",
                },
            }
        ),
        201,
    )


@inquiries_bp.get("/inquiries")
def list_inquiries():
    limit = min(max(request.args.get("limit", default=20, type=int), 1), 100)

    try:
        with get_db_cursor(dictionary=True) as (_, cursor):
            cursor.execute(
                """
                SELECT id, full_name, phone, email, preferred_building,
                       preferred_date, preferred_time, message, consent, status,
                       created_at, updated_at
                FROM inquiries
                ORDER BY created_at DESC
                LIMIT %s
                """,
                (limit,),
            )
            rows = cursor.fetchall()
    except Error:
        return jsonify({"message": "ไม่สามารถดึงข้อมูลคำขอได้"}), 500

    return jsonify({"data": rows, "count": len(rows)}), 200
