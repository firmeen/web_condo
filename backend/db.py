from contextlib import contextmanager

import mysql.connector
from mysql.connector import Error

from config import config


def create_connection():
    return mysql.connector.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME,
        autocommit=False,
    )


@contextmanager
def get_db_cursor(dictionary=False):
    conn = None
    cursor = None
    try:
        conn = create_connection()
        cursor = conn.cursor(dictionary=dictionary)
        yield conn, cursor
        conn.commit()
    except Error:
        if conn:
            conn.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
