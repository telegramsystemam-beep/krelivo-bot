import telebot
from telebot import types

TOKEN = "9081123644:AAGv3PKfhdXcllBYkvvy11W07fKub6VLKqQ"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("🛍️ مشاهده محصولات", callback_data="products")
    item2 = types.InlineKeyboardButton("🛒 سبد خرید", callback_data="cart")
    item3 = types.InlineKeyboardButton("📞 پشتیبانی", callback_data="support")
    item4 = types.InlineKeyboardButton("ℹ️ درباره ما", callback_data="about")
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
        bot.answer_callback_query(call.id, "بارگذاری محصولات...")
        bot.send_message(call.message.chat.id, "📦 لیست دسته‌بندی محصولات:\n\n1️⃣ کالای دیجیتال\n2️⃣ پوشاک\n\nکد محصول مورد نظر را انتخاب کنید.")
    elif call.data == "cart":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "🛒 سبد خرید شما در حال حاضر خالی است.")
    elif call.data == "support":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "📞 برای ارتباط با پشتیبانی به آی‌دی زیر پیام دهید:\n@Support_Krelivo")
    elif call.data == "about":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "ℹ️ فروشگاه Krelivo، ارائه دهنده بهترین محصولات با مناسب‌ترین قیمت به صورت ۲۴ ساعته در خدمت شماست.")

if __name__ == "__main__":
    print("Bot Krelivo is running...")
    bot.infinity_polling()
