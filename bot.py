import os
import telebot
from telebot import types
from flask import Flask
import threading
from datetime import datetime

TOKEN = "9081123644:AAGv3PKfhdXcllBYkvvy11W07fKub6VLKqQ"
bot = telebot.TeleBot(TOKEN)

app = Flask('')

user_languages = {}
user_states = {}
user_invites = {}          # تعداد دعوت‌های کل هر کاربر
user_invite_tier = {}      # مرحله فعلی پاداش دعوت کاربر (۱ تا ۴ به بعد)
user_referred = set()
user_balances = {}         # سکه‌های KP
user_last_checkin = {}     # تاریخ آخرین حضور روزانه
user_nicknames = {}        # نام مستعار/پروفایل کاربران

TRANSLATIONS = {
    "en": {
        "welcome": "Welcome to Krelivo Gaming Hub! 🚀\n\nChoose an option below:",
        "catalog": "📦 Catalog", "cart": "🛒 Cart", "profile": "👤 Profile",
        "premium": "⭐ Premium", "affiliate": "🤝 Referrals & Tiers",
        "language": "🌐 Language", "support": "🎫 Support",
        "leaderboard": "🏆 Leaderboard", "daily": "🎁 Daily Bonus",
        "rewards_shop": "🎁 Rewards Shop", "back": "🔙 Back",
        "new_ticket": "🎫 New Ticket", "my_tickets": "📁 My Tickets",
        "privacy": "🔒 Privacy Policy", "terms": "📄 Terms of Service",
        "support_text": "🎫 **Support Center**\n\nChoose an option:",
        "ticket_prompt": "📝 Please send your message to support:",
        "ticket_success": "✅ Message sent successfully!"
    },
    "fa": {
        "welcome": "به هاب گیمینگ کرلیوو خوش آمدید! 🚀\n\nاز گزینه‌های زیر استفاده کنید:",
        "catalog": "📦 کاتالوگ", "cart": "🛒 سبد خرید", "profile": "👤 پروفایل",
        "premium": "⭐ پریمیوم", "affiliate": "🤝 سیستم معرفی و سطوح",
        "language": "🌐 زبان", "support": "🎫 پشتیبانی",
        "leaderboard": "🏆 لیدربورد", "daily": "🎁 حضور روزانه",
        "rewards_shop": "🎁 فروشگاه جوایز", "back": "🔙 بازگشت",
        "new_ticket": "🎫 تیکت جدید", "my_tickets": "📁 تیکت‌های من",
        "privacy": "🔒 حریم خصوصی", "terms": "📄 شرایط خدمات",
        "support_text": "🎫 **مرکز پشتیبانی**\n\nلطفاً یکی را انتخاب کنید:",
        "ticket_prompt": "📝 لطفاً پیام خود را برای پشتیبانی بفرستید:",
        "ticket_success": "✅ پیام شما با موفقیت ارسال شد!"
    }
}

@app.route('/')
def home():
    return "Bot is alive and running!"

def get_user_name(user_id, default_name):
    return user_nicknames.get(user_id, f"User_{user_id}")

def show_main_menu(chat_id, message_id=None, is_new=False):
    lang = user_languages.get(chat_id, "en")
    t = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(t["catalog"], callback_data="catalog"),
        types.InlineKeyboardButton(t["cart"], callback_data="cart"),
        types.InlineKeyboardButton(t["profile"], callback_data="profile"),
        types.InlineKeyboardButton(t["rewards_shop"], callback_data="rewards_shop"),
        types.InlineKeyboardButton(t["affiliate"], callback_data="affiliate"),
        types.InlineKeyboardButton(t["daily"], callback_data="daily_bonus"),
        types.InlineKeyboardButton(t["leaderboard"], callback_data="leaderboard"),
        types.InlineKeyboardButton(t["premium"], callback_data="premium"),
        types.InlineKeyboardButton(t["language"], callback_data="language"),
        types.InlineKeyboardButton(t["support"], callback_data="support")
    )
    
    if is_new or not message_id:
        bot.send_message(chat_id, t["welcome"], reply_markup=markup)
    else:
        try:
            bot.edit_message_text(t["welcome"], chat_id, message_id, reply_markup=markup)
        except:
            bot.send_message(chat_id, t["welcome"], reply_markup=markup)

@bot.message_handler(commands=['start'])
def cmd_start(message):
    user_id = message.from_user.id
    args = message.text.split()
    if len(args) > 1 and args[1].startswith("ref_"):
        try:
            inviter_id = int(args[1].replace("ref_", ""))
            if inviter_id != user_id and user_id not in user_referred:
                user_referred.add(user_id)
                user_invites[inviter_id] = user_invites.get(inviter_id, 0) + 1
                user_balances[inviter_id] = user_balances.get(inviter_id, 0) + 10
                try:
                    bot.send_message(inviter_id, "✨ New referral joined! +10 KP added.")
                except:
                    pass
        except:
            pass
    show_main_menu(message.chat.id, None, is_new=True)

@bot.message_handler(commands=['profile'])
def cmd_profile(message):
    show_profile_page(message.chat.id)

def show_profile_page(chat_id, message_id=None):
    lang = user_languages.get(chat_id, "en")
    t = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    balance = user_balances.get(chat_id, 0)
    invites = user_invites.get(chat_id, 0)
    tier = user_invite_tier.get(chat_id, 1)
    nickname = user_nicknames.get(chat_id, f"User_{chat_id}")
    
    # تعیین هدف دعوت مرحله‌ای مثل بازی
    targets = {1: 100, 2: 200, 3: 500}
    current_target = targets.get(tier, 1000)
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("✏️ تغییر نام کاربری (Nickname)", callback_data="set_nickname"),
        types.InlineKeyboardButton(t["back"], callback_data="main_menu")
    )
    
    text = (
        f"👤 **پروفایل کاربری شما:**\n"
        f"• نام: **{nickname}**\n"
        f"• شناسه: `{chat_id}`\n"
        f"• موجودی KP: **{balance} KP**\n"
        f"• سطح دعوت فعلی: **مرحله {tier}** (پیشرفت: {invites} / {current_target})\n"
        f"• وضعیت اشتراک: عادی"
    )
    if message_id:
        bot.edit_message_text(text, chat_id, message_id, reply_markup=markup, parse_mode="Markdown")
    else:
        bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    lang = user_languages.get(chat_id, "en")
    t = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    
    if call.data == "main_menu":
        bot.answer_callback_query(call.id)
        show_main_menu(chat_id, message_id)
    elif call.data == "profile":
        bot.answer_callback_query(call.id)
        show_profile_page(chat_id, message_id)
    elif call.data == "set_nickname":
        bot.answer_callback_query(call.id)
        user_states[chat_id] = "waiting_for_nickname"
        bot.send_message(chat_id, "✏️ لطفاً نام کاربری (Nickname) جدید خود را بفرستید:")
    elif call.data == "rewards_shop":
        bot.answer_callback_query(call.id)
        balance = user_balances.get(chat_id, 0)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("⭐ خرید ۱ ماه اشتراک (۶۰۰ KP)", callback_data="buy_sub_kp"),
            types.InlineKeyboardButton(t["back"], callback_data="main_menu")
        )
        text = f"🎁 **فروشگاه جوایز KP**\n\nموجودی شما: **{balance} KP**\n\nبا داشتن ۶۰۰ KP می‌توانید ۱ ماه اشتراک رایگان دریافت کنید!"
        bot.edit_message_text(text, chat_id, message_id, reply_markup=markup, parse_mode="Markdown")
    elif call.data == "buy_sub_kp":
        balance = user_balances.get(chat_id, 0)
        if balance >= 600:
            user_balances[chat_id] = balance - 600
            bot.answer_callback_query(call.id, "🎉 تبریک! ۱ ماه اشتراک رایگان با موفقیت برای شما فعال شد.", show_alert=True)
        else:
            bot.answer_callback_query(call.id, f"❌ موجودی کافی نیست! شما به {600 - balance} KP دیگر نیاز دارید.", show_alert=True)
    elif call.data == "affiliate":
        bot.answer_callback_query(call.id)
        show_affiliate_menu_edit(chat_id, message_id)
    elif call.data == "daily_bonus":
        today = datetime.now().strftime("%Y-%m-%d")
        if user_last_checkin.get(chat_id) == today:
            bot.answer_callback_query(call.id, "❌ امروز هدیه روزانه رو گرفتی!", show_alert=True)
        else:
            user_last_checkin[chat_id] = today
            user_balances[chat_id] = user_balances.get(chat_id, 0) + 2
            bot.answer_callback_query(call.id, "🎉 موفق بودی! +2 KP به حسابت اضافه شد.", show_alert=True)
        show_affiliate_menu_edit(chat_id, message_id)
    elif call.data == "leaderboard":
        bot.answer_callback_query(call.id)
        sorted_users = sorted(user_balances.items(), key=lambda x: x[1], reverse=True)[:10]
        lb_text = "🏆 **لیدربورد برترین‌های KP**\n\n"
        if sorted_users:
            for idx, (uid, bal) in enumerate(sorted_users, 1):
                name = user_nicknames.get(uid, f"User_{uid}")
                lb_text += f"{idx}. {name} — **{bal} KP**\n"
        else:
            lb_text += "هنوز رکوردی ثبت نشده است."
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(t["back"], callback_data="main_menu"))
        bot.edit_message_text(lb_text, chat_id, message_id, reply_markup=markup, parse_mode="Markdown")
    elif call.data == "language":
        bot.answer_callback_query(call.id)
        show_language_menu_edit(chat_id, message_id)
    elif call.data == "support":
        bot.answer_callback_query(call.id)
        show_support_menu_edit(chat_id, message_id)
    elif call.data.startswith("lang_"):
        lang_code = call.data.replace("lang_", "")
        user_languages[chat_id] = lang_code
        bot.answer_callback_query(call.id, "Language updated!")
        show_main_menu(chat_id, message_id)
    elif call.data == "catalog":
        bot.answer_callback_query(call.id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(t["back"], callback_data="main_menu"))
        bot.edit_message_text("📦 **کاتالوگ محصولات:**\nبه زودی محصولات اینجا قرار می‌گیرند.", chat_id, message_id, reply_markup=markup, parse_mode="Markdown")
    elif call.data == "cart":
        bot.answer_callback_query(call.id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(t["back"], callback_data="main_menu"))
        bot.edit_message_text("🛒 **سبد خرید:**\nسبد خرید شما خالی است.", chat_id, message_id, reply_markup=markup, parse_mode="Markdown")
    elif call.data == "new_ticket":
        bot.answer_callback_query(call.id)
        user_states[chat_id] = "waiting_for_ticket"
        bot.send_message(chat_id, t["ticket_prompt"])
    elif call.data == "my_tickets":
        bot.answer_callback_query(call.id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(t["back"], callback_data="support"))
        bot.edit_message_text("📁 **تیکت‌های من:**\nتیکت فعالی وجود ندارد.", chat_id, message_id, reply_markup=markup, parse_mode="Markdown")
    elif call.data == "privacy_policy":
        bot.answer_callback_query(call.id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(t["back"], callback_data="support"))
        bot.edit_message_text("🔒 **حریم خصوصی:**\nاطلاعات شما محفوظ است.", chat_id, message_id, reply_markup=markup, parse_mode="Markdown")
    elif call.data == "terms_service":
        bot.answer_callback_query(call.id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(t["back"], callback_data="support"))
        bot.edit_message_text("📄 **شرایط خدمات:**\nاستفاده از ربات به منزله پذیرش قوانین است.", chat_id, message_id, reply_markup=markup, parse_mode="Markdown")
    elif call.data.startswith("pay_"):
        bot.answer_callback_query(call.id)
        prices = {"pay_single": 50, "pay_basic": 290, "pay_pro": 690, "pay_ultra": 1990}
        plan_name = call.data.replace("pay_", "").capitalize()
        amount = prices.get(call.data, 50)
        bot.send_invoice(
            chat_id=chat_id,
            title=f"Krelivo {plan_name} Plan",
            description=f"Subscription for {plan_name} package in Krelivo Store (30 Days)",
            invoice_payload=f"krelivo_{plan_name.lower()}",
            provider_token="",
            currency="XTR",
            prices=[types.LabeledPrice(label=f"{plan_name} Plan", amount=amount)]
        )

def show_affiliate_menu_edit(chat_id, message_id):
    lang = user_languages.get(chat_id, "en")
    t = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    invites = user_invites.get(chat_id, 0)
    tier = user_invite_tier.get(chat_id, 1)
    
    # تعیین مرحله بعدی بازی مثل سیستم مراحل کالاف/بازی‌ها
    targets = {1: 100, 2: 200, 3: 500}
    current_target = targets.get(tier, 1000)
    
    # بررسی اینکه آیا کاربر شرط مرحله فعلی رو رد کرده یا نه تا به مرحله بعدی بره
    if invites >= current_target:
        tier += 1
        user_invite_tier[chat_id] = tier
        current_target = targets.get(tier, 1000)

    ref_link = f"https://t.me/Krelivo_bot?start=ref_{chat_id}"
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🎁 دریافت هدیه روزانه (+2 KP)", callback_data="daily_bonus"),
        types.InlineKeyboardButton("🔗 اشتراک‌گذاری لینک دعوت", url=f"https://t.me/share/url?url={ref_link}&text=Join%20Krelivo!"),
        types.InlineKeyboardButton(t["back"], callback_data="main_menu")
    )
    
    text = (
        f"🤝 **سیستم معرفی و سطوح پاداش (مرحله‌ای)** ⭐\n\n"
        f"🎮 **مرحله فعلی شما:** مرحله {tier}\n"
        f"🎯 **هدف این مرحله:** دعوت {current_target} نفر (پیشرفت شما: {invites} نفر)\n"
        f"🎁 **جایزه این مرحله:** ۱ ماه اشتراک رایگان!\n\n"
        f"📌 *ترتیب مراحل:* مرحله ۱ (۱۰۰ نفر) ➔ مرحله ۲ (۲۰۰ نفر) ➔ مرحله ۳ (۵۰۰ نفر) ➔ مراحل بعدی (هر بار ۱۰۰۰ نفر).\n\n"
        f"🔗 **لینک اختصاصی شما:**\n`{ref_link}`"
    )
    bot.edit_message_text(text, chat_id, message_id, reply_markup=markup, parse_mode="Markdown")

def show_language_menu_edit(chat_id, message_id):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
        types.InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
        types.InlineKeyboardButton("🇺🇦 Українська", callback_data="lang_uk"),
        types.InlineKeyboardButton("🇮🇷 فارسی", callback_data="lang_fa"),
        types.InlineKeyboardButton("🇸🇦 العربية", callback_data="lang_ar"),
        types.InlineKeyboardButton("🇨🇳 中文", callback_data="lang_cn"),
        types.InlineKeyboardButton("🇪🇸 Español", callback_data="lang_es"),
        types.InlineKeyboardButton("🇮🇩 Indonesia", callback_data="lang_id"),
        types.InlineKeyboardButton("🇵🇹 Português", callback_data="lang_pt"),
        types.InlineKeyboardButton("🇫🇷 Français", callback_data="lang_fr"),
        types.InlineKeyboardButton("🇹🇷 Türkçe", callback_data="lang_tr"),
        types.InlineKeyboardButton("🇻🇳 Tiếng Việt", callback_data="lang_vi"),
        types.InlineKeyboardButton("🇩🇪 Deutsch", callback_data="lang_de"),
        types.InlineKeyboardButton("🇮🇹 Italiano", callback_data="lang_it"),
        types.InlineKeyboardButton("🔙 Back", callback_data="main_menu")
    )
    bot.edit_message_text("🌐 **Select Language / انتخاب زبان**", chat_id, message_id, reply_markup=markup, parse_mode="Markdown")

def show_support_menu_edit(chat_id, message_id):
    lang = user_languages.get(chat_id, "en")
    t = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(t["new_ticket"], callback_data="new_ticket"),
        types.InlineKeyboardButton(t["my_tickets"], callback_data="my_tickets"),
        types.InlineKeyboardButton(t["privacy"], callback_data="privacy_policy"),
        types.InlineKeyboardButton(t["terms"], callback_data="terms_service"),
        types.InlineKeyboardButton(t["back"], callback_data="main_menu")
    )
    bot.edit_message_text(t["support_text"], chat_id, message_id, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True, content_types=['text', 'photo', 'document', 'video'])
def handle_all_messages(message):
    user_id = message.from_user.id
    
    # تنظیم نام کاربری (Nickname)
    if user_states.get(user_id) == "waiting_for_nickname":
        user_nicknames[user_id] = message.text[:20]  # حداکثر ۲۰ کاراکتر
        user_states[user_id] = None
        bot.send_message(user_id, f"✅ نام کاربری شما با موفقیت به **{message.text}** تغییر کرد!")
        show_profile_page(user_id)
        return

    if message.reply_to_message and message.reply_to_message.forward_from:
        target_user_id = message.reply_to_message.forward_from.id
        try:
            bot.copy_message(chat_id=target_user_id, from_chat_id=message.chat.id, message_id=message.id)
            bot.reply_to(message, "✅ Reply sent to user!")
        except Exception as e:
            bot.reply_to(message, f"❌ Failed to send: {e}")
        return

    if user_states.get(user_id) == "waiting_for_ticket":
        user_states[user_id] = None
        lang = user_languages.get(user_id, "en")
        t = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
        bot.send_message(user_id, t["ticket_success"])
        show_main_menu(user_id)

@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    bot.send_message(message.chat.id, "🎉 Payment successful! Thank you.")

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    t = threading.Thread(target=run_flask)
    t.start()
    bot.infinity_polling()
