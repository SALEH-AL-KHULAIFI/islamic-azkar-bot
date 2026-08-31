import sqlite3
import os

# حفظ قاعدة البيانات داخل مجلد data لسهولة ربطها مع Volumes في Railway
DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'users.db')

def get_connection():
    """إنشاء اتصال بقاعدة البيانات مع التأكد من وجود المجلد."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    """إنشاء جدول المستخدمين في حال عدم وجوده."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def add_user(user_id: int) -> bool:
    """إضافة مستخدم جديد إلى قاعدة البيانات دون تكرار."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT OR IGNORE INTO users (user_id) VALUES (?)', (user_id,))
        conn.commit()
        added = cursor.rowcount > 0
        conn.close()
        return added
    except Exception as e:
        print(f"خطأ أثناء إضافة المستخدم {user_id}: {e}")
        return False

def get_all_users() -> list:
    """جلب قائمة بكل معرفات المستخدمين للإرسال التلقائي."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT user_id FROM users')
        rows = cursor.fetchall()
        conn.close()
        return [row[0] for row in rows]
    except Exception as e:
        print(f"خطأ أثناء جلب قائمة المستخدمين: {e}")
        return []

def remove_user(user_id: int):
    """حذف مستخدم (في حال قام بحظر البوت لتجنب فشل الإرسال المستمر)."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"خطأ أثناء حذف المستخدم {user_id}: {e}")
