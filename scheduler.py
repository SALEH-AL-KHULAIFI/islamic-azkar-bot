import json
import random
import time
from apscheduler.schedulers.background import BackgroundScheduler
from database import get_all_users, remove_user

def load_all_azkar():
    """تحميل واستخراج كافة نصوص الأذكار والأدعية من جميع الأقسام بنجاح"""
    try:
        with open("data/azkar.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        all_texts = []

        # 1. استخراج الأذكار من التذكيرات الدورية
        for item in data.get("periodic_reminders", []):
            if isinstance(item, dict) and "text" in item:
                all_texts.append(item["text"])

        # 2. استخراج الأذكار من كافة التصنيفات (morning, evening, etc.)
        categories = data.get("categories", {})
        for cat_key, cat_list in categories.items():
            if isinstance(cat_list, list):
                for item in cat_list:
                    if isinstance(item, dict) and "text" in item:
                        all_texts.append(item["text"])

        # إزالة التكرارات
        return list(set(all_texts))
    except Exception as e:
        print(f"Error loading azkar: {e}")
        return []

def send_hourly_reminder(bot):
    azkar_pool = load_all_azkar()
    if not azkar_pool:
        print("تحذير: لم يتم العثور على أذكار في القائمة.")
        return
    
    # اختيار ذكر أو دعاء عشوائي
    random_zekr = random.choice(azkar_pool)
    message_text = f"✨ **تذكير الساعة** ✨\n\n{random_zekr}"

    users = get_all_users()
    print(f"جاري إرسال التذكير الدوري إلى {len(users)} مستخدم...")

    for user_id in users:
        try:
            bot.send_message(chat_id=user_id, text=message_text, parse_mode="Markdown")
            time.sleep(0.05)  # تفادي حظر المعدل (Rate Limit)
        except Exception as e:
            print(f"فشل الإرسال للمستخدم {user_id}، جاري الحذف: {e}")
            remove_user(user_id)

def start_scheduler(bot):
    scheduler = BackgroundScheduler()
    # إرسال تذكير كل ساعة
    scheduler.add_job(send_hourly_reminder, 'interval', hours=1, args=[bot])
    scheduler.start()
    print("تم تفعيل مجدول التذكيرات الساعية بنجاح.")
