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
user_invites = {}
user_referred = set()
user_balances = {}       # ذخیره سکه های KP کاربران
user_last_checkin = {}   # ذخیره تاریخ آخرین ورود روزانه

TRANSLATIONS = {
    "en": {
        "welcome": "Welcome to Krelivo Store! 🚀\n\nExplore our exclusive digital products and services below.",
        "catalog": "📦 Catalog", "cart": "🛒 Cart", "profile": "👤 Profile",
        "premium": "⭐ Premium", "affiliate": "🤝 Referral",
        "language": "🌐 Language", "support": "🎫 Support",
        "leaderboard": "🏆 Leaderboard", "daily": "🎁 Daily Bonus",
        "back": "🔙 Back", "new_ticket": "🎫 New Ticket", "my_tickets": "📁 My Tickets",
        "privacy": "🔒 Privacy Policy", "terms": "📄 Terms of Service",
        "support_text": "🎫 **Support Center**\n\nChoose an option below:",
        "ticket_prompt": "📝 Please send your message or issue for the support team:",
        "ticket_success": "✅ Your message has been sent to support!"
    },
    "fa": {
        "welcome": "به فروشگاه کرلیوو خوش آمدید! 🚀\n\nمحصولات و خدمات انحصاری ما را در زیر بررسی کنید.",
        "catalog": "📦 کاتالوگ", "cart": "🛒 سبد خرید", "profile": "👤 پروفایل",
        "premium": "⭐ پریمیوم", "affiliate": "🤝 سیستم معرفی",
        "language": "🌐 زبان", "support": "🎫 پشتیبانی",
        "leaderboard": "🏆 لیدربورد", "daily": "🎁 هدیه روزانه",
        "back": "🔙 بازگشت", "new_ticket": "🎫 تیکت جدید", "my_tickets": "📁 تیکت‌های من",
        "privacy": "🔒 حریم خصوصی", "terms": "📄 شرایط خدمات",
        "support_text": "🎫 **مرکز پشتیبانی**\n\nلطفاً یکی از گزینه‌های زیر را انتخاب کنید:",
        "ticket_prompt": "📝 لطفاً پیام یا مشکل خود را برای پشتیبانی ارسال کنید:",
        "ticket_success": "✅ پیام شما برای پشتیبانی ارسال شد!"
    },
    "ru": {
        "welcome": "Добро пожаловать в Krelivo Store! 🚀\n\nИзучите наши продукты ниже.",
        "catalog": "📦 Каталог", "cart": "🛒 Корзина", "profile": "👤 Профиль",
        "premium": "⭐ Премиум", "affiliate": "🤝 Рефералы",
        "language": "🌐 Язык", "support": "🎫 Поддержка",
        "leaderboard": "🏆 Лидеры", "daily": "🎁 Бонус",
        "back": "🔙 Назад", "new_ticket": "🎫 Новый тикет", "my_tickets": "📁 Мои тикеты",
        "privacy": "🔒 Конфиденциальность", "terms": "📄 Условия",
        "support_text": "🎫 **Центр поддержки**\n\nВыберите вариант:",
        "ticket_prompt": "📝 Отправьте сообщение в поддержку:",
        "ticket_success": "✅ Сообщение отправлено!"
    },
    "uk": {
        "welcome": "Ласкаво просимо до Krelivo Store! 🚀\n\nДосліджуйте наші продукти нижче.",
        "catalog": "📦 Каталог", "cart": "🛒 Кошик", "profile": "👤 Профіль",
        "premium": "⭐ Преміум", "affiliate": "🤝 Реферали",
        "language": "🌐 Мова", "support": "🎫 Підтримка",
        "leaderboard": "🏆 Лідери", "daily": "🎁 Бонус",
        "back": "🔙 Назад", "new_ticket": "🎫 Новий тикет", "my_tickets": "📁 Мої тикети",
        "privacy": "🔒 Конфіденційність", "terms": "📄 Умови",
        "support_text": "🎫 **Центр підтримки**\n\nВиберіть варіант:",
        "ticket_prompt": "📝 Надішліть повідомлення до підтримки:",
        "ticket_success": "✅ Повідомлення надіслано!"
    },
    "ar": {
        "welcome": "أهلاً بك في متجر Krelivo! 🚀\n\nاستكشف منتجاتنا أدناه.",
        "catalog": "📦 الكتالوج", "cart": "🛒 السلة", "profile": "👤 الملف",
        "premium": "⭐ المميزة", "affiliate": "🤝 نظام الإحالة",
        "language": "🌐 اللغة", "support": "🎫 الدعم",
        "leaderboard": "🏆 لوحة الصدارة", "daily": "🎁 الهدية اليومية",
        "back": "🔙 رجوع", "new_ticket": "🎫 تذكرة جديدة", "my_tickets": "📁 تذاكري",
        "privacy": "🔒 الخصوصية", "terms": "📄 الشروط",
        "support_text": "🎫 **مركز الدعم**\n\nاختر خياراً:",
        "ticket_prompt": "📝 أرسل رسالتك للدعم:",
        "ticket_success": "✅ تم إرسال رسالتك!"
    },
    "zh": {
        "welcome": "欢迎来到 Krelivo 商店！🚀\n\n在下方探索产品。",
        "catalog": "📦 目录", "cart": "🛒 购物车", "profile": "👤 个人资料",
        "premium": "⭐ 高级", "affiliate": "🤝 推荐系统",
        "language": "🌐 语言", "support": "🎫 支持",
        "leaderboard": "🏆 排行榜", "daily": "🎁 每日奖励",
        "back": "🔙 返回", "new_ticket": "🎫 新建工单", "my_tickets": "📁 我的工单",
        "privacy": "🔒 隐私政策", "terms": "📄 服务条款",
        "support_text": "🎫 **支持中心**\n\n请选择：",
        "ticket_prompt": "📝 发送消息给支持：",
        "ticket_success": "✅ 消息已发送！"
    },
    "es": {
        "welcome": "¡Bienvenido a Krelivo Store! 🚀\n\nExplora nuestros productos.",
        "catalog": "📦 Catálogo", "cart": "🛒 Carrito", "profile": "👤 Perfil",
        "premium": "⭐ Premium", "affiliate": "🤝 Referidos",
        "language": "🌐 Idioma", "support": "🎫 Soporte",
        "leaderboard": "🏆 Líderes", "daily": "🎁 Bono diario",
        "back": "🔙 Volver", "new_ticket": "🎫 Nuevo ticket", "my_tickets": "📁 Mis tickets",
        "privacy": "🔒 Privacidad", "terms": "📄 Términos",
        "support_text": "🎫 **Soporte**\n\nElige una opción:",
        "ticket_prompt": "📝 Envía tu mensaje:",
        "ticket_success": "✅ ¡Enviado!"
    },
    "id": {
        "welcome": "Selamat datang di Krelivo Store! 🚀",
        "catalog": "📦 Katalog", "cart": "🛒 Keranjang", "profile": "👤 Profil",
        "premium": "⭐ Premium", "affiliate": "🤝 Referensi",
        "language": "🌐 Bahasa", "support": "🎫 Dukungan",
        "leaderboard": "🏆 Pعperingkat", "daily": "🎁 Bonus Harian",
        "back": "🔙 Kembali", "new_ticket": "🎫 Tiket Baru", "my_tickets": "📁 Tiket Saya",
        "privacy": "🔒 Privasi", "terms": "📄 Ketentuan",
        "support_text": "🎫 **Dukungan**\n\nPilih opsi:",
        "ticket_prompt": "📝 Kirim pesan:",
        "ticket_success": "✅ Terkirim!"
    },
    "pt": {
        "welcome": "Bem-vindo à Krelivo Store! 🚀",
        "catalog": "📦 Catálogo", "cart": "🛒 Carrinho", "profile": "👤 Perfil",
        "premium": "⭐ Premium", "affiliate": "🤝 Indicação",
        "language": "🌐 Idioma", "support": "🎫 Suporte",
        "leaderboard": "🏆 Líderes", "daily": "🎁 Bônus Diário",
        "back": "🔙 Voltar", "new_ticket": "🎫 Novo ticket", "my_tickets": "📁 Meus tickets",
        "privacy": "🔒 Privacidade", "terms": "📄 Termos",
        "support_text": "🎫 **Suporte**\n\nEscolha:",
        "ticket_prompt": "📝 Envie sua mensagem:",
        "ticket_success": "✅ Enviado!"
    },
    "fr": {
        "welcome": "Bienvenue sur Krelivo Store ! 🚀",
        "catalog": "📦 Catalogue", "cart": "🛒 Panier", "profile": "👤 Profil",
        "premium": "⭐ Premium", "affiliate": "🤝 Parrainage",
        "language": "🌐 Langue", "support": "🎫 Support",
        "leaderboard": "🏆 Classement", "daily": "🎁 Bonus Quotidien",
        "back": "🔙 Retour", "new_ticket": "🎫 Nouveau ticket", "my_tickets": "📁 Mes tickets",
        "privacy": "🔒 Confidentialité", "terms": "📄 Conditions",
        "support_text": "🎫 **Support**\n\nChoisissez :",
        "ticket_prompt": "📝 Envoyez votre message :",
        "ticket_success": "✅ Envoyé !"
    },
    "tr": {
        "welcome": "Krelivo Mağazasına Hoş Geldiniz! 🚀",
        "catalog": "📦 Katalog", "cart": "🛒 Sepet", "profile": "👤 Profil",
        "premium": "⭐ Premium", "affiliate": "🤝 Referans",
        "language": "🌐 Dil", "support": "🎫 Destek",
        "leaderboard": "🏆 Liderler", "daily": "🎁 Günlük Bonus",
        "back": "🔙 Geri", "new_ticket": "🎫 Yeni Destek", "my_tickets": "📁 Biletlerim",
        "privacy": "🔒 Gizlilik", "terms": "📄 Şartlar",
        "support_text": "🎫 **Destek**\n\nSeçenek seçin:",
        "ticket_prompt": "📝 Mesajınızı gönderin:",
        "ticket_success": "✅ Gönderildi!"
    },
    "vi": {
        "welcome": "Chào mừng đến với Krelivo Store! 🚀",
        "catalog": "📦 Danh mục", "cart": "🛒 Giỏ hàng", "profile": "👤 Hồ sơ",
        "premium": "⭐ Premium", "affiliate": "🤝 Giới thiệu",
        "language": "🌐 Ngôn ngữ", "support": "🎫 Hỗ trợ",
        "leaderboard": "🏆 Bảng xếp hạng", "daily": "🎁 Thưởng ngày",
        "back": "🔙 Quay lại", "new_ticket": "🎫 Tạo vé mới", "my_tickets": "📁 Vé của tôi",
        "privacy": "🔒 Bảo mật", "terms": "📄 Điều khoản",
        "support_text": "🎫 **Hỗ trợ**\n\nChọn:",
        "ticket_prompt": "📝 Gửi tin nhắn:",
        "ticket_success": "✅ Đã gửi!"
    },
    "de": {
        "welcome": "Willkommen im Krelivo Store! 🚀",
        "catalog": "📦 Katalog", "cart": "🛒 Warenkorb", "profile": "👤 Profil",
        "premium": "⭐ Premium", "affiliate": "🤝 Empfehlung",
        "language": "🌐 Sprache", "support": "🎫 Support",
        "leaderboard": "🏆 Bestenliste", "daily": "🎁 Täglicher Bonus",
        "back": "🔙 Zurück", "new_ticket": "🎫 Neues Ticket", "my_tickets": "📁 Meine Tickets",
        "privacy": "🔒 Datenschutz", "terms": "📄 AGB",
        "support_text": "🎫 **Support**\n\nWählen:",
        "ticket_prompt": "📝 Nachricht senden:",
        "ticket_success": "✅ Gesendet!"
    },
    "it": {
        "welcome": "Benvenuto su Krelivo Store! 🚀",
        "catalog": "📦 Catalogo", "cart": "🛒 Carrello", "profile": "👤 Profilo",
        "premium": "⭐ Premium", "affiliate": "🤝 Affiliazione",
        "language": "🌐 Lingua", "support": "🎫 Supporto",
        "leaderboard": "🏆 Classifica", "daily": "🎁 Bonus Giornaliero",
        "back": "🔙 Indietro", "new_ticket": "🎫 Nuovo ticket", "my_tickets": "📁 I miei ticket",
        "privacy": "🔒 Privacy", "terms": "📄 Termini",
        "support_text": "🎫 **Supporto**\n\nScegli:",
        "ticket_prompt": "📝 Invia messaggio:",
        "ticket_success": "✅ Inviato!"
    }
}

@app.route('/')
def home():
    return "Bot is alive and running!"

def show_main_menu(chat_id, message_id=None, is_new=False):
    lang = user_languages.get(chat_id, "en")
    t = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(t["catalog"], callback_data="catalog"),
        types.InlineKeyboardButton(t["cart"], callback_data="cart"),
        types.InlineKeyboardButton(t["profile"], callback_data="profile"),
        types.InlineKeyboardButton(t["premium"], callback_data="premium"),
        types.InlineKeyboardButton(t["affiliate"], callback_data="affiliate"),
        types.InlineKeyboardButton(t["daily"], callback_data="daily_bonus"),
        types.InlineKeyboardButton(t["leaderboard"], callback_data="leaderboard"),
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
                # پاداش دعوت: هر نفر ۱۰ سکه KP به معرف اضافه می‌کند
                user_balances[inviter_id] = user_balances.get(inviter_id, 0) + 10
                try:
                    bot.send_message(inviter_id, "✨ Someone joined via your referral link! +10 KP added.")
                except:
                    pass
        except:
            pass
    show_main_menu(message.chat.id, None, is_new=True)

@bot.message_handler(commands=['products'])
def cmd_products(message):
    lang = user_languages.get(message.chat.id, "en")
    t = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(t["back"], callback_data="main_menu"))
    bot.send_message(message.chat.id, "📦 **Catalog:**\nExclusive digital products will appear here soon.", reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(commands=['cart'])
def cmd_cart(message):
    lang = user_languages.get(message.chat.id, "en")
    t = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(t["back"], callback_data="main_menu"))
    bot.send_message(message.chat.id, "🛒 **Shopping Cart:**\nYour cart is currently empty.", reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(commands=['profile'])
def cmd_profile(message):
    chat_id = message.chat.id
    lang = user_languages.get(chat_id, "en")
    t = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    balance = user_balances.get(chat_id, 0)
    invites = user_invites.get(chat_id, 0)
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(t["back"], callback_data="main_menu"))
    text = (
        f"👤 **Profile:**\n"
        f"• ID: `{chat_id}`\n"
        f"• Balance: **{balance} KP** (Krelivo Points)\n"
        f"• Invited Friends: **{invites} / 100**\n"
        f"• Status: Active"
    )
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(commands=['premium'])
def cmd_premium(message):
    lang = user_languages.get(message.chat.id, "en")
    t = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("⭐ Single – 50 ⭐️", callback_data="pay_single"),
        types.InlineKeyboardButton("⭐ Basic – 290 ⭐️", callback_data="pay_basic"),
        types.InlineKeyboardButton("⭐ Pro – 690 ⭐️", callback_data="pay_pro"),
        types.InlineKeyboardButton("⭐ Ultra – 1990 ⭐️", callback_data="pay_ultra"),
        types.InlineKeyboardButton(t["back"], callback_data="main_menu")
    )
    bot.send_message(message.chat.id, "⭐ **Premium Plans (30 Days)**\nChoose your subscription plan:", reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(commands=['language'])
def cmd_language(message):
    show_language_menu_msg(message.chat.id)

@bot.message_handler(commands=['support'])
def cmd_support(message):
    show_support_menu_msg(message.chat.id)

@bot.message_handler(commands=['help'])
def cmd_help(message):
    bot.send_message(message.chat.id, "ℹ️ **Help & Guide:**\nUse the buttons below to navigate or earn KP coins.", parse_mode="Markdown")

def show_language_menu_msg(chat_id):
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
    bot.send_message(chat_id, "🌐 **Select Language / انتخاب زبان / Выберите язык**", reply_markup=markup, parse_mode="Markdown")

def show_support_menu_msg(chat_id):
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
    bot.send_message(chat_id, t["support_text"], reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    lang = user_languages.get(chat_id, "en")
    t = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    
    if call.data == "main_menu":
        bot.answer_callback_query(call.id)
        show_main_menu(chat_id, message_id)
    elif call.data == "premium":
        bot.answer_callback_query(call.id)
        show_premium_menu_edit(chat_id, message_id)
    elif call.data == "affiliate":
        bot.answer_callback_query(call.id)
        show_affiliate_menu_edit(chat_id, message_id)
    elif call.data == "daily_bonus":
        today = datetime.now().strftime("%Y-%m-%d")
        last_checkin = user_last_checkin.get(chat_id)
        if last_checkin == today:
            bot.answer_callback_query(call.id, "❌ You already claimed your daily 2 KP today!", show_alert=True)
        else:
            user_last_checkin[chat_id] = today
            user_balances[chat_id] = user_balances.get(chat_id, 0) + 2
            bot.answer_callback_query(call.id, "🎉 Success! +2 KP added to your balance.", show_alert=True)
        show_affiliate_menu_edit(chat_id, message_id)
    elif call.data == "leaderboard":
        bot.answer_callback_query(call.id)
        # ساخت لیدربورد بر اساس بیشترین سکه KP
        sorted_users = sorted(user_balances.items(), key=lambda x: x[1], reverse=True)[:10]
        lb_text = "🏆 **Krelivo Leaderboard (Top KP Earners)**\n\n"
        if sorted_users:
            for idx, (uid, bal) in enumerate(sorted_users, 1):
                lb_text += f"{idx}. User `{uid}` — **{bal} KP**\n"
        else:
            lb_text += "No records yet. Be the first to earn KP!"
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
        bot.edit_message_text("📦 **Catalog:**\nExclusive digital products will appear here soon.", chat_id, message_id, reply_markup=markup, parse_mode="Markdown")
    elif call.data == "cart":
        bot.answer_callback_query(call.id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(t["back"], callback_data="main_menu"))
        bot.edit_message_text("🛒 **Shopping Cart:**\nYour cart is currently empty.", chat_id, message_id, reply_markup=markup, parse_mode="Markdown")
    elif call.data == "profile":
        bot.answer_callback_query(call.id)
        balance = user_balances.get(chat_id, 0)
        invites = user_invites.get(chat_id, 0)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(t["back"], callback_data="main_menu"))
        text = f"👤 **Profile:**\n• ID: `{chat_id}`\n• Balance: **{balance} KP**\n• Invited: **{invites} / 100**\n• Status: Active"
        bot.edit_message_text(text, chat_id, message_id, reply_markup=markup, parse_mode="Markdown")
    elif call.data == "new_ticket":
        bot.answer_callback_query(call.id)
        user_states[chat_id] = "waiting_for_ticket"
        bot.send_message(chat_id, t["ticket_prompt"])
    elif call.data == "my_tickets":
        bot.answer_callback_query(call.id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(t["back"], callback_data="support"))
        bot.edit_message_text("📁 **My Tickets:**\nNo active tickets found.", chat_id, message_id, reply_markup=markup, parse_mode="Markdown")
    elif call.data == "privacy_policy":
        bot.answer_callback_query(call.id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(t["back"], callback_data="support"))
        bot.edit_message_text("🔒 **Privacy Policy:**\nYour data is secure and encrypted with us.", chat_id, message_id, reply_markup=markup, parse_mode="Markdown")
    elif call.data == "terms_service":
        bot.answer_callback_query(call.id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(t["back"], callback_data="support"))
        bot.edit_message_text("📄 **Terms of Service:**\nAll sales are final. Use services responsibly.", chat_id, message_id, reply_markup=markup, parse_mode="Markdown")
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

def show_premium_menu_edit(chat_id, message_id):
    lang = user_languages.get(chat_id, "en")
    t = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("⭐ Single – 50 ⭐️", callback_data="pay_single"),
        types.InlineKeyboardButton("⭐ Basic – 290 ⭐️", callback_data="pay_basic"),
        types.InlineKeyboardButton("⭐ Pro – 690 ⭐️", callback_data="pay_pro"),
        types.InlineKeyboardButton("⭐ Ultra – 1990 ⭐️", callback_data="pay_ultra"),
        types.InlineKeyboardButton(t["back"], callback_data="main_menu")
    )
    bot.edit_message_text("⭐ **Premium Plans (30 Days)**\nChoose your subscription plan:", chat_id, message_id, reply_markup=markup, parse_mode="Markdown")

def show_affiliate_menu_edit(chat_id, message_id):
    lang = user_languages.get(chat_id, "en")
    t = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    invites = user_invites.get(chat_id, 0)
    balance = user_balances.get(chat_id, 0)
    ref_link = f"https://t.me/Krelivo_bot?start=ref_{chat_id}"
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🎁 Claim Daily (+2 KP)", callback_data="daily_bonus"),
        types.InlineKeyboardButton("🔗 Share Invite Link", url=f"https://t.me/share/url?url={ref_link}&text=Join%20Krelivo%20Store!"),
        types.InlineKeyboardButton(t["back"], callback_data="main_menu")
    )
    text = (
        f"🤝 **Referral & Rewards System (KP)** ⭐\n\n"
        f"🎁 **Daily Check-in:** Get +2 KP every day! (300 days = 1 Month Free)\n"
        f"👥 **Referral Bonus:** Invite 100 friends = 1 Month Free\n\n"
        f"🔗 **Your Invite Link:**\n`{ref_link}`\n\n"
        f"📊 **Your Stats:**\n"
        f"• Balance: **{balance} KP**\n"
        f"• Invited: **{invites} / 100**"
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
    bot.edit_message_text("🌐 **Select Language / انتخاب زبان / Выберите язык**", chat_id, message_id, reply_markup=markup, parse_mode="Markdown")

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
    bot.send_message(message.chat.id, "🎉 Payment successful! Thank you for your purchase.")

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    t = threading.Thread(target=run_flask)
    t.start()
    bot.infinity_polling()
