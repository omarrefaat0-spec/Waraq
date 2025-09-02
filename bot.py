import requests
import time
import telegram

# ====== إعدادات البوت ======
BOT_TOKEN = "7950810389:AAHjf-fi2lAxr0G1LJumnBBUh4S6HiCaN9g"
CHAT_ID = "1191340221"

# الحسابات اللي عايز تتابعها
PROFILES = [
    "https://www.facebook.com/tamer.mohmed.5245",
    "https://www.facebook.com/hmam.shkry.2025",
    "https://www.facebook.com/makram.mahros.2025"
]

# مكتبة تيليجرام
bot = telegram.Bot(token=BOT_TOKEN)

# دالة تجيب آخر بوست من لينك الحساب
def get_last_post(profile_url):
    # هنا placeholder
    # تقدر تستخدم Graph API أو scraping
    # دلوقتي بس هرجع بوست وهمي للتجربة
    return f"📌 آخر بوست من {profile_url}"

# برنامج البوت الأساسي
def run_bot():
    sent_posts = set()
    while True:
        for profile in PROFILES:
            post = get_last_post(profile)
            if post and post not in sent_posts:
                bot.send_message(chat_id=CHAT_ID, text=post)
                sent_posts.add(post)
        time.sleep(60)  # كل دقيقة يعمل تشيك

if __name__ == "__main__":
    run_bot()
