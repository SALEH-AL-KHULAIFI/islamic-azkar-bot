⚙️ التشغيل المحلي (Local Setup)
 * استنسخ المستودع (Clone the repository):
   git clone [https://github.com/your-username/islamic-azkar-bot.git](https://github.com/your-username/islamic-azkar-bot.git)
cd islamic-azkar-bot

 * قم بتثبيت المكتبات المطلوبة:
   pip install -r requirements.txt

 * إعداد ملف البيئة .env:
   قم بإنشاء ملف باسم .env في المجلد الرئيسي واكتب فيه التوكن الخاص ببوتك:
   BOT_TOKEN=your_telegram_bot_token_here

 * تشغيل البوت:
   python bot.py

☁️ النشر على Railway (Deployment)
 * ارفع المشروع إلى GitHub.
 * سجل الدخول إلى Railway:
   * اختر New Project -> Deploy from GitHub repo.
   * حدد مستودع البوت الخاص بك.
 * أضف المتغيرات البيئية (Variables):
   * انتقل إلى قسم Variables في Railway.
   * أضف متغير باسم BOT_TOKEN وضع فيه قيمة توكن البوت.
 * ربط التخزين الثابت (Volume):
   * من إعدادات الخدمة (Settings)، قم بإنشاء Volume.
   * اجعل مسار التثبيت (Mount Path) يساوي: /app/data للحفاظ على بيانات المستخدمين وقاعدة البيانات عند إعادة التشغيل.
     """
with open("README.md", "w", encoding="utf-8") as f:
f.write(readme_content)
print("README.md created successfully.")

```text?code_stdout&code_event_index=1
README.md created successfully.


🌿 بوت الأذكار الإسلامية (Islamic Azkar Bot)
بوت تلغرام إسلامي تفاعلي ومبرمج بلغة Python، يقوم بإرسال تذكيرات وأدعية قصيرة ومختلفة تلقائياً للمستخدمين كل ساعتين، بالإضافة إلى توفير أذكار مقسمة ومنظمة عبر أزرار تفاعلية.
🚀 المميزات
 * تذكير دوري تلقائي: إرسال ذكر أو دعاء عشوائي لكل المستخدمين كل ساعتين.
 * قائمة أذكار مقسمة: تشمل أذكار الصباح، أذكار المساء، أذكار بعد الصلاة، وأدعية متنوعة.
 * حفظ المستخدمين: حفظ تلقائي لجميع المشتركين في قاعدة بيانات SQLite بدون تكرار.
 * إدارة الحظر: حذف المستخدمين تلقائياً في حال قاموا بحظر البوت للحفاظ على سرعة وكفاءة الإرسال.
 * جاهز للنشر السحابي: متوافق بالكامل مع منصة Railway.
📁 هيكلة المشروع (Project Structure)
islamic-azkar-bot/
├── bot.py             # الملف الرئيسي لتشغيل البوت والأوامر
├── database.py        # إدارة قاعدة البيانات (SQLite)
├── scheduler.py       # جدول التذكيرات التلقائية (كل ساعتين)
├── data/
│   └── azkar.json     # ملف البيانات الخاص بالأذكار والأدعية
├── requirements.txt   # المكتبات البرمجية المطلوبة
├── Procfile           # أمر تشغيل البوت على منصات الاستضافة
├── .gitignore         # لتجاهل الملفات الحساسة والتنفيذية
└── README.md          # ملف التوثيق الشارح للمشروع

⚙️ التشغيل المحلي (Local Setup)
 * استنسخ المستودع (Clone the repository):
   git clone https://github.com/your-username/islamic-azkar-bot.git
cd islamic-azkar-bot

 * قم بتثبيت المكتبات المطلوبة:
   pip install -r requirements.txt

 * إعداد ملف البيئة .env:
   قم بإنشاء ملف باسم .env في المجلد الرئيسي واكتب فيه التوكن الخاص ببوتك:
   BOT_TOKEN=your_telegram_bot_token_here

 * تشغيل البوت:
   python bot.py

☁️ النشر على Railway (Deployment)
 * ارفع المشروع إلى GitHub.
 * سجل الدخول إلى Railway:
   * اختر New Project -> Deploy from GitHub repo.
   * حدد مستودع البوت الخاص بك.
 * أضف المتغيرات البيئية (Variables):
   * انتقل إلى قسم Variables في Railway.
   * أضف متغير باسم BOT_TOKEN وضع فيه قيمة توكن البوت.
 * ربط التخزين الثابت (Volume):
   * من إعدادات الخدمة (Settings)، قم بإنشاء Volume.
   * اجعل مسار التثبيت (Mount Path) يساوي: /app/data للحفاظ على بيانات المستخدمين وقاعدة البيانات عند إعادة التشغيل.
