import os
import telebot
from telebot import types
from flask import Flask
import threading

TOKEN = "9081123644:AAGv3PKfhdXcllBYkvvy11W07fKub6VLKqQ"
ADMIN_ID = 530000000  # در صورت نیاز آیدی عددی تلگرام خودت را اینجا بگذار تا تیکت‌ها برایت بیاید

bot = telebot.TeleBot(TOKEN)
app = Flask('')

user_languages = {}
user_states = {}
user_invites = {}
user_referred = set()
user_tickets = {}

TRANSLATIONS = {
    "en": {
        "welcome": "Welcome to Krelivo Store! 🚀\n\nExplore our exclusive digital products and services below.",
        "catalog": "📦 Catalog", "cart": "🛒 Cart", "profile": "👤 Profile",
        "premium": "⭐ Premium", "affiliate": "🤝 Referral",
        "language": "🌐 Language", "support": "🎫 Support",
        "back": "🔙 Back", "new_ticket": "🎫 New Ticket", "my_tickets": "📁 My Tickets",
        "privacy": "🔒 Privacy Policy", "terms": "📄 Terms of Service",
        "support_text": "🎫 **Support Center**\n\nIf you have any questions or issues, please choose an option below:",
        "ticket_prompt": "📝 Please send your message or issue for the support team:",
        "ticket_success": "✅ Your ticket has been submitted to the admin successfully!"
    },
    "fa": {
        "welcome": "به فروشگاه کرلیوو خوش آمدید! 🚀\n\nمحصولات و خدمات انحصاری ما را در زیر بررسی کنید.",
        "catalog": "📦 کاتالوگ", "cart": "🛒 سبد خرید", "profile": "👤 پروفایل",
        "premium": "⭐ پریمیوم", "affiliate": "🤝 سیستم معرفی",
        "language": "🌐 زبان", "support": "🎫 پشتیبانی",
        "back": "🔙 بازگشت", "new_ticket": "🎫 تیکت جدید", "my_tickets": "📁 تیکت‌های من",
        "privacy": "🔒 حریم خصوصی", "terms": "📄 شرایط خدمات",
        "support_text": "🎫 **مرکز پشتیبانی**\n\nاگر سؤال یا مشکلی داری، لطفاً یکی از گزینه‌های زیر را انتخاب کن:",
        "ticket_prompt": "📝 لطفاً پیام یا مشکل خود را برای تیم پشتیبانی ارسال کنید:",
        "ticket_success": "✅ تیکت شما با موفقیت برای مدیریت ارسال شد!"
    },
    "ru": {
        "welcome": "Добро пожаловать в Krelivo Store! 🚀\n\nИзучите наши эксклюзивные цифровые продукты ниже.",
        "catalog": "📦 Каталог", "cart": "🛒 Корзина", "profile": "👤 Профиль",
        "premium": "⭐ Премиум", "affiliate": "🤝 Рефералы",
        "language": "🌐 Язык", "support": "🎫 Поддержка",
        "back": "🔙 Назад", "new_ticket": "🎫 Новый тикет", "my_tickets": "📁 Мои тикеты",
        "privacy": "🔒 Конфиденциальность", "terms": "📄 Условия",
        "support_text": "🎫 **Центр поддержки**\n\nВыберите вариант ниже:",
        "ticket_prompt": "📝 Пожалуйста, отправьте ваше сообщение в службу поддержки:",
        "ticket_success": "✅ Ваш тикет успешно отправлен админу!"
    },
    "uk": {
        "welcome": "Ласкаво просимо до Krelivo Store! 🚀\n\nДосліджуйте наші ексклюзивні цифрові продукти нижче.",
        "catalog": "📦 Каталог", "cart": "🛒 Кошик", "profile": "👤 Профіль",
        "premium": "⭐ Преміум", "affiliate": "🤝 Реферати",
        "language": "🌐 Мова", "support": "🎫 Підтримка",
        "back": "🔙 Назад", "new_ticket": "🎫 Новий тикет", "my_tickets": "📁 Мої тикети",
        "privacy": "🔒 Конфіденційність", "terms": "📄 Умови",
        "support_text": "🎫 **Центр підтримки**\n\nВиберіть варіант нижче:",
        "ticket_prompt": "📝 Надішліть ваше повідомлення до служби підтримки:",
        "ticket_success": "✅ Ваш тикет успішно надіслано!"
    },
    "ar": {
        "welcome": "أهلاً بك في متجر Krelivo! 🚀\n\nاستكشف منتجاتنا وخدماتنا الرقمية الحصرية أدناه.",
        "catalog": "📦 الكتالوج", "cart": "🛒 السلة", "profile": "👤 الملف",
        "premium": "⭐ المميزة", "affiliate": "🤝 نظام الإحالة",
        "language": "🌐 اللغة", "support": "🎫 الدعم",
        "back": "🔙 رجوع", "new_ticket": "🎫 تذكرة جديدة", "my_tickets": "📁 تذاكري",
        "privacy": "🔒 الخصوصية", "terms": "📄 الشروط",
        "support_text": "🎫 **مركز الدعم**\n\nاختر أحد الخيارات أدناه:",
        "ticket_prompt": "📝 يرجى إرسال رسالتك لفريق الدعم:",
        "ticket_success": "✅ تم إرسال تذكرتك بنجاح!"
    },
    "zh": {
        "welcome": "欢迎来到 Krelivo 商店！🚀\n\n在下方探索我们的独家数字产品和服务。",
        "catalog": "📦 目录", "cart": "🛒 购物车", "profile": "👤 个人资料",
        "premium": "⭐ 高级", "affiliate": "🤝 推荐系统",
        "language": "🌐 语言", "support": "🎫 支持",
        "back": "🔙 返回", "new_ticket": "🎫 新建工单", "my_tickets": "📁 我的工单",
        "privacy": "🔒 隐私政策", "terms": "📄 服务条款",
        "support_text": "🎫 **支持中心**\n\n请选择以下选项：",
        "ticket_prompt": "📝 请发送您的留言给支持团队：",
        "ticket_success": "✅ 您的工单已成功提交！"
    },
    "es": {
        "welcome": "¡Bienvenido a Krelivo Store! 🚀\n\nExplora nuestros productos y servicios digitales exclusivos a continuación.",
        "catalog": "📦 Catálogo", "cart": "🛒 Carrito", "profile": "👤 Perfil",
        "premium": "⭐ Premium", "affiliate": "🤝 Sistema de referidos",
        "language": "🌐 Idioma", "support": "🎫 Soporte",
        "back": "🔙 Volver", "new_ticket": "🎫 Nuevo ticket", "my_tickets": "📁 Mis tickets",
        "privacy": "🔒 Privacidad", "terms": "📄 Términos",
        "support_text": "🎫 **Centro de Soporte**\n\nElige una opción:",
        "ticket_prompt": "📝 Envía tu mensaje al equipo de soporte:",
        "ticket_success": "✅ ¡Tu ticket ha sido enviado con éxito!"
    },
    "id": {
        "welcome": "Selamat datang di Krelivo Store! 🚀\n\nJelajahi produk dan layanan digital eksklusif kami di bawah ini.",
        "catalog": "📦 Katalog", "cart": "🛒 Keranjang", "profile": "👤 Profil",
        "premium": "⭐ Premium", "affiliate": "🤝 Sistem Rujukan",
        "language": "🌐 Bahasa", "support": "🎫 Dukungan",
        "back": "🔙 Kembali", "new_ticket": "🎫 Tiket Baru", "my_tickets": "📁 Tiket Saya",
        "privacy": "🔒 Privasi", "terms": "📄 Ketentuan",
        "support_text": "🎫 **Pusat Dukungan**\n\nPilih opsi di bawah:",
        "ticket_prompt": "📝 Kirimkan pesan Anda ke tim dukungan:",
        "ticket_success": "✅ Tiket Anda berhasil dikirim!"
    },
    "pt": {
        "welcome": "Bem-vindo à Krelivo Store! 🚀\n\nExplore nossos produtos e serviços digitais exclusivos abaixo.",
        "catalog": "📦 Catálogo", "cart": "🛒 Carrinho", "profile": "👤 Perfil",
        "premium": "⭐ Premium", "affiliate": "🤝 Sistema de indicações",
        "language": "🌐 Idioma", "support": "🎫 Suporte",
        "back": "🔙 Voltar", "new_ticket": "🎫 Novo ticket", "my_tickets": "📁 Meus tickets",
        "privacy": "🔒 Privacidade", "terms": "📄 Termos",
        "support_text": "🎫 **Centro de Suporte**\n\nEscolha uma opção:",
        "ticket_prompt": "📝 Envie sua mensagem para o suporte:",
        "ticket_success": "✅ Seu ticket foi enviado com sucesso!"
    },
    "fr": {
        "welcome": "Bienvenue sur Krelivo Store ! 🚀\n\nDécouvrez nos produits et services numériques exclusifs ci-dessous.",
        "catalog": "📦 Catalogue", "cart": "🛒 Panier", "profile": "👤 Profil",
        "premium": "⭐ Premium", "affiliate": "🤝 Parrainage",
        "language": "🌐 Langue", "support": "🎫 Support",
        "back": "🔙 Retour", "new_ticket": "🎫 Nouveau ticket", "my_tickets": "📁 Mes tickets",
        "privacy": "🔒 Confidentialité", "terms": "📄 Conditions",
        "support_text": "🎫 **Centre de Support**\n\nChoisissez une option :",
        "ticket_prompt": "📝 Veuillez envoyer votre message au support :",
        "ticket_success": "✅ Votre ticket a été envoyé avec succès !"
    },
    "tr": {
        "welcome": "Krelivo Mağazasına Hoş Geldiniz! 🚀\n\nÖzel dijital ürünlerimizi ve hizmetlerimizi aşağıda keşfedin.",
        "catalog": "📦 Katalog", "cart": "🛒 Sepet", "profile": "👤 Profil",
        "premium": "⭐ Premium", "affiliate": "🤝 Referans Sistemi",
        "language": "🌐 Dil", "support": "🎫 Destek",
        "back": "🔙 Geri", "new_ticket": "🎫 Yeni Destek", "my_tickets": "📁 Biletlerim",
        "privacy": "🔒 Gizlilik", "terms": "📄 Şartlar",
        "support_text": "🎫 **Destek Merkezi**\n\nAşağıdan bir seçenek seçin:",
        "ticket_prompt": "📝 Lütfen mesajınızı destek ekibine gönderin:",
        "ticket_success": "✅ Destek talebiniz başarıyla iletildi!"
    },
    "vi": {
        "welcome": "Chào mừng đến với Krelivo Store! 🚀\n\nKhám phá các sản phẩm và dịch vụ kỹ thuật số độc quyền của chúng tôi bên dưới.",
        "catalog": "📦 Danh mục", "cart": "🛒 Giỏ hàng", "profile": "👤 Hồ sơ",
        "premium": "⭐ Premium", "affiliate": "🤝 Hệ thống giới thiệu",
        "language": "🌐 Ngôn ngữ", "support": "🎫 Hỗ trợ",
        "back": "🔙 Quay lại", "new_ticket": "🎫 Tạo vé mới", "my_tickets": "📁 Vé của tôi",
        "privacy": "🔒 Bảo mật", "terms": "📄 Điều khoản",
        "support_text": "🎫 **Trung tâm hỗ trợ**\n\nVui lòng chọn tùy chọn bên dưới:",
        "ticket_prompt": "📝 Gửi tin nhắn của bạn cho đội ngũ hỗ trợ:",
        "ticket_success": "✅ Yêu cầu hỗ trợ đã được gửi thành công!"
    },
    "de": {
        "welcome": "Willkommen im Krelivo Store! 🚀\n\nEntdecken Sie unten unsere exklusiven digitalen Produkte und Dienstleistungen.",
        "catalog": "📦 Katalog", "cart": "🛒 Warenkorb", "profile": "👤 Profil",
        "premium": "⭐ Premium", "affiliate": "🤝 Empfehlungssystem",
        "language": "🌐 Sprache", "support": "🎫 Support",
        "back": "🔙 Zurück", "new_ticket": "🎫 Neues Ticket", "my_tickets": "📁 Meine Tickets",
        "privacy": "🔒 Datenschutz", "terms": "📄 AGB",
        "support_text": "🎫 **Support-Center**\n\nWählen Sie eine Option:",
        "ticket_prompt": "📝 Bitte senden Sie Ihre Nachricht an den Support:",
        "ticket_success": "✅ Ihr Ticket wurde erfolgreich gesendet!"
    },
    "it": {
        "welcome": "Benvenuto su Krelivo Store! 🚀\n\nEsplora i nostri prodotti e servizi digitali esclusivi qui sotto.",
        "catalog": "📦 Catalogo", "cart": "🛒 Carrello", "profile": "👤 Profilo",
        "premium": "⭐ Premium", "affiliate": "🤝 Sistema di affiliazione",
        "language": "🌐 Lingua", "support": "🎫 Supporto",
        "back": "🔙 Indietro", "new_ticket": "🎫 Nuovo ticket", "my_tickets": "📁 I miei ticket",
        "privacy": "🔒 Privacy", "terms": "📄 Termini",
        "support_text": "🎫 **Centro Assistenza**\n\nScegli un'opzione:",
        "ticket_prompt": "📝 Invia il tuo messaggio al supporto:",
        "ticket_success": "✅ Il tuo ticket è stato inviato con successo!"
    }
}

@app.route('/')
def home():
    return "Bot is alive and running!"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    args = message.text.split()
    
    if len(args) > 1 and args[1].startswith("ref_"):
        try:
            inviter_id = int(args[1].replace("ref_", ""))
            if inviter_id != user_id and user_id not in user_referred:
                user_referred.add(user_id)
                user_invites[inviter_id] = user_invites.get(inviter_id, 0) + 1
                try:
                    bot.send_message(inviter_id, "✨ Someone joined via your referral link! Reward added.")
                except:
                    pass
        except:
            pass

    show_main_menu(message.chat.id, None, is_new=True)

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

def show_language_menu(chat_id, message_id):
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

def show_support_menu(chat_id, message_id):
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

def show_affiliate_menu(chat_id, message_id):
    lang = user_languages.get(chat_id, "en")
    t = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    count = user_invites.get(chat_id, 0)
    ref_link = f"https://t.me/Krelivo_bot?start=ref_{chat_id}"
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🔗 Share Link", url=f"https://t.me/share/url?url={ref_link}&text=Join%20Krelivo%20Store!"),
        types.InlineKeyboardButton(t["back"], callback_data="main_menu")
    )
    
    text = (
        "🤝 **Referral System** ⭐\n\n"
        f"🔗 **Invite Link:**\n`{ref_link}`\n\n"
        f"📊 **Stats:**\n• Invited: **{count}**\n• Earned: **{count * 10} ⭐️**"
    )
    bot.edit_message_text(text, chat_id, message_id, reply_markup=markup, parse_mode="Markdown")

def show_premium_menu(chat_id, message_id):
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
    bot.edit_message_text("⭐ **Premium Plans (30 Days)**\nChoose your plan:", chat_id, message_id, reply_markup=markup, parse_mode="Markdown")

def show_catalog(chat_id, message_id):
    lang = user_languages.get(chat_id, "en")
    t = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(t["back"], callback_data="main_menu"))
    bot.edit_message_text("📦 **Catalog:**\nExclusive digital products will appear here soon.", chat_id, message_id, reply_markup=markup, parse_mode="Markdown")

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
        show_premium_menu(chat_id, message_id)
    elif call.data == "affiliate":
        bot.answer_callback_query(call.id)
        show_affiliate_menu(chat_id, message_id)
    elif call.data == "language":
        bot.answer_callback_query(call.id)
        show_language_menu(chat_id, message_id)
    elif call.data == "support":
        bot.answer_callback_query(call.id)
        show_support_menu(chat_id, message_id)
    elif call.data.startswith("lang_"):
        lang_code = call.data.replace("lang_", "")
        user_languages[chat_id] = lang_code
        bot.answer_callback_query(call.id, "Language updated!")
        show_main_menu(chat_id, message_id)
    elif call.data == "catalog":
        bot.answer_callback_query(call.id)
        show_catalog(chat_id, message_id)
    elif call.data == "cart":
        bot.answer_callback_query(call.id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(t["back"], callback_data="main_menu"))
        bot.edit_message_text("🛒 **Shopping Cart:**\nYour cart is empty.", chat_id, message_id, reply_markup=markup, parse_mode="Markdown")
    elif call.data == "profile":
        bot.answer_callback_query(call.id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(t["back"], callback_data="main_menu"))
        bot.edit_message_text(f"👤 **Profile:**\nID: `{chat_id}`\nStatus: Active", chat_id, message_id, reply_markup=markup, parse_mode="Markdown")
    elif call.data == "new_ticket":
        bot.answer_callback_query(call.id)
        user_states[chat_id] = "waiting_for_ticket"
        bot.send_message(chat_id, t["ticket_prompt"])
    elif call.data == "my_tickets":
        bot.answer_callback_query(call.id)
        user_list = user_tickets.get(chat_id, [])
        ticket_msg = "📁 **Your Tickets:**\n\n" + ("\n".join(user_list) if user_list else "No active tickets.")
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(t["back"], callback_data="support"))
        bot.edit_message_text(ticket_msg, chat_id, message_id, reply_markup=markup, parse_mode="Markdown")
    elif call.data == "privacy_policy":
        bot.answer_callback_query(call.id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(t["back"], callback_data="support"))
        bot.edit_message_text("🔒 **Privacy Policy:**\nYour data is completely secure.", chat_id, message_id, reply_markup=markup, parse_mode="Markdown")
    elif call.data == "terms_service":
        bot.answer_callback_query(call.id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(t["back"], callback_data="support"))
        bot.edit_message_text("📄 **Terms of Service:**\nAll sales are final.", chat_id, message_id, reply_markup=markup, parse_mode="Markdown")
    elif call.data.startswith("pay_"):
        bot.answer_callback_query(call.id)
        prices = {"pay_single": 50, "pay_basic": 290, "pay_pro": 690, "pay_ultra": 1990}
        plan_name = call.data.replace("pay_", "").capitalize()
        amount = prices.get(call.data, 50)
        bot.send_invoice(
            chat_id=chat_id,
            title=f"Krelivo {plan_name} Plan",
            description=f"Subscription for {plan_name} package (30 Days)",
            invoice_payload=f"krelivo_{plan_name.lower()}",
            provider_token="",
            currency="XTR",
            prices=[types.LabeledPrice(label=f"{plan_name} Plan", amount=amount)]
        )

@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == "waiting_for_ticket")
def receive_ticket(message):
    chat_id = message.chat.id
    lang = user_languages.get(chat_id, "en")
    t = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    
    if chat_id not in user_tickets:
        user_tickets[chat_id] = []
    
    user_tickets[chat_id].append(f"• {message.text}")
    user_states[chat_id] = None
    bot.send_message(chat_id, t["ticket_success"])
    
    # ارسال پیام تیکت به ادمین (خودت)
    admin_notice = f"🚨 **New Support Ticket!**\n\n👤 **User ID:** `{chat_id}`\n💬 **Message:** {message.text}"
    try:
        if ADMIN_ID != 530000000:
            bot.send_message(ADMIN_ID, admin_notice, parse_mode="Markdown")
        else:
            bot.send_message(chat_id, f"[Admin Copy Notice]: Ticket recorded. (Set your ADMIN_ID in code to receive copies directly)")
    except:
        pass
        
    show_main_menu(chat_id)

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
