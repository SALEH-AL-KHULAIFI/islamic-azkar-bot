import os
import json
import telebot
from telebot import types
from dotenv import load_dotenv
from database import init_db, add_user
from scheduler import start_scheduler

# تحميل المتغيرات البيئية من ملف .env
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("لم يتم العثور على BOT_TOKEN. يرجى التأكد من ضبطه في ملف .env أو في إعدادات Railway.")

bot = telebot.TeleBot(BOT_TOKEN)

AZKAR_FILE = os.path.join(os.path.dirname(__file__), 'data', 'azkar.json')

def load_azkar_data():
    """تحميل بيانات الأذكار من ملف JSON."""
    try:
        with open(AZKAR_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"خطأ أثناء تحميل الأذكار: {e}")
        return {}

def build_main_menu():
    """إنشاء أزرار القائمة الرئيسية."""
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_morning = types.InlineKeyboardButton("🌅 أذكار الصباح", callback_data="cat_morning")
    btn_evening = types.InlineKeyboardButton("🌆 أذكار المساء", callback_data="cat_evening")
    btn_after_prayer = types.InlineKeyboardButton("🕌 أذكار بعد الصلاة", callback_data="cat_after_prayer")
    btn_duas = types.InlineKeyboardButton("🤲 أدعية متنوعة", callback_data="cat_duas")
    
    markup.add(btn_morning, btn_evening, btn_after_prayer, btn_duas)
    return markup

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name or "المستخدم"
    
    # إضافة المستخدم لجدول التذكيرات الدوري[span_0](start_span)[span_0](end_span)
    add_user(user_id)
    
    welcome_text = (
        f"أهلاً بك يا {first_name} في بوت الأذكار الإسلامية 🌿\n\n"
        "سيقوم البوت بحفظ حسابك تلقائياً وإرسال أدعية وتذكيرات متنوعة لك **كل ساعتين** بإذن الله.\n\n"
        "يمكنك أيضاً تصفح الأذكار والأدعية المقسمة من القائمة أدناه:"
    )
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=build_main_menu(), parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data.startswith('cat_'))
def handle_category_selection(call):
    category_key = call.data.replace('cat_', '')
    azkar_data = load_azkar_data()
    categories = azkar_data.get('categories', {})
    
    category_names = {
        'morning': '🌅 أذكار الصباح',
        'evening': '🌆 أذكار المساء',
        'after_prayer': '🕌 أذكار بعد الصلاة',
        'duas': '🤲 أدعية متنوعة'
    }
    
    items = categories.get(category_key, [])
    
    if not items:
        bot.answer_callback_query(call.id, "لا توجد أذكار متوفرة في هذا القسم حالياً.")
        return
    
    bot.answer_callback_query(call.id)
    
    title = category_names.get(category_key, "الأذكار")
    text_response = f"✨ **{title}** ✨\n\n"
    
    for item in items:
        item_title = item.get('title', '')
        item_text = item.get('text', '')
        count = item.get('count')
        
        text_response += f"🔹 **{item_title}**\n{item_text}\n"
        if count:
            text_response += f"⏱ التكرار: {count}\n"
        text_response += "\n-------------------\n\n"
    
    # زر العودة للقائمة الرئيسية
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu"))
    
    bot.edit_message_text(
        text=text_response,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup,
        parse_mode='Markdown'
    )

@bot.callback_query_handler(func=lambda call: call.data == "main_menu")
def handle_back_to_main(call):
    bot.answer_callback_query(call.id)
    bot.edit_message_text(
        text="اختر قسم الأذكار الذي تريد تصفحه:",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=build_main_menu()
    )

if __name__ == '__main__':
    print("جاري تشغيل البوت وإعداد قاعدة البيانات...")
    init_db()
    start_scheduler(bot)
    print("البوت يعمل الآن واستقبال الرسائل مفعل...")
    bot.infinity_polling()
