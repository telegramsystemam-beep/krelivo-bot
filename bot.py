import os
import json
import telebot
from telebot import types
from flask import Flask
import threading
from datetime import datetime

TOKEN = "9081123644:AAGv3PKfhdXcllBYkvvy11W07fKub6VLKqQ"
bot = telebot.TeleBot(TOKEN)

app = Flask('')

DATA_FILE = "krelivo_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {"languages": {}, "balances": {}, "invites": {}, "invite_tier": {}, "nicknames": {}, "checkins": {}}

def save_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except:
        pass

db = load_data()
user_states = {}
user_referred = set()

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
        "support_text": "🎫 Support Center\n\nChoose an option below:",
        "ticket_prompt": "📝 Please send your message to support:",
        "ticket_success": "✅ Message sent successfully to support!",
        "nickname_prompt": "✏️ Please send your new Nickname:",
        "nickname_success": "✅ Your nickname has been successfully updated!"
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
        "support_text": "🎫 مرکز پشتیبانی\n\nلطفاً یکی از گزینه‌های زیر را انتخاب کنید:",
        "ticket_prompt": "📝 لطفاً پیام خود را برای پشتیبانی بفرستید:",
        "ticket_success": "✅ پیام شما با موفقیت برای پشتیبانی ارسال شد!",
        "nickname_prompt": "✏️ لطفاً نام کاربری (Nickname) جدید خود را بفرستید:",
        "nickname_success": "✅ نام کاربری شما با موفقیت تغییر کرد!"
    },
    "ru": {
        "welcome": "Добро пожаловать в Krelivo Gaming Hub! 🚀",
        "catalog": "📦 Каталог", "cart": "🛒 Корзина", "profile": "👤 Профиль",
        "premium": "⭐ Премиум", "affiliate": "🤝 Рефералы",
        "language": "🌐 Язык", "support": "🎫 Поддержка",
        "leaderboard": "🏆 Лидеры", "daily": "🎁 Бонус",
        "rewards_shop": "🎁 Магазин наград", "back": "🔙 Назад",
        "new_ticket": "🎫 Новый тикет", "my_tickets": "📁 Мои тикеты",
        "privacy": "🔒 Конфиденциальность", "terms": "📄 Условия",
        "support_text": "🎫 Центр поддержки", "ticket_prompt": "📝 Отправьте сообщение:",
        "ticket_success": "✅ Успешно отправлено!",
        "nickname_prompt": "✏️ Введите новое имя:", "nickname_success": "✅ Имя обновлено!"
    },
    "uk": {
        "welcome": "Ласкаво просимо до Krelivo Gaming Hub! 🚀",
        "catalog": "📦 Каталог", "cart": "🛒 Кошик", "profile": "👤 Профіль",
        "premium": "⭐ Преміум", "affiliate": "🤝 Реферали",
        "language": "🌐 Мова", "support": "🎫 Підтримка",
        "leaderboard": "🏆 Лідери", "daily": "🎁 Бонус",
        "rewards_shop": "🎁 Магазин нагород", "back": "🔙 Назад",
        "new_ticket": "🎫 Новий тикет", "my_tickets": "📁 Мої тикети",
        "privacy": "🔒 Конфіденційність", "terms": "📄 Умови",
        "support_text": "🎫 Підтримка", "ticket_prompt": "📝 Надішліть повідомлення:",
        "ticket_success": "✅ Успішно!",
        "nickname_prompt": "✏️ Введіть нік:", "nickname_success": "✅ Оновлено!"
    },
    "ar": {
        "welcome": "أهلاً بك في متجر Krelivo! 🚀",
        "catalog": "📦 الكتالوج", "cart": "🛒 السلة", "profile": "👤 الملف",
        "premium": "⭐ المميزة", "affiliate": "🤝 الإحالة",
        "language": "🌐 اللغة", "support": "🎫 الدعم",
        "leaderboard": "🏆 لوحة الصدارة", "daily": "🎁 الهدية اليومية",
        "rewards_shop": "🎁 متجر المكافآت", "back": "🔙 رجوع",
        "new_ticket": "🎫 تذكرة جديدة", "my_tickets": "📁 تذاكري",
        "privacy": "🔒 الخصوصية", "terms": "📄 الشروط",
        "support_text": "🎫 مركز الدعم", "ticket_prompt": "📝 أرسل رسالتك:",
        "ticket_success": "✅ تم الإرسال!",
        "nickname_prompt": "✏️ أرسل اسمك:", "nickname_success": "✅ تم التحديث!"
    },
    "zh": {
        "welcome": "欢迎来到 Krelivo 游戏中心！🚀",
        "catalog": "📦 目录", "cart": "🛒 购物车", "profile": "👤 个人资料",
        "premium": "⭐ 高级", "affiliate": "🤝 推荐",
        "language": "🌐 语言", "support": "🎫 支持",
        "leaderboard": "🏆 排行榜", "daily": "🎁 每日奖励",
        "rewards_shop": "🎁 奖励商店", "back": "🔙 返回",
        "new_ticket": "🎫 新建工单", "my_tickets": "📁 我的工单",
        "privacy": "🔒 隐私政策", "terms": "📄 服务条款",
        "support_text": "🎫 支持中心", "ticket_prompt": "📝 发送消息：",
        "ticket_success": "✅ 已发送！",
        "nickname_prompt": "✏️ 发送新昵称：", "nickname_success": "✅ 已更新！"
    },
    "es": {
        "welcome": "¡Bienvenido a Krelivo Gaming Hub! 🚀",
        "catalog": "📦 Catálogo", "cart": "🛒 Carrito", "profile": "👤 Perfil",
        "premium": "⭐ Premium", "affiliate": "🤝 Referidos",
        "language": "🌐 Idioma", "support": "🎫 Soporte",
        "leaderboard": "🏆 Líderes", "daily": "🎁 Bono diario",
        "rewards_shop": "🎁 Tienda", "back": "🔙 Volver",
        "new_ticket": "🎫 Nuevo ticket", "my_tickets": "📁 Mis tickets",
        "privacy": "🔒 Privacidad", "terms": "📄 Términos",
        "support_text": "🎫 Soporte", "ticket_prompt": "📝 Envía tu mensaje:",
        "ticket_success": "✅ ¡Enviado!",
        "nickname_prompt": "✏️ Envía tu apodo:", "nickname_success": "✅ ¡Actualizado!"
    },
    "id": {
        "welcome": "Selamat datang di Krelivo Gaming Hub! 🚀",
        "catalog": "📦 Katalog", "cart": "🛒 Keranjang", "profile": "👤 Profil",
        "premium": "⭐ Premium", "affiliate": "🤝 Referensi",
        "language": "🌐 Bahasa", "support": "🎫 Dukungan",
        "leaderboard": "🏆 Peringkat", "daily": "🎁 Bonus Harian",
        "rewards_shop": "🎁 Toko Hadiah", "back": "🔙 Kembali",
        "new_ticket": "🎫 Tiket Baru", "my_tickets": "📁 Tiket Saya",
        "privacy": "🔒 Privasi", "terms": "📄 Ketentuan",
        "support_text": "🎫 Dukungan", "ticket_prompt": "📝 Kirim pesan:",
        "ticket_success": "✅ Terkirim!",
        "nickname_prompt": "✏️ Kirim nama:", "nickname_success": "✅ Berhasil!"
    },
    "pt": {
        "welcome": "Bem-vindo ao Krelivo Gaming Hub! 🚀",
        "catalog": "📦 Catálogo", "cart": "🛒 Carrinho", "profile": "👤 Perfil",
        "premium": "⭐ Premium", "affiliate": "🤝 Indicação",
        "language": "🌐 Idioma", "support": "🎫 Suporte",
        "leaderboard": "🏆 Líderes", "daily": "🎁 Bônus Diário",
        "rewards_shop": "🎁 Loja", "back": "🔙 Voltar",
        "new_ticket": "🎫 Novo ticket", "my_tickets": "📁 Meus tickets",
        "privacy": "🔒 Privacidade", "terms": "📄 Termos",
        "support_text": "🎫 Suporte", "ticket_prompt": "📝 Envie sua mensagem:",
        "ticket_success": "✅ Enviado!",
        "nickname_prompt": "✏️ Envie seu apelido:", "nickname_success": "✅ Atualizado!"
    },
    "fr": {
        "welcome": "Bienvenue sur Krelivo Gaming Hub ! 🚀",
        "catalog": "📦 Catalogue", "cart": "🛒 Panier", "profile": "👤 Profil",
        "premium": "⭐ Premium", "affiliate": "🤝 Parrainage",
        "language": "🌐 Langue", "support": "🎫 Support",
        "leaderboard": "🏆 Classement", "daily": "🎁 Bonus Quotidien",
        "rewards_shop": "🎁 Boutique", "back": "🔙 Retour",
        "new_ticket": "🎫 Nouveau ticket", "my_tickets": "📁 Mes tickets",
        "privacy": "🔒 Confidentialité", "terms": "📄 Conditions",
        "support_text": "🎫 Support", "ticket_prompt": "📝 Envoyez votre message :",
        "ticket_success": "✅ Envoyé !",
        "nickname_prompt": "✏️ Envoyez votre pseudo :", "nickname_success": "✅ Mis à jour !"
    },
    "tr": {
        "welcome": "Krelivo Gaming Hub'a Hoş Geldiniz! 🚀",
        "catalog": "📦 Katalog", "cart": "🛒 Sepet", "profile": "👤 Profil",
        "premium": "⭐ Premium", "affiliate": "🤝 Referans",
        "language": "🌐 Dil", "support": "🎫 Destek",
        "leaderboard": "🏆 Liderler", "daily": "🎁 Günlük Bonus",
        "rewards_shop": "🎁 Ödül Mağazası", "back": "🔙 Geri",
        "new_ticket": "🎫 Yeni Destek", "my_tickets": "📁 Biletlerim",
        "privacy": "🔒 Gizlilik", "terms": "📄 Şartlar",
        "support_text": "🎫 Destek", "ticket_prompt": "📝 Mesajınızı gönderin:",
        "ticket_success": "✅ Gönderildi!",
        "nickname_prompt": "✏️ Takma adınızı gönderin:", "nickname_success": "✅ Güncellendi!"
    },
    "vi": {
        "welcome": "Chào mừng đến với Krelivo Gaming Hub! 🚀",
        "catalog": "📦 Danh mục", "cart": "🛒 Giỏ hàng", "profile": "👤 Hồ sơ",
        "premium": "⭐ Premium", "affiliate": "🤝 Giới thiệu",
        "language": "🌐 Ngôn ngữ", "support": "🎫 Hỗ trợ",
        "leaderboard": "🏆 Bảng xếp hạng", "daily": "🎁 Thưởng ngày",
        "rewards_shop": "🎁 Cửa hàng", "back": "🔙 Quay lại",
        "new_ticket": "🎫 Tạo vé mới", "my_tickets": "📁 Vé của tôi",
        "privacy": "🔒 Bảo mật", "terms": "📄 Điều khoản",
        "support_text": "🎫 Hỗ trợ", "ticket_prompt": "📝 Gửi tin nhắn:",
        "ticket_success": "✅ Đã gửi!",
        "nickname_prompt": "✏️ Gửi tên:", "nickname_success": "✅ Thành công!"
    },
    "de": {
        "welcome": "Willkommen im Krelivo Gaming Hub! 🚀",
        "catalog": "📦 Katalog", "cart": "🛒 Warenkorb", "profile": "👤 Profil",
        "premium": "⭐ Premium", "affiliate": "🤝 Empfehlung",
        "language": "🌐 Sprache", "support": "🎫 Support",
        "leaderboard": "🏆 Bestenliste", "daily": "🎁 Täglicher Bonus",
        "rewards_shop": "🎁 Prämien-Shop", "back": "🔙 Zurück",
        "new_ticket": "🎫 Neues Ticket", "my_tickets": "📁 Meine Tickets",
        "privacy": "🔒 Datenschutz", "terms": "📄 AGB",
        "support_text": "🎫 Support", "ticket_prompt": "📝 Nachricht senden:",
        "ticket_success": "✅ Gesendet!",
        "nickname_prompt": "✏️ Nickname senden:", "nickname_success": "✅ Aktualisiert!"
    },
    "it": {
        "welcome": "Benvenuto su Krelivo Gaming Hub! 🚀",
        "catalog": "📦 Catalogo", "cart": "🛒 Carrello", "profile": "👤 Profilo",
        "premium": "⭐ Premium", "affiliate": "🤝 Affiliazione",
        "language": "🌐 Lingua", "support": "🎫 Supporto",
        "leaderboard": "🏆 Classifica", "daily": "🎁 Bonus Giornaliero",
        "rewards_shop": "🎁 Negozio", "back": "🔙 Indietro",
        "new_ticket": "🎫 Nuovo ticket", "my_tickets": "📁 I miei ticket",
        "privacy": "🔒 Privacy", "terms": "📄 Termini",
        "support_text": "🎫 Supporto", "ticket_prompt": "📝 Invia messaggio:",
        "ticket_success": "✅ Inviato!",
        "nickname_prompt": "✏️ Invia nickname:", "nickname_success": "✅ Aggiornato!"
    }
}

@app.route('/')
def home():
    return "Bot is alive and running!"

def get_lang(chat_id):
    return db["languages"].get(str(chat_id), "en")

def safe_edit(chat_id, message_id, text, reply_markup=None):
    try:
        bot.edit_message_text(text, chat_id, message_id, reply_markup=reply_markup)
    except Exception as e:
        if "message is not modified" in str(e):
            pass
        else:
            try:
                bot.send_message(chat_id, text, reply_markup=reply_markup)
            except:
                pass

def show_main_menu(chat_id, message_id=None, is_new=False):
    lang = get_lang(chat_id)
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
        safe_edit(chat_id, message_id, t["welcome"], reply_markup=markup)

@bot.message_handler(commands=['start'])
def cmd_start(message):
    user_id = str(message.from_user.id)
    args = message.text.split()
    if len(args) > 1 and args[1].startswith("ref_"):
        try:
            inviter_id = args[1].replace("ref_", "")
            if inviter_id != user_id and user_id not in user_referred:
                user_referred.add(user_id)
                db["invites"][inviter_id] = db["invites"].get(inviter_id, 0) + 1
                db["balances"][inviter_id] = db["balances"].get(inviter_id, 0) + 10
                save_data(db)
                try:
                    bot.send_message(int(inviter_id), "✨ New referral joined! +10 KP added.")
                except:
                    pass
        except:
            pass
    show_main_menu(message.chat.id, None, is_new=True)

@bot.message_handler(commands=['profile'])
def cmd_profile(message):
    show_profile_page(message.chat.id)

def show_profile_page(chat_id, message_id=None):
    c_id = str(chat_id)
    balance = db["balances"].get(c_id, 0)
    invites = db["invites"].get(c_id, 0)
    tier = db["invite_tier"].get(c_id, 1)
    nickname = db["nicknames"].get(c_id, f"User_{chat_id}")
    
    targets = {1: 100, 2: 200, 3: 500}
    current_target = targets.get(tier, 1000)
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("✏️ Change Nickname", callback_data="set_nickname"),
        types.InlineKeyboardButton("🔙 Back", callback_data="main_menu")
    )
    
    text = (
        f"👤 **Profile:**\n"
        f"• Name: {nickname}\n"
        f"• ID: `{chat_id}`\n"
        f"• Balance: {balance} KP\n"
        f"• Tier: {tier} (Progress: {invites} / {current_target})"
    )
    
    if message_id:
        safe_edit(chat_id, message_id, text, reply_markup=markup)
    else:
        bot.send_message(chat_id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    c_id = str(chat_id)
    message_id = call.message.message_id
    lang = get_lang(chat_id)
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
        bot.send_message(chat_id, t["nickname_prompt"])
    elif call.data == "rewards_shop":
        bot.answer_callback_query(call.id)
        balance = db["balances"].get(c_id, 0)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("⭐ Buy 1 Month Sub (600 KP)", callback_data="buy_sub_kp"),
            types.InlineKeyboardButton(t["back"], callback_data="main_menu")
        )
        text = f"🎁 **KP Rewards Shop**\n\nBalance: {balance} KP\nExchange 600 KP for 1 Month Sub!"
        safe_edit(chat_id, message_id, text, reply_markup=markup)
    elif call.data == "buy_sub_kp":
        balance = db["balances"].get(c_id, 0)
        if balance >= 600:
            db["balances"][c_id] = balance - 600
            save_data(db)
            bot.answer_callback_query(call.id, "🎉 Success! Subscription activated.", show_alert=True)
        else:
            bot.answer_callback_query(call.id, f"❌ Not enough KP! Need {600 - balance} more.", show_alert=True)
    elif call.data == "affiliate":
        bot.answer_callback_query(call.id)
        show_affiliate_menu_edit(chat_id, message_id)
    elif call.data == "daily_bonus":
        today = datetime.now().strftime("%Y-%m-%d")
        if db["checkins"].get(c_id) == today:
            bot.answer_callback_query(call.id, "❌ Already claimed today!", show_alert=True)
        else:
            db["checkins"][c_id] = today
            db["balances"][c_id] = db["balances"].get(c_id, 0) + 2
            save_data(db)
            bot.answer_callback_query(call.id, "🎉 +2 KP added!", show_alert=True)
        show_affiliate_menu_edit(chat_id, message_id)
    elif call.data == "leaderboard":
        bot.answer_callback_query(call.id)
        sorted_users = sorted(db["balances"].items(), key=lambda x: x[1], reverse=True)[:10]
        lb_text = "🏆 **Leaderboard (Top KP)**\n\n"
        if sorted_users:
            for idx, (uid, bal) in enumerate(sorted_users, 1):
                name = db["nicknames"].get(uid, f"User_{uid}")
                lb_text += f"{idx}. {name} — {bal} KP\n"
        else:
            lb_text += "No records yet."
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(t["back"], callback_data="main_menu"))
        safe_edit(chat_id, message_id, lb_text, reply_markup=markup)
    elif call.data == "premium":
        bot.answer_callback_query(call.id)
        show_premium_menu_edit(chat_id, message_id)
    elif call.data == "language":
        bot.answer_callback_query(call.id)
        show_language_menu_edit(chat_id, message_id)
    elif call.data == "support":
        bot.answer_callback_query(call.id)
        show_support_menu_edit(chat_id, message_id)
    elif call.data.startswith("lang_"):
        lang_code = call.data.replace("lang_", "")
        db["languages"][c_id] = lang_code
        save_data(db)
        bot.answer_callback_query(call.id, "Language updated!")
        show_main_menu(chat_id, message_id)
    elif call.data == "catalog":
        bot.answer_callback_query(call.id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(t["back"], callback_data="main_menu"))
        safe_edit(chat_id, message_id, "📦 **Catalog:**\nComing soon.", reply_markup=markup)
    elif call.data == "cart":
        bot.answer_callback_query(call.id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(t["back"], callback_data="main_menu"))
        safe_edit(chat_id, message_id, "🛒 **Shopping Cart:**\nYour cart is empty.", reply_markup=markup)
    elif call.data == "new_ticket":
        bot.answer_callback_query(call.id)
        user_states[chat_id] = "waiting_for_ticket"
        bot.send_message(chat_id, t["ticket_prompt"])
    elif call.data == "my_tickets":
        bot.answer_callback_query(call.id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(t["back"], callback_data="support"))
        safe_edit(chat_id, message_id, "📁 **My Tickets:**\nNo active tickets.", reply_markup=markup)
    elif call.data == "privacy_policy":
        bot.answer_callback_query(call.id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(t["back"], callback_data="support"))
        safe_edit(chat_id, message_id, "🔒 **Privacy Policy:**\nSecure data.", reply_markup=markup)
    elif call.data == "terms_service":
        bot.answer_callback_query(call.id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(t["back"], callback_data="support"))
        safe_edit(chat_id, message_id, "📄 **Terms of Service:**\nAll sales final.", reply_markup=markup)
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
    lang = get_lang(chat_id)
    t = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("⭐ Single – 50 ⭐️", callback_data="pay_single"),
        types.InlineKeyboardButton("⭐ Basic – 290 ⭐️", callback_data="pay_basic"),
        types.InlineKeyboardButton("⭐ Pro – 690 ⭐️", callback_data="pay_pro"),
        types.InlineKeyboardButton("⭐ Ultra – 1990 ⭐️", callback_data="pay_ultra"),
        types.InlineKeyboardButton(t["back"], callback_data="main_menu")
    )
    safe_edit(chat_id, message_id, "⭐ **Premium Plans (30 Days)**\nChoose your subscription plan:", reply_markup=markup)

def show_affiliate_menu_edit(chat_id, message_id):
    c_id = str(chat_id)
    lang = get_lang(chat_id)
    t = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    invites = db["invites"].get(c_id, 0)
    tier = db["invite_tier"].get(c_id, 1)
    
    targets = {1: 100, 2: 200, 3: 500}
    current_target = targets.get(tier, 1000)
    
    if invites >= current_target:
        tier += 1
        db["invite_tier"][c_id] = tier
        save_data(db)
        current_target = targets.get(tier, 1000)

    ref_link = f"https://t.me/Krelivo_bot?start=ref_{chat_id}"
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🎁 Claim Daily (+2 KP)", callback_data="daily_bonus"),
        types.InlineKeyboardButton("🔗 Share Invite Link", url=f"https://t.me/share/url?url={ref_link}&text=Join%20Krelivo!"),
        types.InlineKeyboardButton(t["back"], callback_data="main_menu")
    )
    
    text = (
        f"🤝 **Referral & Tiers System**\n\n"
        f"🎮 Current Tier: {tier}\n"
        f"🎯 Target: {current_target} invites (Progress: {invites})\n"
        f"🎁 Reward: 1 Month Free Subscription!\n\n"
        f"🔗 Invite Link:\n{ref_link}"
    )
    safe_edit(chat_id, message_id, text, reply_markup=markup)

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
    safe_edit(chat_id, message_id, "🌐 **Select Language / انتخاب زبان**", reply_markup=markup)

def show_support_menu_edit(chat_id, message_id):
    lang = get_lang(chat_id)
    t = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(t["new_ticket"], callback_data="new_ticket"),
        types.InlineKeyboardButton(t["my_tickets"], callback_data="my_tickets"),
        types.InlineKeyboardButton(t["privacy"], callback_data="privacy_policy"),
        types.InlineKeyboardButton(t["terms"], callback_data="terms_service"),
        types.InlineKeyboardButton(t["back"], callback_data="main_menu")
    )
    safe_edit(chat_id, message_id, t["support_text"], reply_markup=markup)

@bot.message_handler(func=lambda message: True, content_types=['text', 'photo', 'document', 'video'])
def handle_all_messages(message):
    user_id = message.from_user.id
    c_id = str(user_id)
    lang = get_lang(user_id)
    t = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    
    if user_states.get(user_id) == "waiting_for_nickname":
        db["nicknames"][c_id] = message.text[:20]
        save_data(db)
        user_states[user_id] = None
        bot.send_message(user_id, t["nickname_success"])
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
