import os
import telebot
from flask import Flask
import threading

TOKEN = "9081123644:AAGv3PKfhdXcllBYkvvy11W07fKub6VLKqQ"
bot = telebot.TeleBot(TOKEN)

# ساخت وب‌سرور فلاسگ با قالب گرافیکی مینی‌پپ
server = Flask(__name__)

@server.route('/')
def webhook():
    return """
    <!DOCTYPE html>
    <html lang="fa" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>فروشگاه Krelivo</title>
        <style>
            body { background-color: #121212; color: #ffffff; font-family: Tahoma, sans-serif; text-align: center; padding: 40px; margin: 0; }
            .container { background: #1e1e1e; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.6); max-width: 400px; margin: auto; }
            h1 { color: #2ea6ff; font-size: 22px; }
            p { color: #cccccc; font-size: 14px; line-height: 1.6; }
            .btn { display: inline-block; background: #2ea6ff; color: white; padding: 10px 20px; border-radius: 8px; text-decoration: none; margin-top: 15px; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🛍️ فروشگاه Krelivo</h1>
            <p>خوش آمدید! فروشگاه آنلاین شما با موفقیت روی سرور فعال شد و آماده‌ی استفاده است.</p>
            <a href="https://t.me/Krelivo_bot" class="btn">بازگشت به ربات</a>
        </div>
    </body>
    </html>
    """, 200

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    item1 = telebot.types.InlineKeyboardButton("🛍️ مشاهده محصولات", callback_data="products")
    item2 = telebot.types.InlineKeyboardButton("🛒 سبد خرید", callback_data="cart")
    item3 = telebot.types.InlineKeyboardButton("📞 پشتیبانی", callback_data="support")
    item4 = telebot.types.InlineKeyboardButton("ℹ️ درباره ما", callback_data="about")
    markup.add(item1, item2, item3, item4)
    
    welcome_text = (
        f"سلام {user_name} عزیز! 🌹\n"
        "به فروشگاه **Krelivo** خوش آمدید.\n\n"
        "لطفاً از منوی زیر گزینه مورد نظرتان را انتخاب کنید:"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "products":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "📦 لیست دسته‌بندی محصولات:\n\n1️⃣ کالای دیجیتال\n2️⃣ پوشاک\n\nلطفاً عدد ۱ یا ۲ را ارسال کنید.")
    elif call.data == "cart":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "🛒 سبد خرید شما در حال حاضر خالی است.")
    elif call.data == "support":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "📞 برای ارتباط با پشتیبانی به آی‌دی زیر پیام دهید:\n@Support_Krelivo")
    elif call.data == "about":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "ℹ️ فروشگاه Krelivo، ارائه دهنده بهترین محصولات با مناسب‌ترین قیمت.")

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    text = message.text.strip()
    if text == "1" or "دیجیتال" in text:
        bot.send_message(message.chat.id, "📱 **بخش کالای دیجیتال:**\n- گوشی موبایل و لوازم جانبی\n- هدست و ساعت هوشمند")
    elif text == "2" or "پوشاک" in text:
        bot.send_message(message.chat.id, "👕 **بخش پوشاک:**\n- هودی و تیشرت\n- شلوار و اکسسوری")
    else:
        bot.send_message(message.chat.id, "دستور نامعتبر! برای مشاهده منو لطفا /start را بفرستید.")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    threading.Thread(target=server.run, kwargs={"host": "0.0.0.0", "port": port, "debug": False, "use_reloader": False}).start()
    
    try:
        bot.remove_webhook()
    except Exception as e:
        print(e)
        
    bot.infinity_polling()
