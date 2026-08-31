import json
import random
import os
import telebot
from apscheduler.schedulers.background import BackgroundScheduler
from database import get_all_users, remove_user

AZKAR_FILE = os.path.join(os.path.dirname(__file__), 'data', 'azkar.json')

def load_periodic_azkar():
    """تحميل قائمة التذكيرات الدورية من ملف JSON."""
    try:
        with open(AZKAR_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('periodic_reminders', [])
    except Exception as e:
        print(f"خطأ أثناء قراءة ملف الأذكار: {e}")
        return []

def send_periodic_zkr(bot: telebot.TeleBot):
    """إرسال تذكير عشوائي لكل المستخدمين كل ساعتين."""
    azkar_list = load_periodic_azkar()
    if not azkar_list:
        return

    selected_zkr = random.choice(azkar_list)
    users = get_all_users()

    message = f"✨ **تذكير دوري** ✨\n\n{selected_zkr['text']}\n\n🤲 لا تنسنا من صالح دعائك."

    for user_id in users:
        try:
            bot.send_message(user_id, message, parse_mode='Markdown')
        except telebot.apihelper.ApiTelegramException as e:
            # إذا حظر المستخدم البوت أو حذف حسابه يتم مسحه من قاعدة البيانات
            if e.error_code in [403, 400]:
                remove_user(user_id)
        except Exception as e:
            print(f"فشل الإرسال للمستخدم {user_id}: {e}")

def start_scheduler(bot: telebot.TeleBot):
    """بدء مؤقت الإرسال التلقائي كل ساعتين."""
    scheduler = BackgroundScheduler(timezone="UTC")
    # تعيين التكرار كل ساعتين (hours=2)
    scheduler.add_job(send_periodic_zkr, 'interval', hours=2, args=[bot])
    scheduler.start()
    print("تم تشغيل جدول التذكيرات التلقائية (كل ساعتين).")
