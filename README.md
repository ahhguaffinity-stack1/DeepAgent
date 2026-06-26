🤖 DeepAgent

وكيل ذكي مفتوح المصدر لإدارة الخوادم، التداول الآلي، وأتمتة المهام البرمجية عبر الدردشة.

https://img.shields.io/badge/License-MIT-yellow.svg
https://img.shields.io/badge/python-3.10+-blue.svg
https://img.shields.io/github/stars/ahhguaffinity-stack1/DeepAgent.svg

---

📖 عن المشروع

DeepAgent هو وكيل ذكي يعمل بالذكاء الاصطناعي، صُمم لتسهيل إدارة الخوادم (VPS)، تنفيذ الأوامر، التداول الآلي، وأتمتة المهام البرمجية، كل ذلك عبر واجهة محادثة بسيطة.

✨ المميزات الرئيسية

الميزة الوصف
🖥️ إدارة الخوادم تنفيذ أوامر على VPS عبر الدردشة (مثل docker ps, systemctl, df -h).
🤖 التداول الآلي دعم منصات Binance، Bybit، Coinbase مع استراتيجيات RSI و Stop Loss.
🧠 نماذج متعددة يدعم Ollama (Gemma 3)، OpenRouter، و 9Router.
📊 لوحة تحكم واجهة ويب تفاعلية لعرض الأداء والتحكم (Open WebUI).
🔌 قابلية التوسع إضافة أدوات (Tools) مخصصة بسهولة.
🌐 دعم GitHub مزامنة التغييرات وإدارة الإصدارات عبر Git.

---

🛠️ التثبيت السريع

المتطلبات الأساسية

· Python 3.10+
· Docker (اختياري)
· Ollama (لتشغيل النماذج المحلية)
· Git

خطوات التثبيت

```bash
# 1. استنساخ المستودع
git clone https://github.com/ahhguaffinity-stack1/DeepAgent.git
cd DeepAgent

# 2. تثبيت الاعتماديات
pip install -r requirements.txt

# 3. تشغيل الوكيل
python agent.py
```

---

🚀 الاستخدام

1️⃣ عبر واجهة الدردشة (Open WebUI)

· افتح المتصفح على: http://localhost:8080
· سجل الدخول وابدأ المحادثة.

2️⃣ عبر الأوامر المباشرة

```bash
python agent.py --command "مرحباً، من أنت؟"
```

3️⃣ عبر Telegram (اختياري)

· أضف بوت Telegram وأدخل TELEGRAM_BOT_TOKEN في ملف .env.

---

📂 هيكل المشروع

```
DeepAgent/
├── agent.py              # الكود الرئيسي للوكيل
├── tools/                # أدوات مخصصة (بحث، ملفات، أوامر)
│   ├── terminal.py
│   ├── trading.py
│   └── web_search.py
├── frontend/             # واجهة المستخدم (HTML/CSS/JS)
│   └── index.html
├── config/               # ملفات الإعدادات
│   └── config.yaml
├── requirements.txt      # اعتماديات Python
├── Dockerfile            # بناء حاوية Docker
├── docker-compose.yml    # تشغيل الخدمات المتعددة
└── README.md             # هذا الملف
```

---

🔧 الإعدادات المتقدمة

ملف .env (مثال)

```env
# Ollama
OLLAMA_HOST=http://localhost:11434
MODEL_NAME=gemma3:4b

# OpenRouter
OPENROUTER_API_KEY=sk-or-...

# Binance
BINANCE_API_KEY=your_key
BINANCE_SECRET_KEY=your_secret

# Telegram
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHAT_ID=your_chat_id
```

تشغيل الوكيل كخدمة (systemd)

```bash
sudo cp deepagent.service /etc/systemd/system/
sudo systemctl enable deepagent
sudo systemctl start deepagent
```

---

🤝 المساهمة

نرحب بمساهماتكم! 🚀

1. Fork المشروع.
2. أنشئ فرعاً جديداً (git checkout -b feature/amazing-feature).
3. أضف تغييراتك (git commit -m 'Add amazing feature').
4. ارفع التغييرات (git push origin feature/amazing-feature).
5. افتح Pull Request.

---

📝 الترخيص

هذا المشروع مرخص تحت MIT License.

---

📬 التواصل

· المطور: ahhguaffinity-stack1
· البريد الإلكتروني: ssemoa32@gmail.com

---

🌟 شكر خاص

· Ollama لتشغيل النماذج المحلية.
· Open WebUI للواجهة الرسومية.
· 9Router لتوجيه النماذج.

---

⭐ لا تنسَ أن تضع نجمة (Star) على المشروع إذا أعجبك!

---

بعد كتابة هذا الـ README، يمكنك رفعه إلى GitHub مع باقي الملفات. إذا احتجت تعديلاً أو إضافة قسم معين، أخبرني. 😊
