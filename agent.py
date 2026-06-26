import os
import json
import time
import logging
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

# ============================================
# إعدادات الوكيل
# ============================================

BASE_DIR = Path(__file__).parent.absolute()
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOGS_DIR / "deepagent.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("DeepAgent")

# ============================================
# الأدوات (Tools)
# ============================================

class DeepAgentTools:
    def __init__(self):
        self.allowed_commands = [
            # النظام الأساسي
            "ls", "pwd", "whoami", "df -h", "free -m", "uptime",
            "docker ps", "docker logs --tail 50", "ollama list",
            "systemctl status docker", "cat /etc/os-release",
            # الملفات والمشاريع
            "ls -la /root/wld_bot",
            "cat /root/wld_bot/.env",
            "head -n 20 /root/wld_bot/.env",
            "tail -n 20 /root/wld_bot/logs/bot.log",
            "ps aux | grep bot.py",
            "ls -la /root/SmartBinanceBot",
            "cat /root/SmartBinanceBot/config.json",
            "tail -n 50 /root/SmartBinanceBot/logs/bot.log",
            "ps aux | grep SmartBinanceBot",
            # Git
            "git clone", "git pull", "git status", "git add .",
            "git commit -m", "git push origin main",
            # أوامر إضافية
            "screen -ls", "docker ps -a",
            "systemctl list-units --type=service --state=running",
            "find / -name *.env -type f 2>/dev/null",
            "curl -s", "wget", "ping -c 4",
            "node -v", "npm -v", "npx",
            "9router", "opencode",
        ]

    def execute_command(self, command: str) -> str:
        """تنفيذ أمر مع التحقق من الصلاحية"""
        command = command.strip()
        if command not in self.allowed_commands:
            return f"⛔ الأمر '{command}' غير مسموح."

        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=15)
            if result.returncode == 0:
                return f"✅ تم التنفيذ:\n```\n{result.stdout}\n```"
            else:
                return f"⚠️ خطأ (الرمز {result.returncode}):\n```\n{result.stderr}\n```"
        except subprocess.TimeoutExpired:
            return "❌ استغرق الأمر وقتاً طويلاً وتم إلغاؤه."
        except Exception as e:
            return f"❌ خطأ غير متوقع: {str(e)}"

    def read_file(self, filepath: str) -> str:
        """قراءة محتوى ملف"""
        try:
            if not os.path.exists(filepath):
                return f"❌ الملف '{filepath}' غير موجود."
            with open(filepath, 'r', encoding='utf-8') as f:
                return f"📄 محتوى {filepath}:\n```\n{f.read()}\n```"
        except Exception as e:
            return f"❌ خطأ في القراءة: {str(e)}"

    def list_directory(self, path: str = ".") -> str:
        """عرض محتويات مجلد"""
        try:
            items = os.listdir(path)
            files = [f for f in items if os.path.isfile(os.path.join(path, f))]
            dirs = [d for d in items if os.path.isdir(os.path.join(path, d))]
            result = f"📁 مجلد: {path}\n"
            result += f"📂 مجلدات ({len(dirs)}): {', '.join(dirs[:10])}\n"
            result += f"📄 ملفات ({len(files)}): {', '.join(files[:10])}\n"
            if len(items) > 20:
                result += f"... و {len(items)-20} عناصر أخرى"
            return result
        except Exception as e:
            return f"❌ خطأ في عرض المجلد: {str(e)}"

    def get_system_info(self) -> str:
        """معلومات النظام"""
        try:
            info = []
            info.append(f"🖥️  النظام: {subprocess.run('cat /etc/os-release | grep PRETTY_NAME', shell=True, capture_output=True, text=True).stdout.strip()}")
            info.append(f"📅 الوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            info.append(f"💻 المستخدم: {subprocess.run('whoami', shell=True, capture_output=True, text=True).stdout.strip()}")
            info.append(f"💾 الذاكرة: {subprocess.run('free -h | grep Mem | awk \'{print $3 \"/\" $2}\'', shell=True, capture_output=True, text=True).stdout.strip()}")
            info.append(f"💿 المساحة: {subprocess.run('df -h / | awk \'NR==2 {print $3 \"/\" $2 \" (\" $5 \")\"}\'', shell=True, capture_output=True, text=True).stdout.strip()}")
            return "\n".join(info)
        except Exception as e:
            return f"❌ خطأ: {str(e)}"

# ============================================
# الوكيل الرئيسي
# ============================================

class DeepAgent:
    def __init__(self):
        self.tools = DeepAgentTools()
        self.memory = []
        self.max_memory = 50

    def process(self, user_input: str) -> str:
        """معالجة طلب المستخدم"""
        # حفظ في الذاكرة
        self.memory.append({"role": "user", "content": user_input, "time": datetime.now().isoformat()})
        if len(self.memory) > self.max_memory:
            self.memory.pop(0)

        user_input_lower = user_input.lower().strip()

        # أوامر النظام
        if user_input_lower.startswith("نفذ") or user_input_lower.startswith("execute"):
            command = user_input_lower.replace("نفذ", "").replace("execute", "").strip()
            return self.tools.execute_command(command)

        elif user_input_lower.startswith("اقرأ") or user_input_lower.startswith("read"):
            filepath = user_input_lower.replace("اقرأ", "").replace("read", "").strip()
            return self.tools.read_file(filepath)

        elif user_input_lower.startswith("عرض") or user_input_lower.startswith("list"):
            path = user_input_lower.replace("عرض", "").replace("list", "").strip() or "."
            return self.tools.list_directory(path)

        elif user_input_lower in ["معلومات", "info", "حالة", "status"]:
            return self.tools.get_system_info()

        elif user_input_lower in ["مساعدة", "help"]:
            return """
🛠️ **الأوامر المتاحة:**
- **نفذ <أمر>** : تنفيذ أمر على الخادم
- **اقرأ <مسار>** : عرض محتوى ملف
- **عرض <مسار>** : عرض محتويات مجلد
- **معلومات** : عرض معلومات النظام
- **مساعدة** : عرض هذه القائمة
- **ذاكرة** : عرض تاريخ المحادثات
"""
        else:
            return f"🤖 أنا DeepAgent. لم أفهم طلبك. اكتب 'مساعدة' لرؤية الأوامر المتاحة."

# ============================================
# تشغيل الوكيل
# ============================================

if __name__ == "__main__":
    agent = DeepAgent()
    print("🤖 DeepAgent يعمل!")
    print("اكتب 'مساعدة' لرؤية الأوامر، أو 'خروج' للإنهاء.\n")

    while True:
        try:
            user_input = input("\n🔹 أنت: ").strip()
            if user_input.lower() in ["خروج", "exit", "quit"]:
                print("👋 وداعاً!")
                break
            if not user_input:
                continue
            response = agent.process(user_input)
            print(f"\n🤖 DeepAgent: {response}")
        except KeyboardInterrupt:
            print("\n👋 تم الإنهاء.")
            break
        except Exception as e:
            logger.error(f"خطأ غير متوقع: {e}")
            print(f"❌ حدث خطأ: {e}")
