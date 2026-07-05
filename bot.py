import os
import time
import json
import urllib.request
import urllib.error
from datetime import datetime

# ============================================
# 🔑 توكن البوت (ضع التوكن هنا)
# ============================================
BOT_TOKEN = "8770824530:AAFqrPDiqQfKjYMgF9KWZ9H8sc9G8Rc8BAQ"

# ============================================
# 📁 الإعدادات
# ============================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# ============================================
# 📂 دوال الملفات
# ============================================
def read_file(path):
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        return [line.strip() for line in f if line.strip()]

def write_file(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(data))

def append_file(path, data):
    with open(path, 'a', encoding='utf-8') as f:
        f.write(data + '\n')

def clear_file(path):
    if os.path.exists(path):
        os.remove(path)

# ============================================
# 🚀 مولد الإيميلات الذكي (جميع الصيغ)
# ============================================
def generate_all_emails(list1, list2, domains, options):
    """توليد جميع الإيميلات الممكنة بناءً على الخيارات"""
    results = set()
    
    # تحديد الفواصل حسب الخيارات
    separators = []
    if options.get('dot'): separators.append('.')
    if options.get('hyphen'): separators.append('-')
    if options.get('underscore'): separators.append('_')
    if not separators:  # إذا لم يختار أي فاصل، استخدم "" (بدون فاصل)
        separators = ['']
    
    years = list(range(1970, 2031)) if options.get('years') else []
    numbers = list(range(0, 1000)) if options.get('numbers') else []
    extra_words = ['PLAY', 'PLAYSTATION', 'PLAYSTATION3', 'PS3', 'PSN']
    
    for first in list1:
        for second in list2:
            # 1. الأساسيات
            results.add(first + second)
            if options.get('reverse'):
                results.add(second + first)
            
            # 2. مع فواصل
            for sep in separators:
                if sep:
                    results.add(first + sep + second)
                    if options.get('reverse'):
                        results.add(second + sep + first)
            
            # 3. مع أرقام
            if options.get('numbers'):
                for num in numbers[:200]:
                    for sep in separators:
                        if sep:
                            results.add(first + sep + second + sep + str(num))
                            results.add(first + sep + str(num))
                            if options.get('reverse'):
                                results.add(second + sep + first + sep + str(num))
                                results.add(second + sep + str(num))
                        else:
                            results.add(first + second + str(num))
                            results.add(first + str(num))
                            results.add(second + str(num))
            
            # 4. مع سنوات
            if options.get('years'):
                for year in years[:20]:
                    for sep in separators:
                        if sep:
                            results.add(first + sep + second + sep + str(year))
                            results.add(first + sep + str(year))
                            if options.get('reverse'):
                                results.add(second + sep + first + sep + str(year))
                                results.add(second + sep + str(year))
                        else:
                            results.add(first + second + str(year))
                            results.add(first + str(year))
                            results.add(second + str(year))
            
            # 5. تكرار الكلمات
            if options.get('repeat'):
                results.add(first + first)
                results.add(second + second)
                results.add(first + second + first)
                results.add(second + first + second)
            
            # 6. كلمات إضافية (PLAY, PS3, PSN...)
            for extra in extra_words:
                for sep in separators:
                    if sep:
                        results.add(first + sep + extra)
                        results.add(second + sep + extra)
                        results.add(first + sep + second + sep + extra)
                        if options.get('reverse'):
                            results.add(second + sep + first + sep + extra)
                    else:
                        results.add(first + extra)
                        results.add(second + extra)
                        results.add(first + second + extra)
                        if options.get('reverse'):
                            results.add(second + first + extra)
            
            # 7. أنماط خاصة (q-q-0, q.q.0, q_q_0)
            for sep1 in ['-', '.', '_']:
                for sep2 in ['-', '.', '_']:
                    results.add(first + sep1 + second + sep2 + '0')
                    results.add(first + sep1 + second + sep2 + '100')
                    results.add(first + sep1 + second + sep2 + '123')
                    results.add(first + sep1 + second + sep2 + '2026')
                    if options.get('numbers'):
                        for num in numbers[:100]:
                            results.add(first + sep1 + second + sep2 + str(num))
            
            # 8. أنماط (q-q-PLAY, q.q.PLAY, q_q_PLAY)
            for extra in extra_words:
                for sep1 in ['-', '.', '_']:
                    for sep2 in ['-', '.', '_']:
                        results.add(first + sep1 + second + sep2 + extra)
            
            # 9. أنماط بدون فاصل (qq0, qq100, qq123)
            if options.get('numbers'):
                for num in numbers[:100]:
                    results.add(first + second + str(num))
            
            # 10. أنماط (q-q@, q.q@, q_q@)
            for sep in ['-', '.', '_']:
                results.add(first + sep + second)
    
    # إضافة النطاقات
    final = []
    for email in results:
        for domain in domains:
            final.append(email + domain)
    
    return list(set(final))

# ============================================
# 🔍 فاحص EA
# ============================================
def check_ea(email, proxy=None):
    try:
        url = f'https://signin.ea.com/p/{email}'
        req = urllib.request.Request(url, method='HEAD')
        req.add_header('User-Agent', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0)')
        if proxy:
            proxy_handler = urllib.request.ProxyHandler({'http': proxy, 'https': proxy})
            opener = urllib.request.build_opener(proxy_handler)
            urllib.request.install_opener(opener)
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status == 200
    except:
        return False

def check_ms(email, proxy=None):
    try:
        url = 'https://login.live.com/GetCredentialType.srf'
        data = json.dumps({"Username": email}).encode('utf-8')
        req = urllib.request.Request(url, data=data, method='POST')
        req.add_header('Content-Type', 'application/json')
        if proxy:
            proxy_handler = urllib.request.ProxyHandler({'http': proxy, 'https': proxy})
            opener = urllib.request.build_opener(proxy_handler)
            urllib.request.install_opener(opener)
        with urllib.request.urlopen(req, timeout=6) as resp:
            result = json.loads(resp.read().decode())
            if result.get('IfExistsResult') == 0:
                return 'available'
            elif result.get('IfExistsResult') == 1:
                return 'not_available'
            else:
                return 'error'
    except:
        return 'error'

# ============================================
# 🌐 مدير البروكسيات
# ============================================
class ProxyManager:
    def __init__(self, proxies=None):
        self.proxies = proxies if proxies else []
        self.index = 0
        self.failed = []
    
    def get_next(self):
        if not self.proxies:
            return None
        proxy = self.proxies[self.index % len(self.proxies)]
        self.index += 1
        return proxy
    
    def mark_failed(self, proxy):
        if proxy in self.proxies:
            self.proxies.remove(proxy)
            self.failed.append(proxy)
    
    def get_stats(self):
        return {
            'total': len(self.proxies) + len(self.failed),
            'active': len(self.proxies),
            'failed': len(self.failed)
        }

# ============================================
# 📊 دوال التلغرام
# ============================================
def send_message(chat_id, text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = f"chat_id={chat_id}&text={text}&parse_mode=Markdown"
        req = urllib.request.Request(url, data=data.encode('utf-8'), method='POST')
        urllib.request.urlopen(req, timeout=10)
        return True
    except Exception as e:
        print(f"❌ خطأ في الإرسال: {e}")
        return False

def send_file(chat_id, file_path, caption=""):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
        boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
        with open(file_path, 'rb') as f:
            file_data = f.read()
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="chat_id"\r\n\r\n{chat_id}\r\n'
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="caption"\r\n\r\n{caption}\r\n'
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="document"; filename="{os.path.basename(file_path)}"\r\n'
            f"Content-Type: text/plain\r\n\r\n"
        ).encode('utf-8') + file_data + f"\r\n--{boundary}--\r\n".encode('utf-8')
        req = urllib.request.Request(url, data=body, method='POST')
        req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')
        urllib.request.urlopen(req, timeout=30)
        return True
    except Exception as e:
        print(f"❌ خطأ في إرسال الملف: {e}")
        return False

def get_updates(offset=None):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
        if offset:
            url += f"?offset={offset}"
        req = urllib.request.Request(url, method='GET')
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            return data.get('result', [])
    except Exception as e:
        print(f"❌ خطأ في جلب التحديثات: {e}")
        return []

# ============================================
# 📋 حالة المستخدمين
# ============================================
user_sessions = {}

# ============================================
# ⚙️ معالج الأوامر
# ============================================
def process_command(chat_id, text):
    global user_sessions
    
    # التحقق من وجود جلسة نشطة
    if chat_id in user_sessions:
        session = user_sessions[chat_id]
        step = session.get('step')
        
        # ===== مرحلة توليد الإيميلات =====
        if step == 'awaiting_first':
            session['first'] = text.strip()
            session['step'] = 'awaiting_second'
            send_message(chat_id, "📝 **أرسل الكلمة الثانية** (اختياري، اكتب /skip للتخطي)")
            return
        
        elif step == 'awaiting_second':
            if text == '/skip':
                session['second'] = ''
            else:
                session['second'] = text.strip()
            session['step'] = 'awaiting_domains'
            send_message(chat_id, """
🌐 **اختر النطاقات:**
1. @hotmail.com
2. @outlook.com
3. @live.com
4. @msn.com
5. الكل (1,2,3,4)

أرسل الأرقام مفصولة بفواصل (مثال: 1,2,5)
            """)
            return
        
        elif step == 'awaiting_domains':
            domains = []
            if '1' in text or '5' in text:
                domains.append('@hotmail.com')
            if '2' in text or '5' in text:
                domains.append('@outlook.com')
            if '3' in text or '5' in text:
                domains.append('@live.com')
            if '4' in text or '5' in text:
                domains.append('@msn.com')
            if not domains:
                send_message(chat_id, "❌ اختر نطاقاً واحداً على الأقل")
                return
            session['domains'] = domains
            session['step'] = 'awaiting_options'
            send_message(chat_id, """
⚙️ **اختر خيارات التوليد:**
أرسل الأرقام المطلوبة (مفصولة بفواصل):
1. أرقام
2. سنوات
3. نقطة (.)
4. شرطة (-)
5. شرطة سفلية (_)
6. عكس الترتيب
7. تكرار

مثال: 1,2,3,4,5,6,7 (الكل)
أو /skip لاستخدام الإعدادات الافتراضية
            """)
            return
        
        elif step == 'awaiting_options':
            options = {
                'numbers': False,
                'years': False,
                'dot': False,
                'hyphen': False,
                'underscore': False,
                'reverse': False,
                'repeat': False
            }
            if text == '/skip':
                # تفعيل كل شيء
                options = {
                    'numbers': True,
                    'years': True,
                    'dot': True,
                    'hyphen': True,
                    'underscore': True,
                    'reverse': True,
                    'repeat': True
                }
            else:
                if '1' in text: options['numbers'] = True
                if '2' in text: options['years'] = True
                if '3' in text: options['dot'] = True
                if '4' in text: options['hyphen'] = True
                if '5' in text: options['underscore'] = True
                if '6' in text: options['reverse'] = True
                if '7' in text: options['repeat'] = True
            
            # توليد الإيميلات
            list1 = [session.get('first')]
            list2 = [session.get('second')] if session.get('second') else ['']
            domains = session['domains']
            
            send_message(chat_id, "⏳ جاري توليد الإيميلات...")
            emails = generate_all_emails(list1, list2, domains, options)
            write_file(os.path.join(DATA_DIR, 'emails.txt'), emails)
            
            send_message(chat_id, f"✅ **تم توليد {len(emails)} إيميل**\n📁 حفظ في `emails.txt`")
            
            # عرض عينة
            sample = "\n".join(emails[:15])
            send_message(chat_id, f"📋 **عينة من الإيميلات:**\n```\n{sample}\n```")
            if len(emails) > 15:
                send_message(chat_id, f"... و {len(emails)-15} إيميل آخر")
            
            # حذف الجلسة
            del user_sessions[chat_id]
            send_message(chat_id, "🔄 **الآن يمكنك بدء فحص EA**\nأرسل /check_ea")
            return
        
        # ===== مرحلة فحص EA =====
        elif step == 'awaiting_proxies':
            proxies = []
            if text.startswith('/'):
                # استيراد من ملف
                file_path = os.path.join(DATA_DIR, 'proxies.txt')
                proxies = read_file(file_path)
                if not proxies:
                    send_message(chat_id, "❌ ملف البروكسيات فارغ! أرسل بروكسيات يدوياً (واحد لكل سطر، انتهى بـ /done)")
                    return
            else:
                # كتابة يدوية
                proxies = [p.strip() for p in text.split('\n') if p.strip()]
                write_file(os.path.join(DATA_DIR, 'proxies.txt'), proxies)
            
            send_message(chat_id, f"🌐 تم تحميل {len(proxies)} بروكسي")
            
            # بدء الفحص
            session['proxies'] = proxies
            session['step'] = 'checking_ea'
            session['linked'] = []
            session['not_linked'] = []
            session['total'] = len(read_file(os.path.join(DATA_DIR, 'emails.txt')))
            session['checked'] = 0
            
            send_message(chat_id, f"▶️ **بدء فحص EA لـ {session['total']} إيميل...**")
            
            # تشغيل الفحص
            start_check_ea(chat_id)
            return
    
    # ===== أوامر رئيسية =====
    if text == "/start":
        send_message(chat_id, """
🤖 **بوت EA + Outlook Checker v2.0**

📌 **الأوامر المتاحة:**
/generate - توليد إيميلات (جميع الصيغ)
/check_ea - فحص EA (يتطلب بروكسيات)
/check_ms - فحص Microsoft (تلقائي بعد EA)
/stats - عرض الإحصائيات
/export - تصدير النتائج (ملفات TXT)
/help - عرض المساعدة

📁 **النتائج تحفظ في مجلد data/**
        """)
    
    elif text == "/generate":
        user_sessions[chat_id] = {'step': 'awaiting_first'}
        send_message(chat_id, "📝 **أرسل الكلمة الأولى** (مثال: king)")
    
    elif text == "/check_ea":
        emails = read_file(os.path.join(DATA_DIR, 'emails.txt'))
        if not emails:
            send_message(chat_id, "❌ لا توجد إيميلات! استخدم /generate أولاً")
            return
        
        proxies = read_file(os.path.join(DATA_DIR, 'proxies.txt'))
        if proxies:
            send_message(chat_id, f"🌐 تم العثور على {len(proxies)} بروكسي في الملف\nبدء الفحص...")
            user_sessions[chat_id] = {
                'step': 'checking_ea',
                'proxies': proxies,
                'linked': [],
                'not_linked': [],
                'total': len(emails),
                'checked': 0
            }
            start_check_ea(chat_id)
        else:
            user_sessions[chat_id] = {'step': 'awaiting_proxies'}
            send_message(chat_id, """
📤 **أرسل البروكسيات** (واحد لكل سطر)
أو ارفع ملف `proxies.txt`
أو اكتب `/file` لاستيراد من الملف
            """)
    
    elif text == "/check_ms":
        emails = read_file(os.path.join(DATA_DIR, 'NotLinked.txt'))
        if not emails:
            send_message(chat_id, "❌ لا توجد إيميلات غير مرتبطة! استخدم /check_ea أولاً")
            return
        
        proxies = read_file(os.path.join(DATA_DIR, 'proxies.txt'))
        if not proxies:
            send_message(chat_id, "⚠️ لا توجد بروكسيات! استخدم /check_ea أولاً")
            return
        
        send_message(chat_id, f"▶️ **بدء فحص Microsoft لـ {len(emails)} إيميل...**")
        start_check_ms(chat_id)
    
    elif text == "/stats":
        files = {
            'emails.txt': '📧 الإيميلات الكلي',
            'Linked.txt': '🔗 مرتبط بـ EA',
            'NotLinked.txt': '❌ غير مرتبط',
            'Available.txt': '📤 متاح',
            'NotAvailable.txt': '📥 غير متاح',
            'Errors.txt': '⚠️ أخطاء'
        }
        msg = "📊 **الإحصائيات:**\n\n"
        for f, label in files.items():
            count = len(read_file(os.path.join(DATA_DIR, f)))
            msg += f"{label}: {count}\n"
        proxies = len(read_file(os.path.join(DATA_DIR, 'proxies.txt')))
        msg += f"🌐 البروكسيات المحملة: {proxies}"
        send_message(chat_id, msg)
    
    elif text == "/export":
        files = ['emails.txt', 'Linked.txt', 'NotLinked.txt', 'Available.txt', 'NotAvailable.txt', 'Errors.txt']
        sent = 0
        for f in files:
            path = os.path.join(DATA_DIR, f)
            if os.path.exists(path) and os.path.getsize(path) > 0:
                if send_file(chat_id, path, f"📄 {f}"):
                    sent += 1
        if sent == 0:
            send_message(chat_id, "❌ لا توجد ملفات للتصدير")
        else:
            send_message(chat_id, f"✅ تم إرسال {sent} ملف")
    
    elif text == "/help":
        send_message(chat_id, """
🤖 **الأوامر المتاحة:**

/generate - توليد إيميلات
/check_ea - فحص EA
/check_ms - فحص Microsoft
/stats - إحصائيات
/export - تصدير الملفات
/help - هذه المساعدة

📁 **ملفات النتائج:**
Linked.txt, NotLinked.txt
Available.txt, NotAvailable.txt, Errors.txt
        """)
    
    else:
        send_message(chat_id, f"❌ أمر غير معروف: {text}\nاستخدم /help")

# ============================================
# 🔍 دالة فحص EA (غير متزامنة - متزامنة)
# ============================================
def start_check_ea(chat_id):
    session = user_sessions.get(chat_id)
    if not session:
        return
    
    emails = read_file(os.path.join(DATA_DIR, 'emails.txt'))
    proxies = session.get('proxies', [])
    proxy_manager = ProxyManager(proxies)
    
    # مسح الملفات القديمة
    clear_file(os.path.join(DATA_DIR, 'Linked.txt'))
    clear_file(os.path.join(DATA_DIR, 'NotLinked.txt'))
    
    linked = []
    not_linked = []
    total = len(emails)
    checked = 0
    start_time = time.time()
    
    for email in emails:
        proxy = proxy_manager.get_next()
        result = check_ea(email, proxy)
        
        if result:
            linked.append(email)
            append_file(os.path.join(DATA_DIR, 'Linked.txt'), email)
        else:
            not_linked.append(email)
            append_file(os.path.join(DATA_DIR, 'NotLinked.txt'), email)
        
        checked += 1
        session['checked'] = checked
        session['linked'] = linked
        session['not_linked'] = not_linked
        
        # تحديث كل 10 إيميلات
        if checked % 10 == 0 or checked == total:
            elapsed = time.time() - start_time
            cpm = int((checked / elapsed) * 60) if elapsed > 0 else 0
            
            msg = f"📊 **{checked}/{total}**\n🔗 مرتبط: {len(linked)}\n❌ غير مرتبط: {len(not_linked)}\n⚡ {cpm} CPM"
            send_message(chat_id, msg)
    
    # انتهاء الفحص
    elapsed = time.time() - start_time
    send_message(chat_id, f"""
✅ **انتهى فحص EA**
🔗 مرتبط: {len(linked)}
❌ غير مرتبط: {len(not_linked)}
⏱️ الوقت: {int(elapsed)} ثانية
📁 حفظ في `Linked.txt` و `NotLinked.txt`
    """)
    
    # إرسال الملفات
    if linked:
        send_file(chat_id, os.path.join(DATA_DIR, 'Linked.txt'), "✅ الإيميلات المرتبطة بـ EA")
    
    # بدء فحص Microsoft تلقائياً
    if not_linked:
        send_message(chat_id, f"🔄 **بدء فحص Microsoft تلقائياً لـ {len(not_linked)} إيميل...**")
        # تحضير الجلسة لـ MS
        user_sessions[chat_id]['step'] = 'checking_ms'
        user_sessions[chat_id]['ms_start_time'] = time.time()
        start_check_ms(chat_id)
    else:
        send_message(chat_id, "✅ لا توجد إيميلات غير مرتبطة لفحص Microsoft")
        del user_sessions[chat_id]

# ============================================
# 🔍 دالة فحص Microsoft
# ============================================
def start_check_ms(chat_id):
    session = user_sessions.get(chat_id)
    if not session:
        return
    
    emails = read_file(os.path.join(DATA_DIR, 'NotLinked.txt'))
    if not emails:
        send_message(chat_id, "❌ لا توجد إيميلات غير مرتبطة")
        return
    
    proxies = read_file(os.path.join(DATA_DIR, 'proxies.txt'))
    proxy_manager = ProxyManager(proxies if proxies else [])
    
    # مسح الملفات القديمة
    clear_file(os.path.join(DATA_DIR, 'Available.txt'))
    clear_file(os.path.join(DATA_DIR, 'NotAvailable.txt'))
    clear_file(os.path.join(DATA_DIR, 'Errors.txt'))
    
    available = []
    not_available = []
    errors = []
    total = len(emails)
    checked = 0
    start_time = time.time()
    
    for email in emails:
        proxy = proxy_manager.get_next()
        result = check_ms(email, proxy)
        
        if result == 'available':
            available.append(email)
            append_file(os.path.join(DATA_DIR, 'Available.txt'), email)
        elif result == 'not_available':
            not_available.append(email)
            append_file(os.path.join(DATA_DIR, 'NotAvailable.txt'), email)
        else:
            errors.append(email)
            append_file(os.path.join(DATA_DIR, 'Errors.txt'), email)
        
        checked += 1
        session['ms_checked'] = checked
        
        # تحديث كل 10 إيميلات
        if checked % 10 == 0 or checked == total:
            elapsed = time.time() - start_time
            cpm = int((checked / elapsed) * 60) if elapsed > 0 else 0
            
            msg = f"📊 **Microsoft {checked}/{total}**\n📤 متاح: {len(available)}\n📥 غير متاح: {len(not_available)}\n⚠️ أخطاء: {len(errors)}\n⚡ {cpm} CPM"
            send_message(chat_id, msg)
    
    # انتهاء الفحص
    elapsed = time.time() - start_time
    send_message(chat_id, f"""
✅ **انتهى فحص Microsoft**
📤 متاح: {len(available)}
📥 غير متاح: {len(not_available)}
⚠️ أخطاء: {len(errors)}
⏱️ الوقت: {int(elapsed)} ثانية
📁 حفظ في الملفات
    """)
    
    # إرسال الملفات
    if available:
        send_file(chat_id, os.path.join(DATA_DIR, 'Available.txt'), "📤 الإيميلات المتاحة")
    if not_available:
        send_file(chat_id, os.path.join(DATA_DIR, 'NotAvailable.txt'), "📥 الإيميلات غير المتاحة")
    if errors:
        send_file(chat_id, os.path.join(DATA_DIR, 'Errors.txt'), "⚠️ الإيميلات التي حدث فيها خطأ")
    
    # حذف الجلسة
    if chat_id in user_sessions:
        del user_sessions[chat_id]

# ============================================
# 🏃 تشغيل البوت
# ============================================
def run_bot():
    print("""
╔══════════════════════════════════════╗
║   🤖 EA + Outlook Checker Bot v2.0   ║
║   توليد جميع الصيغ + فحص EA + MS     ║
╚══════════════════════════════════════╝
    """)
    print(f"📁 مجلد البيانات: {DATA_DIR}")
    print("✅ البوت جاهز لاستقبال الأوامر!")
    
    last_update_id = 0
    
    while True:
        try:
            updates = get_updates(last_update_id + 1)
            
            for update in updates:
                update_id = update.get('update_id', 0)
                if update_id > last_update_id:
                    last_update_id = update_id
                
                message = update.get('message', {})
                chat_id = message.get('chat', {}).get('id')
                text = message.get('text', '')
                
                if chat_id and text:
                    print(f"📩 رسالة من {chat_id}: {text}")
                    process_command(chat_id, text)
            
            time.sleep(2)
        
        except Exception as e:
            print(f"❌ خطأ: {e}")
            time.sleep(5)

# ============================================
# 🚀 تشغيل البوت
# ============================================
if __name__ == '__main__':
    run_bot()
