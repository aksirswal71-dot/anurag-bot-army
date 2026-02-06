import telebot
import time
import random
import threading
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- सेटिंग्स ---
API_TOKEN = '8320030477:AAFp0-InBUjwmE4qfn91e8B1ZsjReRCyWk8'
ADMIN_ID = '7685030597'
TARGET_URL = 'https://smarttoolspro2026.blogspot.com/'

bot = telebot.TeleBot(API_TOKEN)
is_running = False

DEVICE_IDENTITIES = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15",
    "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
]

def get_high_cpm_proxy():
    try:
        response = requests.get("https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=us,ca,gb,de&ssl=all&anonymity=all")
        if response.status_code == 200:
            proxies = response.text.split('\r\n')
            return random.choice([p for p in proxies if p])
    except:
        return None

def run_bot_mission():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f'user-agent={random.choice(DEVICE_IDENTITIES)}')
    
    proxy = get_high_cpm_proxy()
    if proxy:
        chrome_options.add_argument(f'--proxy-server={proxy}')

    # क्लाउड के लिए ऑटो-ड्राइवर सेटअप
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        driver.get(TARGET_URL)
        wait = WebDriverWait(driver, 20)
        try:
            # बटन पर क्लिक करने की कोशिश
            blue_button = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'Click')))
            driver.execute_script("arguments[0].click();", blue_button)
        except: pass
        
        time.sleep(random.randint(15, 25))
    finally:
        driver.quit()

def army_manager(target):
    global is_running
    current_done = 0
    # रैंडम गैप ताकि नेचुरल लगे
    while current_done < target and is_running:
        threading.Thread(target=run_bot_mission).start()
        current_done += 1
        if current_done % 5 == 0:
            bot.send_message(ADMIN_ID, f"📊 प्रोग्रेस: {current_done}/{target} क्लिक पूरे, अनुराग बाबू।")
        
        # 24 घंटे में काम बांटने के लिए समय का गैप
        gap = (86400 / target) * random.uniform(0.5, 1.5)
        time.sleep(gap)
    
    bot.send_message(ADMIN_ID, "🏁 आज का मिशन पूरा हुआ!")
    is_running = False

@bot.message_handler(commands=['target'])
def set_target(message):
    global is_running
    if str(message.chat.id) != ADMIN_ID: return
    try:
        val = int(message.text.split()[1])
        is_running = True
        bot.reply_to(message, f"🚀 मिशन शुरू! {val} रैंडम विज़िट्स बादलों से भेजी जा रही हैं...")
        threading.Thread(target=army_manager, args=(val,)).start()
    except:
        bot.reply_to(message, "बाबू, ऐसे लिखो: /target 100")

bot.polling()
