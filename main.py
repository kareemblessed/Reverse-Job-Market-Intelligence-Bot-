import time
import telebot
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# === Your Telegram Bot Token ===
BOT_TOKEN = ""
bot = telebot.TeleBot(BOT_TOKEN)

# === Handle /start command ===
@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "👋 Hello! Send a question like:\n*Top 10 richest cities in the world* and I’ll ask Runner H.")

# === Handle user message ===
@bot.message_handler(func=lambda msg: True)
def handle_user_input(message):
    prompt = message.text.strip()
    bot.reply_to(message, "⏳ Asking Runner H, please wait...")
    
    try:
        response = run_runner_h(prompt)
        bot.reply_to(message, f"✅ Runner H response:\n\n{response}")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

# === Automate Runner H using Selenium ===
def run_runner_h(prompt):
    # Setup Chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Optional: Remove if you want to see the browser
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)

    try:
        # Load the Runner H page
        driver.get("https://www.hcompany.ai/runner-h")
        time.sleep(10)  # Adjust this if page takes longer

        # Find input box — inspect this manually if it changes
        input_box = driver.find_element(By.TAG_NAME, "textarea")
        input_box.send_keys(prompt)
        input_box.send_keys(Keys.RETURN)

        # Wait for response (increase if needed)
        time.sleep(20)

        # Capture output — this class name may need updating
        response_elements = driver.find_elements(By.CLASS_NAME, "whitespace-pre-line")
        if response_elements:
            return response_elements[-1].text
        else:
            return "No visible response from Runner H."

    finally:
        driver.quit()

# === Start Bot Polling ===
print("🤖 Bot is running...")
bot.polling()
