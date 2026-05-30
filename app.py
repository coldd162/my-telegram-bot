import os
import telebot
from flask import Flask
from threading import Thread

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHANNEL_USERNAME = "@cold_entry"
PARTNER_LINK = "https://one-vv0786.com/casino/list?open=register&p=cykx"  # 

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running", 200

@app.route('/health')
def health():
    return "OK", 200

def check_subscription(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ['member', 'creator', 'administrator']
    except:
        return False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Напиши /guide, чтобы получить ссылку.")

@bot.message_handler(commands=['guide'])
def send_guide(message):
    user_id = message.from_user.id
    if check_subscription(user_id):
        keyboard = telebot.types.InlineKeyboardMarkup()
        button = telebot.types.InlineKeyboardButton("Перейти к 1win", url=PARTNER_LINK)
        keyboard.add(button)
        bot.reply_to(message, "✅ Ты подписан! Переходи по ссылке:", reply_markup=keyboard)
    else:
        keyboard = telebot.types.InlineKeyboardMarkup()
        button = telebot.types.InlineKeyboardButton("Подписаться на канал", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")
        keyboard.add(button)
        bot.reply_to(message, f"❌ Подпишись на канал {CHANNEL_USERNAME} и повтори команду /guide", reply_markup=keyboard)

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    t = Thread(target=run_bot)
    t.start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
