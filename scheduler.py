import json
import random
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database import get_all_users, remove_user

def load_all_azkar():
    """تحميل دمج كافة الأذكار والأدعية من جميع الأقسام لمنع التكرار وزيادة التنوع"""
    try:
        with open("data/azkar.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        all_items = []
        for category_name, items in data.items():
            if isinstance(items, list):
                all_items.extend(items)
        
        # إزالة التكرارات إن وجدت
        return list(set(all_items))
    except Exception as e:
        print(f"Error loading azkar: {e}")
        return []

async def send_hourly_reminder(bot):
    azkar_pool = load_all_azkar()
    if not azkar_pool:
        return
    
    # اختيار ذكر أو دعاء عشوائي من المجموعة الشاملة
    random_zekr = random.choice(azkar_pool)
    message_text = f"✨ **تذكير الساعة** ✨\n\n{random_zekr}"

    users = get_all_users()
    for user_id in users:
        try:
            await bot.send_message(chat_id=user_id, text=message_text, parse_mode="Markdown")
            await asyncio.sleep(0.05)  # تفادي حظر المعدل (Rate Limit)
        except Exception:
            # حذف المستخدم من قاعدة البيانات في حال قام بحظر البوت
            remove_user(user_id)

def start_scheduler(bot):
    scheduler = AsyncIOScheduler()
    # ضبط التوقيت كل 1 ساعة بدلاً من ساعتين
    scheduler.add_job(send_hourly_reminder, 'interval', hours=1, args=[bot])
    scheduler.start()
