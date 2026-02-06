import os
import time
import random
import threading
import telebot
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- CONFIGURATION (सब कुछ सेट है) ---
TOKEN = '8320030477:AAFp0-InBUjwmE4qfn91e8B1ZsjReRCyWk8' 
TARGET_URL = 'https://smarttoolspro2026.blogspot.com/'
ADMIN_ID = '7685030597'

bot = telebot.TeleBot(TOKEN)

# प्रॉक्सी लिस्ट
PROXIES = [
    "http://72.10.252.134:11690",
    "http://154.21.137.10:6530",
    "http://144.168.164.217:5844",
    "http://154.92.112.98:5641"
]

def run_bot_mission(target_count):
    completed = 0
    # 24 घंटे (86400 सेकंड) में टारगेट को बराबर बांटना
    base_gap = 86400 / target_count 
    
    bot.send_message(ADMIN_ID, f"🚀 मिशन शुरू! {target_count} विज़िट्स अगले 24 घंटों में पूरी की जाएंगी।\nऔसत गैप: {round(base_gap, 2)} सेकंड।")

    while completed < target_count:
        proxy = random.choice(PROXIES)
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument(f'--proxy-server={proxy}')
        
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1"
        ]
        chrome_options.add_argument(f'user-agent={random.choice(user_agents)}')

        driver = None
        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.set_page_load_timeout(50)
            
            # वेबसाइट पर पहुँचना
            driver.get(TARGET_URL)
            
            # --- बटन क्लिक लॉजिक ---
            try:
                # 1. क्लिक करने से पहले 10-20 सेकंड का रैंडम इंतज़ार
                time.sleep(random.randint(10, 20))

                wait = WebDriverWait(driver, 20)
                # नीले बटन को उसके नाम 'CONVERT & SAVE' से ढूंढना
                blue_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'CONVERT & SAVE')] | //input[@value='CONVERT & SAVE']")))
                
                # बटन पर क्लिक
                driver.execute_script("arguments[0].click();", blue_button)
                
                # 2. क्लिक करने के बाद फिर से 10-20 सेकंड का रैंडम इंतज़ार
                time.sleep(random.randint(10, 20))
            except:
                pass # अगर बटन न मिले तो भी गिनती जारी रहे

            completed += 1
            # हर विज़िट के बाद अनुराग बाबू को रिपोर्ट देना
            bot.send_message(ADMIN_ID, f"✅ विज़िट {completed}/{target_count} सफल!\n🌐 स्टेटस: सक्रिय\n⏳ अगली विज़िट कतार (queue) में है।")
            
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(15) # एरर पर थोड़ा ब्रेक
            continue
        finally:
            if driver:
                driver.quit()

        # 24 घंटे के हिसाब से गैप को रैंडम (80%-120%) बनाना
        sleep_time = base_gap * random.uniform(0.8, 1.2)
        time.sleep(max(sleep_time, 15)) # कम से कम 15 सेकंड का गैप सुरक्षा के लिए

    bot.send_message(ADMIN_ID, f"🏁 मुबारक हो अनुराग बाबू! {target_count} विज़िट्स का मिशन सफलतापूर्वक पूरा हुआ।")

@bot.message_handler(commands=['target'])
def start_target(message):
    if str(message.chat.id) != ADMIN_ID:
        return
    try:
        count = int(message.text.split()[1])
        threading.Thread(target=run_bot_mission, args=(count,)).start()
        bot.reply_to(message, f"🫡 जो हुक्म कमांडर अनुराग! {count} विज़िट्स का मिशन 24 घंटे के लिए सेट कर दिया गया है।")
    except:
        bot.reply_to(message, "❌ सही तरीका: /target 50")

bot.polling()
