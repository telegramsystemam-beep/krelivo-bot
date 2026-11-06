import os
import telebot

# توکن ربات شما
TOKEN = "9081123644:AAGv3PKfhdXcllBYkvvy11W07fKub6VLKqQ"
bot = telebot.TeleBot(TOKEN)

# پاسخ به دستور استارت
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    welcome_text = (
        f"Welcome to Krelivo Store, {user_name}! 🚀\n\n"
        "Explore our digital products and tools.\n"
        "Use /help to see available options."
    )
    bot.reply_to(message, welcome_text)

# پاسخ به دستور راهنما
@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = (
        "🛍️ **Krelivo Support:**\n\n"
        "To purchase digital products or inquire, please contact our support or check our official channel."
    )
    bot.reply_to(message, help_text, parse_mode="Markdown")

# اجرای ربات به روش Polling
if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()
