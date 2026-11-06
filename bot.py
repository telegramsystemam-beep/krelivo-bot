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

# منوی اصلی
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_catalog = types.InlineKeyboardButton("🛍️ Catalog", callback_data="catalog")
    btn_cart = types.InlineKeyboardButton("🛒 Cart", callback_data="cart")
    btn_profile = types.InlineKeyboardButton("👤 Profile", callback_data="profile")
    btn_premium = types.InlineKeyboardButton("⭐ Premium Plans", callback_data="premium")
    btn_support = types.InlineKeyboardButton("📝 Support Ticket", callback_data="support")
    btn_wallet = types.InlineKeyboardButton("💎 Tonkeeper Pay", url="https://tonkeeper.com/")
    markup.add(btn_catalog, btn_cart, btn_profile, btn_premium, btn_support, btn_wallet)
    
    welcome_text = "Welcome to Krelivo Store! 🚀\n\nExplore our exclusive digital products below."
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

# متدهای ساخت منوها با قابلیت ویرایش پیام (جلوگیری از ارسال پیام جدید)
def show_main_menu(chat_id, message_id):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🛍️ Catalog", callback_data="catalog"),
        types.InlineKeyboardButton("🛒 Cart", callback_data="cart"),
        types.InlineKeyboardButton("👤 Profile", callback_data="profile"),
        types.InlineKeyboardButton("⭐ Premium Plans", callback_data="premium"),
        types.InlineKeyboardButton("📝 Support Ticket", callback_data="support"),
        types.InlineKeyboardButton("💎 Tonkeeper Pay", url="https://tonkeeper.com/")
    )
    bot.edit_message_text("Welcome to Krelivo Store! 🚀\n\nExplore our exclusive digital products below.", chat_id, message_id, reply_markup=markup)

def show_premium_menu(chat_id, message_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("⭐ Single Package – 50 ⭐️", callback_data="pay_single"),
        types.InlineKeyboardButton("⭐ Basic (30 Days) – 290 ⭐️", callback_data="pay_basic"),
        types.InlineKeyboardButton("⭐ Pro (30 Days) – 690 ⭐️", callback_data="pay_pro"),
        types.InlineKeyboardButton("⭐ Ultra (30 Days) – 1990 ⭐️", callback_data="pay_ultra"),
        types.InlineKeyboardButton("« Back to Main Menu", callback_data="main_menu")
    )
    bot.edit_message_text("⭐ **Special Offers & Plans (30 Days)**\nChoose your subscription plan below:", chat_id, message_id, reply_markup=markup, parse_mode="Markdown")

def show_catalog(chat_id, message_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("« Back to Main Menu", callback_data="main_menu"))
    bot.edit_message_text("🛍️ **Catalog:**\nProducts will be loaded here soon. Stay tuned!", chat_id, message_id, reply_markup=markup, parse_mode="Markdown")

# مدیریت کلیک دکمه‌ها
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    
    if call.data == "main_menu":
        bot.answer_callback_query(call.id)
        show_main_menu(chat_id, message_id)
    elif call.data == "premium":
        bot.answer_callback_query(call.id)
        show_premium_menu(chat_id, message_id)
    elif call.data == "catalog":
        bot.answer_callback_query(call.id)
        show_catalog(chat_id, message_id)
    elif call.data == "cart":
        bot.answer_callback_query(call.id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("« Back to Main Menu", callback_data="main_menu"))
        bot.edit_message_text("🛒 **Your Shopping Cart:**\nYour cart is empty.", chat_id, message_id, reply_markup=markup, parse_mode="Markdown")
    elif call.data == "profile":
        bot.answer_callback_query(call.id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("« Back to Main Menu", callback_data="main_menu"))
        bot.edit_message_text(f"👤 **Profile:**\nID: {chat_id}\nStatus: Active", chat_id, message_id, reply_markup=markup, parse_mode="Markdown")
    elif call.data == "support":
        bot.answer_callback_query(call.id)
        bot.send_message(chat_id, "📝 **Support Ticket**\n\nPlease type and send your question or issue in a single message.", parse_mode="Markdown")
    elif call.data.startswith("pay_"):
        bot.answer_callback_query(call.id)
        # تعیین قیمت بر اساس نوع اشتراک (واحد بر حسب ستاره XTR)
        prices = {
            "pay_single": 50,
            "pay_basic": 290,
            "pay_pro": 690,
            "pay_ultra": 1990
        }
        plan_name = call.data.replace("pay_", "").capitalize()
        amount = prices.get(call.data, 50)
        
        # ارسال فاکتور رسمی تلگرام برای پرداخت با ستاره
        bot.send_invoice(
            chat_id=chat_id,
            title=f"Krelivo {plan_name} Plan",
            description=f"Subscription for {plan_name} package in Krelivo Store (30 Days)",
            invoice_payload=f"krelivo_{plan_name.lower()}",
            provider_token="",  # برای ستاره تلگرام باید خالی باشد
            currency="XTR",     # کد ارز ستاره تلگرام
            prices=[types.LabeledPrice(label=f"{plan_name} Plan", amount=amount)]
        )

# پردازش نهایی پرداخت موفق ستاره
@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    bot.send_message(message.chat.id, "🎉 Payment successful! Thank you for your purchase. Your plan is now active.")

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    t = threading.Thread(target=run_flask)
    t.start()
    bot.infinity_polling()
