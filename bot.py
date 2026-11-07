import os
import telebot
from telebot import types
from flask import Flask
import threading

TOKEN = "9081123644:AAGv3PKfhdXcllBYkvvy11W07fKub6VLKqQ"
bot = telebot.TeleBot(TOKEN)

app = Flask('')

# ذخیره زبان و وضعیت کاربران
user_languages = {}
user_states = {}
user_invites = {}
user_referred = set()
user_tickets = {}

# دیکشنری کامل ترجمه برای ۱۴ زبان (هر دکمه دقیقاً یک ایموجی)
TRANSLATIONS = {
    "en": {
        "welcome": "Welcome to Krelivo Store! 🚀\n\nExplore our exclusive digital products and services below.",
        "catalog": "📦 Catalog", "cart": "🛒 Cart", "profile": "👤 Profile",
        "premium": "⭐ Premium", "affiliate": "🤝 Affiliate",
        "language": "🌐 Language", "support": "🎫 Support", "tonkeeper": "💎 Tonkeeper",
        "back": "🔙 Back", "new_ticket": "🎫 New Ticket", "my_tickets": "📁 My Tickets",
        "privacy": "🔒 Privacy Policy", "terms": "📄 Terms of Service",
        "support_text": "🎫 **Support Center**\n\nIf you have any questions or issues, please choose an option below:",
        "ticket_prompt": "📝 Please send your message or issue for the support team:",
        "ticket_success": "✅ Your ticket has been submitted successfully! We will reply soon."
    },
    "fa": {
        "welcome": "به فروشگاه کرلیوو خوش آمدید! 🚀\n\nمحصولات و خدمات انحصاری ما را در زیر بررسی کنید.",
        "catalog": "📦 کاتالوگ", "cart": "🛒 سبد خرید", "profile": "👤 پروفایل",
        "premium": "⭐ پریمیوم", "affiliate": "🤝 همکاری",
        "language": "🌐 زبان", "support": "🎫 پشتیبانی", "tonkeeper": "💎 تن‌کیپر",
        "back": "🔙 بازگشت", "new_ticket": "🎫 تیکت جدید", "my_tickets": "📁 تیکت‌های من",
        "privacy": "🔒 حریم خصوصی", "terms": "📄 شرایط خدمات",
        "support_text": "🎫 **مرکز پشتیبانی**\n\nاگر سؤال یا مشکلی داری، لطفاً یکی از گزینه‌های زیر را انتخاب کن:",
        "ticket_prompt": "📝 لطفاً پیام یا مشکل خود را برای تیم پشتیبانی ارسال کنید:",
        "ticket_success": "✅ تیکت شما با موفقیت ثبت شد! به زودی پاسخگوی شما خواهیم بود."
    },
    "ru": {
        "welcome": "Добро пожаловать в Krelivo Store! 🚀\n\nИзучите наши эксклюзивные цифровые продукты ниже.",
        "catalog": "📦 Каталог", "cart": "🛒 Корзина", "profile": "👤 Профиль",
        "premium": "⭐ Премиум", "affiliate": "🤝 Партнеры",
        "language": "🌐 Язык", "support": "🎫 Поддержка", "tonkeeper": "💎 Tonkeeper",
        "back": "🔙 Назад", "new_ticket": "🎫 Новый тикет", "my_tickets": "📁 Мои тикеты",
        "privacy": "🔒 Конфиденциальность", "terms": "📄 Условия",
        "support_text": "🎫 **Центр поддержки**\n\nЕсли у вас есть вопросы, выберите вариант ниже:",
        "ticket_prompt": "📝 Пожалуйста, отправьте ваше сообщение в службу поддержки:",
        "ticket_success": "✅ Ваш тикет успешно создан! Мы скоро ответим."
    },
    "uk": {
        "welcome": "Ласкаво просимо до Krelivo Store! 🚀\n\nДосліджуйте наші ексклюзивні цифрові продукти нижче.",
        "catalog": "📦 Каталог", "cart": "🛒 Кошик", "profile": "👤 Профіль",
        "premium": "⭐ Преміум", "affiliate": "🤝 Партнери",
        "language": "🌐 Мова", "support": "🎫 Підтримка", "tonkeeper": "💎 Tonkeeper",
        "back": "🔙 Назад", "new_ticket": "🎫 Новий тикет", "my_tickets": "📁 Мої тикети",
        "privacy": "🔒 Конфіденційність", "terms": "📄 Умови",
        "support_text": "🎫 **Центр підтримки**\n\nЯкщо у вас є питання, виберіть варіант нижче:",
        "ticket_prompt": "📝 Будь ласка, надішліть ваше повідомлення до служби підтримки:",
        "ticket_success": "✅ Ваш тикет успішно створено! Скоро відповімо."
    },
    "ar": {
        "welcome": "أهلاً بك في متجر Krelivo! 🚀\n\nاستكشف منتجاتنا وخدماتنا الرقمية الحصرية أدناه.",
        "catalog": "📦 الكتالوج", "cart": "🛒 السلة", "profile": "👤 الملف",
        "premium": "⭐ المميزة", "affiliate": "🤝 الشراكة",
        "language": "🌐 اللغة", "support": "🎫 الدعم", "tonkeeper": "💎 تنکیپر",
        "back": "🔙 رجوع", "new_ticket": "🎫 تذكرة جديدة", "my_tickets": "📁 تذاكري",
        "privacy": "🔒 الخصوصية", "terms": "📄 الشروط",
        "support_text": "🎫 **مركز الدعم**\n\nإذا كان لديك أي استفسار، يختار أحد الخيارات أدناه:",
        "ticket_prompt": "📝 يرجى إرسال رسالتك أو مشكلتك لفريق الدعم:",
        "ticket_success": "✅ تم إرسال تذكرتك بنجاح! سنقوم بالرد عليك قريباً."
    },
    "zh": {
        "welcome": "欢迎来到 Krelivo 商店！🚀\n\n在下方探索我们的独家数字产品和服务。",
        "catalog": "📦 目录", "cart": "🛒 购物车", "profile": "👤 个人资料",
        "premium": "⭐ 高级", "affiliate": "🤝 联盟",
        "language": "🌐 语言", "support": "🎫 支持", "tonkeeper": "💎 钱包",
        "back": "🔙 返回", "new_ticket": "🎫 新建工单", "my_tickets": "📁 我的工单",
        "privacy": "🔒 隐私政策", "terms": "📄 服务条款",
        "support_text": "🎫 **支持中心**\n\n如果您有任何问题，请选择以下选项：",
        "ticket_prompt": "📝 请发送您的留言或问题给支持团队：",
        "ticket_success": "✅ 您的工单已成功提交！我们将尽快回复。"
    },
    "es": {
        "welcome": "¡Bienvenido a Krelivo Store! 🚀\n\nExplora nuestros productos y servicios digitales exclusivos a continuación.",
        "catalog": "📦 Catálogo", "cart": "🛒 Carrito", "profile": "👤 Perfil",
        "premium": "⭐ Premium", "affiliate": "🤝 Afiliados",
        "language": "🌐 Idioma", "support": "🎫 Soporte", "tonkeeper": "💎 Tonkeeper",
        "back": "🔙 Volver", "new_ticket": "🎫 Nuevo ticket", "my_tickets": "📁 Mis tickets",
        "privacy": "🔒 Privacidad", "terms": "📄 Términos",
        "support_text": "🎫 **Centro de Soporte**\n\nSi tienes dudas o problemas, elige una opción:",
        "ticket_prompt": "📝 Por favor, envía tu mensaje o problema al equipo de soporte:",
        "ticket_success": "✅ ¡Tu ticket ha sido enviado con éxito! Responderemos pronto."
    },
    "id": {
        "welcome": "Selamat datang di Krelivo Store! 🚀\n\nJelajahi produk dan layanan digital eksklusif kami di bawah ini.",
        "catalog": "📦 Katalog", "cart": "🛒 Keranjang", "profile": "👤 Profil",
        "premium": "⭐ Premium", "affiliate": "🤝 Afiliasi",
        "language": "🌐 Bahasa", "support": "🎫 Dukungan", "tonkeeper": "💎 Tonkeeper",
        "back": "🔙 Kembali", "new_ticket": "🎫 Tiket Baru", "my_tickets": "📁 Tiket Saya",
        "privacy": "🔒 Privasi", "terms": "📄 Ketentuan",
        "support_text": "🎫 **Pusat Dukungan**\n\nJika Anda memiliki pertanyaan, pilih opsi di bawah:",
        "ticket_prompt": "📝 Silakan kirim pesan atau masalah Anda ke tim dukungan:",
        "ticket_success": "✅ Tiket Anda berhasil dikirim! Kami akan segera membalas."
    },
    "pt": {
        "welcome": "Bem-vindo à Krelivo Store! 🚀\n\nExplore nossos produtos e serviços digitais exclusivos abaixo.",
        "catalog": "📦 Catálogo", "cart": "🛒 Carrinho", "profile": "👤 Perfil",
        "premium": "⭐ Premium", "affiliate": "🤝 Afiliados",
        "language": "🌐 Idioma", "support": "🎫 Suporte", "tonkeeper": "💎 Tonkeeper",
        "back": "🔙 Voltar", "new_ticket": "🎫 Novo ticket", "my_tickets": "📁 Meus tickets",
        "privacy": "🔒 Privacidade", "terms": "📄 Termos",
        "support_text": "🎫 **Centro de Suporte**\n\nSe você tiver dúvidas, escolha uma opção abaixo:",
        "ticket_prompt": "📝 Por favor, envie sua mensagem para a equipe de suporte:",
        "ticket_success": "✅ Seu ticket foi enviado com sucesso! Responderemos em breve."
    },
    "fr": {
        "welcome": "Bienvenue sur Krelivo Store ! 🚀\n\nDécouvrez nos produits et services numériques exclusifs ci-dessous.",
        "catalog": "📦 Catalogue", "cart": "🛒 Panier", "profile": "👤 Profil",
        "premium": "⭐ Premium", "affiliate": "🤝 Affiliation",
        "language": "🌐 Langue", "support": "🎫 Support", "tonkeeper": "💎 Tonkeeper",
        "back": "🔙 Retour", "new_ticket": "🎫 Nouveau ticket", "my_tickets": "📁 Mes tickets",
        "privacy": "🔒 Confidentialité", "terms": "📄 Conditions",
        "support_text": "🎫 **Centre de Support**\n\nSi vous avez des questions, choisissez une option :",
        "ticket_prompt": "📝 Veuillez envoyer votre message à l'équipe de support :",
        "ticket_success": "✅ Votre ticket a été envoyé avec succès ! Nous répondrons bientôt."
    },
    "tr": {
        "welcome": "Krelivo Mağazasına Hoş Geldiniz! 🚀\n\nÖzel dijital ürünlerimizi ve hizmetlerimizi aşağıda keşfedin.",
        "catalog": "📦 Katalog", "cart": "🛒 Sepet", "profile": "👤 Profil",
        "premium": "⭐ Premium", "affiliate": "🤝 Ortaklık",
        "language": "🌐 Dil", "support": "🎫 Destek", "tonkeeper": "💎 Tonkeeper",
        "back": "🔙 Geri", "new_ticket": "🎫 Yeni Destek", "my_tickets": "📁 Biletlerim",
        "privacy": "🔒 Gizlilik", "terms": "📄 Şartlar",
        "support_text": "🎫 **Destek Merkezi**\n\nSorularınız veya sorunlarınız varsa aşağıdan seçin:",
        "ticket_prompt": "📝 Lütfen destek ekibi için mesajınızı veya sorununuzu gönderin:",
        "ticket_success": "✅ Destek talebiniz başarıyla alındى! En kısa sürede döneceğiz."
    },
    "vi": {
        "welcome": "Chào mừng đến với Krelivo Store! 🚀\n\nKhám phá các sản phẩm và dịch vụ kỹ thuật số độc quyền của chúng tôi bên dưới.",
        "catalog": "📦 Danh mục", "cart": "🛒 Giỏ hàng", "profile": "👤 Hồ sơ",
        "premium": "⭐ Premium", "affiliate": "🤝 Liên kết",
        "language": "🌐 Ngôn ngữ", "support": "🎫 Hỗ trợ", "tonkeeper": "💎 Tonkeeper",
        "back": "🔙 Quay lại", "new_ticket": "🎫 Tạo vé mới", "my_tickets": "📁 Vé của tôi",
        "privacy": "🔒 Bảo mật", "terms": "📄 Điều khoản",
        "support_text": "🎫 **Trung tâm hỗ trợ**\n\nNếu bạn có thắc mắc, vui lòng chọn một tùy chọn:",
        "ticket_prompt": "📝 Vجi lòng gửi tin nhắn hoặc vấn đề của bạn cho đội ngũ hỗ trợ:",
        "ticket_success": "✅ Yêu cầu hỗ trợ đã được gửi thành công! Chúng tôi sẽ phản hồi sớm."
    },
    "de": {
        "welcome": "Willkommen im Krelivo Store! 🚀\n\nEntdecken Sie unten unsere exklusiven digitalen Produkte und Dienstleistungen.",
        "catalog": "📦 Katalog", "cart": "🛒 Warenkorb", "profile": "👤 Profil",
        "premium": "⭐ Premium", "affiliate": "🤝 Partner",
        "language": "🌐 Sprache", "support": "🎫 Support", "tonkeeper": "💎 Tonkeeper",
        "back": "🔙 Zurück", "new_ticket": "🎫 Neues Ticket", "my_tickets": "📁 Meine Tickets",
        "privacy": "🔒 Datenschutz", "terms": "📄 AGB",
        "support_text": "🎫 **Support-Center**\n\nWenn Sie Fragen haben, wählen Sie bitte eine Option:",
        "ticket_prompt": "📝 Bitte senden Sie Ihre Nachricht an das Support-Team:",
        "ticket_success": "✅ Ihr Ticket wurde erfolgreich eingereicht! Wir antworten bald."
    },
    "it": {
        "welcome": "Benvenuto su Krelivo Store! 🚀\n\nEsplora i nostri prodotti e servizi digitali esclusivi qui sotto.",
        "catalog": "📦 Catalogo", "cart": "🛒 Carrello", "profile": "👤 Profilo",
        "premium": "⭐ Premium", "affiliate": "🤝 Affiliati",
        "language": "🌐 Lingua", "support": "🎫 Supporto", "tonkeeper": "💎 Tonkeeper",
        "back": "🔙 Indietro", "new_ticket": "🎫 Nuovo ticket", "my_tickets": "📁 I miei ticket",
        "privacy": "🔒 Privacy", "terms": "📄 Termini",
        "support_text": "🎫 **Centro Assistenza**\n\nSe hai domande o problemi, scegli un'opzione:",
        "ticket_prompt": "📝 Si prega di inviare il vostro messaggio al team di supporto:",
        "ticket_success": "✅ Il tuo ticket è stato inviato con successo! Risponderemo presto."
    }
}

@app.route('/')
def home():
    return "Bot is alive and running!"

@app.route('/webapp')
def webapp_page():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Krelivo WebApp Store</title>
        <style>
            body { background: #121314; color: #fff; font-family: Arial, sans-serif; text-align: center; padding: 20px; }
            .card { background: #1e1f22; padding: 25px; border-radius: 16px; margin: 20px auto; max-width: 420px; box-shadow: 0 6px 15px rgba(0,0,0,0.4); border: 1px solid #2f3136; }
            .btn-green { background: #22c55e; color: white; border: none; padding: 14px 20px; border-radius: 10px; font-weight: bold; cursor: pointer; width: 100%; font-size: 16px; margin-top: 15px; }
        </style>
    </head>
    <body>
        <h2>Krelivo Global Store 🚀</h2>
        <div class="card">
            <h3>⭐ Pro Plan (30 Days)</h3>
            <p>Access all professional digital tools & features.</p>
            <p><strong>Price: 690 Stars ⭐️</strong></p>
            <button class="btn-green" onclick="Telegram.WebApp.close()">Confirm & Buy</button>
        </div>
        <script src="https://telegram.org/js/telegram-web-app.js"></script>
    </body>
    </html>
    """

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
        types.InlineKeyboardButton("🛍️ WebApp", web_app=types.WebAppInfo(url="https://krelivo-bot.onrender.com/webapp")),
        types.InlineKeyboardButton(t["catalog"], callback_data="catalog"),
        types.InlineKeyboardButton(t["cart"], callback_data="cart"),
        types.InlineKeyboardButton(t["profile"], callback_data="profile"),
        types.InlineKeyboardButton(t["premium"], callback_data="premium"),
        types.InlineKeyboardButton(t["affiliate"], callback_data="affiliate"),
        types.InlineKeyboardButton(t["language"], callback_data="language"),
        types.InlineKeyboardButton(t["support"], callback_data="support"),
        types.InlineKeyboardButton(t["tonkeeper"], url="https://tonkeeper.com/")
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
    bot.edit_message_text(
        "🌐 **Select Language / انتخاب زبان / Выберите язык**", 
        chat_id, message_id, reply_markup=markup, parse_mode="Markdown"
    )

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
        "🤝 **Affiliate Program** ⭐\n\n"
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
    bot.edit_message_text("⭐ **Premium Plans (30 Days)**\nChoose your subscription plan:", chat_id, message_id, reply_markup=markup, parse_mode="Markdown")

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
        bot.edit_message_text("🛒 **Shopping Cart:**\nYour cart is currently empty.", chat_id, message_id, reply_markup=markup, parse_mode="Markdown")
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
        ticket_msg = "📁 **Your Tickets:**\n\n" + ("\n".join(user_list) if user_list else "No active tickets found.")
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(t["back"], callback_data="support"))
        bot.edit_message_text(ticket_msg, chat_id, message_id, reply_markup=markup, parse_mode="Markdown")
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
