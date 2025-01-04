import os
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError
import asyncio
import time

# إنشاء مجلد الجلسات إذا لم يكن موجودًا
if not os.path.exists("Sessions"):
    os.makedirs("Sessions")

# تعريف المتغيرات
API_ID = '27975562'  # استبدل بـ API ID الخاص بك
API_HASH = 'd125196a72d2886145180572380395e0'  # استبدل بـ API Hash الخاص بك

# قائمة الحسابات
accounts = []

# تحميل الحسابات من مجلد الجلسات
def load_accounts():
    session_files = [f for f in os.listdir("Sessions") if f.endswith(".session")]
    for session_file in session_files:
        session_name = session_file.replace(".session", "")
        accounts.append({
            "name": session_name,
            "client": TelegramClient(f"Sessions/{session_name}", API_ID, API_HASH)
        })

# تسجيل دخول حساب جديد
async def add_account():
    phone_number = input("أدخل رقم الهاتف (مع رمز الدولة): ")
    session_name = input("أدخل اسمًا لهذا الحساب (لحفظ الجلسة): ")
    client = TelegramClient(f"Sessions/{session_name}", API_ID, API_HASH)
    await client.start(phone=phone_number)
    print(f"تم تسجيل الدخول بنجاح وحفظ الجلسة باسم {session_name}!")
    accounts.append({"name": session_name, "client": client})

# الانضمام إلى قناة أو مجموعة
async def join_chat(account, link):
    try:
        await account.connect()
        await account.join_chat(link)
        print(f"الحساب {account.session.filename} انضم بنجاح إلى {link}")
    except FloodWaitError as e:
        print(f"تم حظر الحساب {account.session.filename} لمدة {e.seconds} ثانية بسبب الطلبات الكثيرة.")
        time.sleep(e.seconds)
    except Exception as e:
        print(f"حدث خطأ: {e}")

# الانضمام إلى دردشة صوتية
async def join_voice_chat(account, link):
    try:
        await account.connect()
        entity = await account.get_entity(link)
        if entity:
            await account.join_group_call(entity)
            print(f"الحساب {account.session.filename} انضم إلى الدردشة الصوتية بنجاح.")
    except FloodWaitError as e:
        print(f"تم حظر الحساب {account.session.filename} لمدة {e.seconds} ثانية بسبب الطلبات الكثيرة.")
        time.sleep(e.seconds)
    except Exception as e:
        print(f"حدث خطأ: {e}")

# واجهة التحكم
async def control_panel():
    while True:
        print("\n--- واجهة التحكم ---")
        print("1. تسجيل دخول حساب جديد")
        print("2. الانضمام إلى قناة/مجموعة (جميع الحسابات)")
        print("3. الانضمام إلى قناة/مجموعة (حساب محدد)")
        print("4. الانضمام إلى دردشة صوتية (جميع الحسابات)")
        print("5. الانضمام إلى دردشة صوتية (حساب محدد)")
        print("6. الخروج")
        choice = input("اختر رقمًا: ")

        if choice == "1":
            await add_account()
        elif choice == "2":
            link = input("أدخل رابط القناة/المجموعة: ")
            for account in accounts:
                await join_chat(account["client"], link)
        elif choice == "3":
            link = input("أدخل رابط القناة/المجموعة: ")
            account_index = int(input("أدخل رقم الحساب (بدءًا من 0): "))
            if 0 <= account_index < len(accounts):
                await join_chat(accounts[account_index]["client"], link)
            else:
                print("رقم الحساب غير صحيح!")
        elif choice == "4":
            link = input("أدخل رابط الدردشة الصوتية: ")
            for account in accounts:
                await join_voice_chat(account["client"], link)
        elif choice == "5":
            link = input("أدخل رابط الدردشة الصوتية: ")
            account_index = int(input("أدخل رقم الحساب (بدءًا من 0): "))
            if 0 <= account_index < len(accounts):
                await join_voice_chat(accounts[account_index]["client"], link)
            else:
                print("رقم الحساب غير صحيح!")
        elif choice == "6":
            break
        else:
            print("اختيار غير صحيح!")

# تشغيل البرنامج
if __name__ == "__main__":
    load_accounts()
    asyncio.run(control_panel())
