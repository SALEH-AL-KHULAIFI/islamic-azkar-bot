import os
import sqlite3
import psycopg2

# جلب رابط قاعدة البيانات مع إزالة الفراغات إن وجدت
DATABASE_URL = os.environ.get("DATABASE_URL", "").strip()

# تصحيح بادئة الرابط إذا كانت بـ postgres:// لتوافق psycopg2
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

def get_connection():
    """إنشاء اتصال مع قاعدة البيانات بناءً على البيئة الحالية"""
    if DATABASE_URL:
        return psycopg2.connect(DATABASE_URL)
    else:
        os.makedirs("data", exist_ok=True)
        return sqlite3.connect("data/users.db")

def init_db():
    """إنشاء الجدول عند بدء التشغيل إذا لم يكن موجوداً"""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        if DATABASE_URL:
            print("DATABASE CHECK: Connected to PostgreSQL successfully.")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id BIGINT PRIMARY KEY
                )
            """)
        else:
            print("DATABASE WARNING: Connected to local SQLite (Users may reset on restart!).")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY
                )
            """)
            
        conn.commit()
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def add_user(user_id):
    """إضافة مشترك جديد"""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        if DATABASE_URL:
            cursor.execute(
                "INSERT INTO users (user_id) VALUES (%s) ON CONFLICT (user_id) DO NOTHING",
                (user_id,)
            )
        else:
            cursor.execute(
                "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
                (user_id,)
            )
        conn.commit()
    except Exception as e:
        print(f"Error adding user {user_id}: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_all_users():
    """جلب جميع المشتركين"""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users")
        rows = cursor.fetchall()
        return [row[0] for row in rows]
    except Exception as e:
        print(f"Error fetching users: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def remove_user(user_id):
    """حذف مشترك (عند حظر البوت مثلاً)"""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        if DATABASE_URL:
            cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        else:
            cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        conn.commit()
    except Exception as e:
        print(f"Error removing user {user_id}: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
