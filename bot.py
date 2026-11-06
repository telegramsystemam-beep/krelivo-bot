import os
import telebot
from telebot import types
from flask import Flask
import threading

TOKEN = "9081123644:AAGv3PKfhdXcllBYkvvy11W07fKub6VLKqQ"
bot = telebot.TeleBot(TOKEN)

app = Flask('')

# ذخیره زبان کاربران
user_languages = {}

# ترجمه کامل متن‌ها برای تمام زبان‌های درخواست‌شده
TRANSLATIONS = {
    "en": {
        "welcome": "Welcome to Krelivo Store! 🚀\n\nExplore our exclusive digital products and services below.",
        "catalog": "🛍️ Catalog", "cart": "🛒 Cart", "profile": "👤 Profile",
        "premium": "⭐ Premium Plans", "affiliate": "🤝 Affiliate Program",
        "language": "🌐 Language", "support": "📝 Support Ticket"
    },
    "fa": {
        "welcome": "به فروشگاه کرلیوو خوش آمدید! 🚀\n\nمحصولات و خدمات انحصاری ما را در زیر بررسی کنید.",
        "catalog": "🛍️ کاتالوگ", "cart": "🛒 سبد خرید", "profile": "👤 پروفایل",
        "premium": "⭐ اشتراک‌های پریمیوم", "affiliate": "🤝 برنامه همکاری در فروش",
        "language": "🌐 زبان", "support": "📝 تیکت پشتیبانی"
    },
    "ru": {
        "welcome": "Добро пожаловать в Krelivo Store! 🚀\n\nИзучите наши эксклюзивные цифровые продукты ниже.",
        "catalog": "🛍️ Каталог", "cart": "🛒 Корзина", "profile": "👤 Профиль",
        "premium": "⭐ Премиум планы", "affiliate": "🤝 Партнерская программа",
        "language": "🌐 Язык", "support": "📝 Поддержка"
    },
    "uk": {
        "welcome": "Ласкаво просимо до Krelivo Store! 🚀\n\nДосліджуйте наші ексклюзивні цифрові продукти нижче.",
        "catalog": "🛍️ Каталог", "cart": "🛒 Кошик", "profile": "👤 Профіль",
        "premium": "⭐ Преміум плани", "affiliate": "🤝 Партнерська програма",
        "language": "🌐 Мова", "support": "📝 Підтримка"
    },
    "ar": {
        "welcome": "أهلاً بك في متجر Krelivo! 🚀\n\nاستكشف منتجاتنا وخدماتنا الرقمية الحصرية أدناه.",
        "catalog": "🛍️ الكتالوج", "cart": "🛒 السلة", "profile": "👤 الملف الشخصي",
        "premium": "⭐ الخطط المميزة", "affiliate": "🤝 برنامج الشراكة",
        "language": "🌐 اللغة", "support": "📝 تذكرة الدعم"
    },
    "zh": {
        "welcome": "欢迎来到 Krelivo 商店！🚀\n\n在下方探索我们的独家数字产品和服务。",
        "catalog": "🛍️ 目录", "cart": "🛒 购物车", "profile": "👤 个人资料",
        "premium": "⭐ 高级计划", "affiliate": "🤝 联盟计划",
        "language": "🌐 语言", "support": "📝 支持工单"
    },
    "es": {
        "welcome": "¡Bienvenido a Krelivo Store! 🚀\n\nExplora nuestros productos y servicios digitales exclusivos a continuación.",
        "catalog": "🛍️ Catálogo", "cart": "🛒 Carrito", "profile": "👤 Perfil",
        "premium": "⭐ Planes Premium", "affiliate": "🤝 Programa de Afiliados",
        "language": "🌐 Idioma", "support": "📝 Soporte"
    },
    "id": {
        "welcome": "Selamat datang di Krelivo Store! 🚀\n\nJelajahi produk dan layanan digital eksklusif kami di bawah ini.",
        "catalog": "🛍️ Katalog", "cart": "🛒 Keranjang", "profile": "👤 Profil",
        "premium": "⭐ Paket Premium", "affiliate": "🤝 Program Afiliasi",
        "language": "🌐 Bahasa", "support": "📝 Tiket Dukungan"
    },
    "pt": {
        "welcome": "Bem-vindo à Krelivo Store! 🚀\n\nExplore nossos produtos e serviços digitais exclusivos abaixo.",
        "catalog": "🛍️ Catálogo", "cart": "🛒 Carrinho", "profile": "👤 Perfil",
        "premium": "⭐ Planos Premium", "affiliate": "🤝 Programa de Afiliados",
        "language": "🌐 Idioma", "support": "📝 Suporte"
    },
    "fr": {
        "welcome": "Bienvenue sur Krelivo Store ! 🚀\n\nDécouvrez nos produits et services numériques exclusifs ci-dessous.",
        "catalog": "🛍️ Catalogue", "cart": "🛒 Panier", "profile": "👤 Profil",
        "premium": "⭐ Plans Premium", "affiliate": "🤝 Programme d'affiliation",
        "language": "🌐 Langue", "support": "📝 Support"
    },
    "tr": {
        "welcome": "Krelivo Mağazasına Hoş Geldiniz! 🚀\n\nÖzel dijital ürünlerimizi ve hizmetlerimizi aşağıda keşfedin.",
        "catalog": "🛍️ Katalog", "cart": "🛒 Sepet", "profile": "👤 Profil",
        "premium": "⭐ Premium Planlar", "affiliate": "🤝 Ortaklık Programı",
        "language": "🌐 Dil", "support": "📝 Destek"
    },
    "vi": {
        "welcome": "Chào mừng đến với Krelivo Store! 🚀\n\nKhám phá các sản phẩm và dịch vụ kỹ thuật số độc quyền của chúng tôi bên dưới.",
        "catalog": "🛍️ Danh mục", "cart": "🛒 Giỏ hàng", "profile": "👤 Hồ sơ",
        "premium": "⭐ Gói Premium", "affiliate": "🤝 Chương trình liên kết",
        "language": "🌐 Ngôn ngữ", "support": "📝 Hỗ trợ"
    },
    "de": {
        "welcome": "Willkommen im Krelivo Store! 🚀\n\nEntdecken Sie unten unsere exklusiven digitalen Produkte und Dienstleistungen.",
        "catalog": "🛍️ Katalog", "cart": "🛒 Warenkorb", "profile": "👤 Profil",
        "premium": "⭐ Premium-Pakete", "affiliate": "🤝 Partnerprogramm",
        "language": "🌐 Sprache", "support": "📝 Support"
    },
    "it": {
        "welcome": "Benvenuto su Krelivo Store! 🚀\n\nEsplora i nostri prodotti e servizi digitali esclusivi qui sotto.",
        "catalog": "🛍️ Catalogo", "cart": "🛒 Carrello", "profile": "👤 Profilo",
        "premium": "⭐ Piani Premium", "affiliate": "🤝 Programma Affiliati",
        "language": "🌐 Lingua", "support": "📝 Supporto"
    }
}

user_invites = {}
user_referred = set()

@app.route('/')
def home():
    return "Bot is alive!"

@app.route('/webapp')
def webapp_page():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Krelivo Store</title>
        <style>
            body { background: #18191a; color: #fff; font-family: Arial, sans-serif; text-align: center; padding: 20px; }
            .card { background: #242526; padding: 20px; border-radius: 12px; margin: 15px auto; max-width: 400px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }
            .btn-green { background: #22c55e; color: white; border: none; padding: 12px 20px; border-radius: 8px; font-weight: bold; cursor: pointer; width: 100%; font-size: 16px; margin-top: 10px; }
        </style>
    </head>
    <body>
        <h2>Krelivo Global Store 🚀</h2>
        <div class="card">
            <h3>⭐ Pro Plan (30 Days)</h3>
            <p>Price: 690 Stars ⭐️</p>
            <button class="btn-green" onclick="alert('Selected successfully!')">Buy Now</button>
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
                    bot.send_message(inviter_id, "✨ Someone joined via your referral link! Your reward has been updated.")
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
        types.InlineKeyboardButton("🟢 🛍️ Open Krelivo WebApp", web_app=types.WebAppInfo(url="https://krelivo-bot.onrender.com/webapp")),
        types.InlineKeyboardButton(t["catalog"], callback_data="catalog"),
        types.InlineKeyboardButton(t["cart"], callback_data="cart"),
        types.InlineKeyboardButton(t["profile"], callback_data="profile"),
        types.InlineKeyboardButton(t["premium"], callback_data="premium"),
        types.InlineKeyboardButton(t["affiliate"], callback_data="affiliate"),
        types.InlineKeyboardButton(t["language"], callback_data="language"),
        types.InlineKeyboardButton(t["support"], callback_data="support"),
        types.InlineKeyboardButton("💎 Tonkeeper Pay", url="https://tonkeeper.com/")
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
        types.InlineKeyboardButton("« Back", callback_data="main_menu")
    )
    bot.edit_message_text(
        "🌐 **Select Language / انتخاب زبان / Выберите язык**\n\nChoose your preferred interface language:", 
        chat_id, message_id, reply_markup=markup, parse_mode="Markdown"
    )

def show_affiliate_menu(chat_id, message_id):
    count = user_invites.get(chat_id, 0)
    ref_link = f"https://t.me/Krelivo_bot?start=ref_{chat_id}"
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🔗 Share Referral Link", url=f"https://t.me/share/url?url={ref_link}&text=Join%20Krelivo%20Store%20and%20get%20exclusive%20digital%20products!"),
        types.InlineKeyboardButton("« Back to Main Menu", callback_data="main_menu")
    )
    
    text = (
        "🤝 **Affiliate Program** ⭐\n\n"
        "✨ Invite your friends and earn rewards for every referral!\n\n"
        f"🔗 **Your Invite Link:**\n`{ref_link}`\n\n"
        f"📊 **Your Stats:**\n"
        f"• Invited Users: **{count}**\n"
        f"• Rewards Earned: **{count * 10} ⭐️**"
    )
    bot.edit_message_text(text, chat_id, message_id, reply_markup=markup, parse_mode="Markdown")

def show_premium_menu(chat_id, message_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🟢 ⭐ Single Package – 50 ⭐️", callback_data="pay_single"),
        types.InlineKeyboardButton("🟢 ⭐ Basic (30 Days) – 290 ⭐️", callback_data="pay_basic"),
        types.InlineKeyboardButton("🟢 ⭐ Pro (30 Days) – 690 ⭐️", callback_data="pay_pro"),
        types.InlineKeyboardButton("🟢 ⭐ Ultra (30 Days) – 1990 ⭐️", callback_data="pay_ultra"),
        types.InlineKeyboardButton("« Back to Main Menu", callback_data="main_menu")
    )
    bot.edit_message_text("⭐ **Special Offers & Plans (30 Days)**\nChoose your subscription plan below:", chat_id, message_id, reply_markup=markup, parse_mode="Markdown")

def show_catalog(chat_id, message_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("« Back to Main Menu", callback_data="main_menu"))
    bot.edit_message_text("🛍️ **Catalog:**\nProducts will be loaded here soon. Stay tuned!", chat_id, message_id, reply_markup=markup, parse_mode="Markdown")

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
    elif call.data == "affiliate":
        bot.answer_callback_query(call.id)
        show_affiliate_menu(chat_id, message_id)
    elif call.data == "language":
        bot.answer_callback_query(call.id)
        show_language_menu(chat_id, message_id)
    elif call.data.startswith("lang_"):
        lang_code = call.data.replace("lang_", "")
        user_languages[chat_id] = lang_code
        bot.answer_callback_query(call.id, "Language updated successfully! / زبان با موفقیت تغییر کرد")
        show_main_menu(chat_id, message_id)
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
        prices = {
            "pay_single": 50,
            "pay_basic": 290,
            "pay_pro": 690,
            "pay_ultra": 1990
        }
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
