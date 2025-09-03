import requests
from bs4 import BeautifulSoup
from telegram import Bot
import time
import re
import threading

# ===== إعدادات البوت =====
TELEGRAM_TOKEN = "7950810389:AAHjf-fi2lAxr0G1LJumnBBUh4S6HiCaN9g"
CHAT_ID = "1191340221"

bot = Bot(token=TELEGRAM_TOKEN)

# = الحسابات المتابعة (أضفت الحساب الجديد)
profiles = {
    "واحد": "https://www.facebook.com/tamer.mohmed.5245/",
    "التاني": "https://www.facebook.com/hmam.shkry.2025/",
    "التالت": "https://www.facebook.com/makram.mahros.2025/",
    "حيثَم": "https://www.facebook.com/haitham.ezz.422249/"
}

last_posts = {}

def get_latest_post(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")

        post = soup.find("div", {"data-ad-preview": "message"})
        text = post.text.strip() if post else None

        link_tag = soup.find("a", href=re.compile("/posts/"))
        link = "https://www.facebook.com" + link_tag["href"] if link_tag else url

        images = [img["src"] for img in soup.find_all("img", src=True) if "scontent" in img["src"]]
        videos = [video["src"] for video in soup.find_all("video") if video.get("src")]

        live = None
        live_tag = soup.find("a", href=re.compile("/live"))
        if live_tag:
            live = "https://www.facebook.com" + live_tag["href"]

        return text, link, images, videos, live
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None, None, [], [], None

def check_posts():
    while True:
        for name, url in profiles.items():
            text, link, images, videos, live = get_latest_post(url)
            if text and last_posts.get(name) != text:
                last_posts[name] = text
                msg = f"📢 بوست جديد من *{name}*:\n\n{text}\n\n🔗 {link}"
                bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode="Markdown")

                for img in images[:3]:
                    bot.send_photo(chat_id=CHAT_ID, photo=img)

                for vid in videos[:2]:
                    bot.send_message(chat_id=CHAT_ID, text=f"🎥 فيديو: {vid}")

                if live:
                    bot.send_message(chat_id=CHAT_ID, text=f"🔴 {name} فاتح لايف: {live}")

        time.sleep(30)  # يفحص كل 30 ثانية

if __name__ == "__main__":
    # رسالة أولية في اللوجات للتأكد من التشغيل
    print("✅ Bot started successfully!")

    threading.Thread(target=check_posts, daemon=True).start()
    bot.send_message(chat_id=CHAT_ID, text="🚀 البوت اشتغل وجاري المتابعة...")
    # من غير Updater لأننا مجرد تابع
    while True:
        time.sleep(1)
