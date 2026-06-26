import os
import subprocess
from datetime import datetime

class TerminalTools:
    def __init__(self):
        # ============================================
        # قائمة الأوامر المسموحة (مقسمة حسب المستوى)
        # ============================================
        
        # المستوى 1: أوامر آمنة للجميع (قراءة فقط)
        self.safe_commands = [
            "ls", "pwd", "whoami", "df -h", "free -m", "uptime",
            "cat /etc/os-release", "ollama list",
            "docker ps", "docker ps -a", "systemctl status docker",
            "git status",
        ]
        
        # المستوى 2: أوامر إدارة الملفات (آمنة مع تحذيرات)
        self.file_commands = [
            "ls -la", "cat", "head -n 20", "tail -n 20",
            "mkdir -p", "touch", "cp -r", "mv", "rm -rf",
            "chmod +x", "chown -R", "find / -name", "grep -r",
        ]
        
        # المستوى 3: أوامر Git
        self.git_commands = [
            "git clone", "git pull", "git status", "git add .",
            "git commit -m", "git push origin main",
        ]
        
        # المستوى 4: أوامر Docker
        self.docker_commands = [
            "docker ps", "docker logs --tail 50",
            "docker start", "docker stop", "docker restart",
            "docker-compose up -d", "docker-compose down",
            "docker-compose ps", "docker-compose logs --tail 50",
        ]
        
        # المستوى 5: أوامر الشبكة
        self.network_commands = [
            "curl -s", "wget", "ping -c 4",
            "systemctl status nginx", "systemctl restart nginx",
        ]
        
        # المستوى 6: أوامر متقدمة (تتطلب تأكيداً)
        self.advanced_commands = [
            "systemctl stop", "systemctl start",
            "docker rm", "docker rmi", "docker-compose restart",
        ]
        
        # دمج جميع الأوامر في قائمة واحدة
        self.allowed_commands = (
            self.safe_commands +
            self.file_commands +
            self.git_commands +
            self.docker_commands +
            self.network_commands +
            self.advanced_commands
        )
        
        # أوامر خطيرة تحتاج تأكيد
        self.dangerous_commands = [
            "rm -rf", "systemctl stop", "docker rm", "docker rmi",
            "docker-compose down", "git push --force",
        ]

    # ============================================
    # تنفيذ الأمر مع تأكيد للأوامر الخطيرة
    # ============================================
    def execute_command(self, command: str, confirm: bool = False) -> str:
        """تنفيذ الأمر مع تحقق من الصلاحية وتأكيد للأوامر الخطيرة"""
        command = command.strip()
        
        # التحقق من وجود الأمر في القائمة المسموحة
        if command not in self.allowed_commands:
            return self._get_help_message(command)
        
        # التحقق من الأوامر الخطيرة
        if any(danger in command for danger in self.dangerous_commands) and not confirm:
            return f"""
⚠️ **تنبيه: الأمر '{command}' قد يكون خطيراً.**

🔒 **تأكد من أنك تريد تنفيذ هذا الأمر.**

📌 **للتأكيد، أضف `confirm=True`**:
مثال: `نفذ الأمر '{command}' مع تأكيد`
"""
        
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=15)
            if result.returncode == 0:
                return f"✅ **تم التنفيذ بنجاح!**\n```\n{result.stdout}\n```"
            else:
                return f"⚠️ **حدث خطأ أثناء التنفيذ.**\n```\n{result.stderr}\n```"
        except subprocess.TimeoutExpired:
            return "⏰ **استغرق الأمر وقتاً طويلاً.** حاول مرة أخرى."
        except Exception as e:
            return f"❌ **حدث خطأ غير متوقع:** {str(e)}"

    # ============================================
    # رسالة مساعدة ودية
    # ============================================
    def _get_help_message(self, command: str) -> str:
        """رسالة مساعدة توضح الأوامر المتاحة"""
        return f"""
❌ **عذراً، الأمر '{command}' غير مسموح.**

📌 **الأوامر المتاحة:**

🔹 **أوامر آمنة (للقراءة):**
`ls`, `pwd`, `whoami`, `df -h`, `free -m`, `uptime`, `ollama list`, `docker ps`

🔹 **إدارة الملفات:**
`ls -la`, `cat`, `head -n 20`, `tail -n 20`, `mkdir -p`, `touch`, `cp -r`, `mv`

🔹 **Git:**
`git clone`, `git pull`, `git status`, `git add .`, `git commit -m`, `git push origin main`

🔹 **Docker:**
`docker ps`, `docker logs --tail 50`, `docker start`, `docker stop`, `docker restart`, `docker-compose up -d`, `docker-compose down`

🔹 **الشبكة:**
`curl -s`, `wget`, `ping -c 4`, `systemctl status nginx`

🔹 **الأوامر المتقدمة (تتطلب تأكيداً):**
`systemctl stop`, `systemctl start`, `docker rm`, `docker rmi`, `docker-compose restart`

💡 **نصيحة:** استخدم `مساعدة` لرؤية قائمة كاملة.
"""

    # ============================================
    # عرض معلومات النظام
    # ============================================
    def get_system_info(self) -> str:
        """عرض معلومات النظام بشكل منظم"""
        try:
            info = []
            info.append(f"🖥️  **النظام:** {subprocess.run('cat /etc/os-release | grep PRETTY_NAME', shell=True, capture_output=True, text=True).stdout.strip()}")
            info.append(f"📅 **الوقت:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            info.append(f"💻 **المستخدم:** {subprocess.run('whoami', shell=True, capture_output=True, text=True).stdout.strip()}")
            info.append(f"💾 **الذاكرة:** {subprocess.run('free -h | grep Mem | awk \'{print $3 \"/\" $2}\'', shell=True, capture_output=True, text=True).stdout.strip()}")
            info.append(f"💿 **المساحة:** {subprocess.run('df -h / | awk \'NR==2 {print $3 \"/\" $2 \" (\" $5 \")\"}\'', shell=True, capture_output=True, text=True).stdout.strip()}")
            return "\n".join(info)
        except Exception as e:
            return f"❌ **خطأ في جلب المعلومات:** {str(e)}"

    # ============================================
    # عرض العمليات النشطة
    # ============================================
    def list_processes(self) -> str:
        """عرض العمليات النشطة"""
        try:
            result = subprocess.run("ps aux --sort=-%cpu | head -20", shell=True, capture_output=True, text=True)
            return f"📊 **العمليات النشطة (أعلى 20):**\n```\n{result.stdout}\n```"
        except Exception as e:
            return f"❌ **خطأ:** {str(e)}"
