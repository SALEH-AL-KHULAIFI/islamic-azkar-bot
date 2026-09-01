import os
import sqlite3
import psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_connection():
    if DATABASE_URL:
        # الاتصال بقاعدة بيانات PostgreSQL على Railway
        return psycopg2.connect(DATABASE_URL)
    else:
        # الاتصال المحلي بقاعدة SQLite
        os.makedirs("data", exist_ok=True)
        return sqlite3.connect("data/users.db")

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    if DATABASE_URL:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id BIGINT PRIMARY KEY
            )
        """)
    else:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY
            )
        """)
    conn.commit()
    cursor.close()
    conn.close()

def add_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        if DATABASE_URL:
            cursor.execute("INSERT INTO users (user_id) VALUES (%s) ON CONFLICT (user_id) DO NOTHING", (user_id,))
        else:
            cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [row[0] for row in rows]

def remove_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        if DATABASE_URL:
            cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        else:
            cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()
