import os
import telebot
from telebot import types
from flask import Flask
import threading

TOKEN = "9081123644:AAGv3PKfhdXcllBYkvvy11W07fKub6VLKqQ"
bot = telebot.TeleBot(TOKEN)

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

# منوی /start با دکمه‌های شیشه‌ای کامل
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    btn_catalog = types.InlineKeyboardButton("🛍️ Catalog", callback_data="catalog")
    btn_cart = types.InlineKeyboardButton("🛒 Cart", callback_data="cart")
    btn_profile = types.InlineKeyboardButton("👤 Profile & Orders", callback_data="profile")
    btn_premium = types.InlineKeyboardButton("⭐ Premium Plans", callback_data="premium")
    btn_support = types.InlineKeyboardButton("📝 Support Ticket", callback_data="support")
    btn_wallet = types.InlineKeyboardButton("💎 Tonkeeper Pay", url="https://tonkeeper.com/")
    
    markup.add(btn_catalog, btn_cart, btn_profile, btn_premium, btn_support, btn_wallet)
    
    welcome_text = (
        "Welcome to Krelivo Store! 🚀\n\n"
        "Explore our exclusive digital products, manage your plans, and access our services below."
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

# دستورات متنی منو
@bot.message_handler(commands=['products'])
def cmd_products(message):
    catalog_menu(message.chat.id)

@bot.message_handler(commands=['cart'])
def cmd_cart(message):
    bot.send_message(message.chat.id, "🛒 **Your Shopping Cart:**\nYour cart is currently empty.", parse_mode="Markdown")

@bot.message_handler(commands=['profile'])
def cmd_profile(message):
    bot.send_message(message.chat.id, "👤 **Your Account & Orders:**\nID: {}\nStatus: Active".format(message.from_user.id), parse_mode="Markdown")

@bot.message_handler(commands=['premium'])
def cmd_premium(message):
    premium_menu(message.chat.id)

@bot.message_handler(commands=['support', 'ticket'])
def cmd_support(message):
    bot.send_message(
        message.chat.id,
        "📝 **Support Ticket**\n\nPlease type and send your question or issue in a single message. We will reply to you soon.",
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['help'])
def cmd_help(message):
    bot.send_message(message.chat.id, "📖 **Guide & FAQ:**\nUse the menu buttons to navigate through Krelivo Store easily.", parse_mode="Markdown")

# منوی اشتراک‌ها (مثل عکس دوم)
def premium_menu(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_single = types.InlineKeyboardButton("⭐ Single Package – 50 ⭐️", callback_data="buy_single")
    btn_basic = types.InlineKeyboardButton("⭐ Basic (30 Days) – 290 ⭐️", callback_data="buy_basic")
    btn_pro = types.InlineKeyboardButton("⭐ Pro (30 Days) – 690 ⭐️", callback_data="buy_pro")
    btn_ultra = types.InlineKeyboardButton("⭐ Ultra (30 Days) – 1990 ⭐️", callback_data="buy_ultra")
    btn_back = types.InlineKeyboardButton("« Back to Main Menu", callback_data="main_menu")
    
    markup.add(btn_single, btn_basic, btn_pro, btn_ultra, btn_back)
    
    bot.send_message(
        chat_id,
        "⭐ **Special Offers & Plans (30 Days)**\nChoose your subscription plan below:",
        reply_markup=markup,
        parse_mode="Markdown"
    )

def catalog_menu(chat_id):
    markup = types.InlineKeyboardMarkup()
    btn_back = types.InlineKeyboardButton("« Back", callback_data="main_menu")
    markup.add(btn_back)
    bot.send_message(chat_id, "🛍️ **Catalog:**\nProducts will be loaded here soon. Stay tuned!", reply_markup=markup, parse_mode="Markdown")

# مدیریت کلیک دکمه‌ها
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "support":
        bot.answer_callback_query(call.id)
        bot.send_message(
            call.message.chat.id,
            "📝 **Support Ticket**\n\nPlease type and send your question or issue in a single message.",
            parse_mode="Markdown"
        )
    elif call.data == "catalog":
        bot.answer_callback_query(call.id)
        catalog_menu(call.message.chat.id)
    elif call.data == "cart":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "🛒 **Your Shopping Cart:**\nYour cart is empty.")
    elif call.data == "profile":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, f"👤 **Profile:**\nID: {call.from_user.id}")
    elif call.data == "premium":
        bot.answer_callback_query(call.id)
        premium_menu(call.message.chat.id)
    elif call.data == "main_menu":
        bot.answer_callback_query(call.id)
        send_welcome(call.message)
    elif call.data.startswith("buy_"):
        bot.answer_callback_query(call.id, "Redirecting to payment...")
        bot.send_message(call.message.chat.id, "💎 To complete your purchase, please use our official Tonkeeper link or contact support.")

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    t = threading.Thread(target=run_flask)
    t.start()
    bot.infinity_polling()
