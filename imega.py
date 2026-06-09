"""
╔══════════════════════════════════════════════════════════════╗
║         RASM TINIQLASHTIRUVCHI TELEGRAM BOT                  ║
║         @imega_foto_4k_bot — Pro versiya                     ║
║         Tillar: UZ | RU | EN | KZ                            ║
╚══════════════════════════════════════════════════════════════╝

O'rnatish:
    pip install python-telegram-bot requests

Ishga tushirish:
    python bot.py
"""

import io, json, logging, os, time
from datetime import datetime, date, timedelta
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)

# ═══════════════════════════════════════════
#   SOZLAMALAR
# ═══════════════════════════════════════════
BOT_TOKEN      = "8615927460:AAEtFxnz1K5OyqCdcqgVXxu6IxLwT7XWpBg"
PICWISH_KEY    = "wxxlcfu0efn3ixhfd"
ADMIN_ID       = 8330377593
KARTA_RAQAM    = "9860080151682814"
KARTA_EGASI    = "Axadov A"
PREMIUM_NARX   = 10000
PREMIUM_KUN    = 30
BEPUL_LIMIT    = 5
PREMIUM_LIMIT  = 30
BOT_USERNAME   = "@imega_foto_4k_bot"

PICWISH_CREATE_URL = "https://techhk.aoscdn.com/api/tasks/visual/scale"
PICWISH_RESULT_URL = "https://techhk.aoscdn.com/api/tasks/visual/scale/{task_id}"

# ═══════════════════════════════════════════
#   TILLAR
# ═══════════════════════════════════════════
TILLAR = {
    "uz": {
        "til_nomi": "🇺🇿 O'zbek",
        "xush_kelibsiz": (
            "👋 Xush kelibsiz!\n\n"
            "📸 Menga rasm yuboring — sifat tanlaysiz,\n"
            "keyin AI orqali tiniqlashtiraman!\n\n"
            "📌 Buyruqlar:\n"
            "  /premium — Premium obuna\n"
            "  /holat — Hisobingiz\n"
            "  /referral — Do'st taklif qil\n"
            "  /til — Tilni o'zgartirish\n\n"
            "👇 Rasm yuboring:"
        ),
        "til_tanlang": "🌐 Tilni tanlang:",
        "sifat_tanlang": "🎚 Qaysi sifatda tiniqlashtirish kerak?",
        "rasm_qabul": "✅ Rasm qabul qilindi!\n\n",
        "qoldi": "Bugun qoldi: {} ta",
        "jarayon": "⏳ {} sifatda tiniqlashtir'lyapti...\nBiroz kuting...",
        "tayyor": "✨ Tayyor! Sifat: {}\n🤖 {} orqali tiniqlashtirildi\n📊 Bugun qoldi: {} ta",
        "limit_tugadi_bepul": (
            "⛔ Kunlik bepul limit tugadi! ({} ta/kun)\n\n"
            "⭐ Premium olsangiz:\n"
            "  • Kuniga 30 ta rasm\n"
            "  • 4K sifat\n"
            "  • Atigi {:,} so'm/oy"
        ),
        "limit_tugadi_premium": "⛔ Kunlik limit tugadi! (30 ta/kun)\n⏰ Limit ertaga yangilanadi.",
        "premium_tugma": "⭐ Premium olish",
        "premium_mavjud": "✅ Siz allaqachon Premium!\n📅 Tugash: {}",
        "premium_taklif": (
            "⭐ Premium obuna — {:,} so'm/oy\n\n"
            "✅ Premium imkoniyatlar:\n"
            "  • Kuniga 30 ta rasm (oddiy: 5 ta)\n"
            "  • 4K sifat\n"
            "  • Ustuvor ishlov\n\n"
            "👇 To'lov qilish:"
        ),
        "tolov_malumot": (
            "💳 To'lov ma'lumotlari:\n\n"
            "💰 Summa: {:,} so'm\n"
            "🏦 Karta: <code>{}</code>\n"
            "👤 Egasi: {}\n\n"
            "📌 To'lov qilgach:\n"
            "1️⃣ Chek (screenshot) shu botga yuboring\n"
            "2️⃣ Admin tekshiradi va Premium beradi\n"
            "⏳ Tasdiqlash: 1-24 soat\n\n"
            "❗ Izohga ID yozing: <code>{}</code>"
        ),
        "chek_qabul": "✅ Chekingiz qabul qilindi!\n⏳ Admin tekshiradi va tez orada javob beradi.",
        "chek_kutilmoqda": "⏳ Oldingi to'lovingiz ko'rib chiqilmoqda. Kuting!",
        "holat": (
            "📊 Hisobingiz:\n\n"
            "👤 Ism: {}\n"
            "🆔 ID: {}\n"
            "⭐ Obuna: {}\n"
            "📅 Premium tugash: {}\n"
            "📸 Bugun: {} ta\n"
            "🔢 Qoldi: {} ta\n"
            "🖼 Jami: {} ta\n"
            "👥 Referral: {} ta taklif → {} ta bonus rasm"
        ),
        "premium_label": "Premium ✅",
        "oddiy_label": "Oddiy",
        "blok": "🚫 Siz botdan bloklangansiz.",
        "premium_kerak": "🔒 Bu sifat faqat Premium uchun!\n\n⭐ Premium: {:,} so'm/oy\n✅ 4K sifat + kuniga 30 ta rasm",
        "referral_matn": (
            "👥 Referral tizimi:\n\n"
            "🔗 Sizning havolangiz:\n{}\n\n"
            "✅ Har bir yangi foydalanuvchi uchun +1 bepul rasm!\n"
            "📊 Taklif qilganlar: {} ta\n"
            "🎁 Qo'lga kiritilgan bonus: {} ta rasm\n"
            "💰 Qolgan bonus rasm: {} ta"
        ),
        "bonus_xabar": "🎁 Referral bonus: +1 bepul rasm qo'shildi! (do'stingiz qo'shildi)",
        "yangi_foydalanuvchi_ref": "🎉 Xush kelibsiz! Siz {} taklifi orqali keldingiz.",
        "xato": "❌ Xato yuz berdi: {}",
        "vaqt_tugadi": "⌛ Vaqt tugadi. Qayta urinib ko'ring!",
    },
    "ru": {
        "til_nomi": "🇷🇺 Русский",
        "xush_kelibsiz": (
            "👋 Добро пожаловать!\n\n"
            "📸 Отправьте мне фото — выберите качество,\n"
            "и я улучшу его с помощью AI!\n\n"
            "📌 Команды:\n"
            "  /premium — Подписка Premium\n"
            "  /holat — Ваш аккаунт\n"
            "  /referral — Пригласить друга\n"
            "  /til — Изменить язык\n\n"
            "👇 Отправьте фото:"
        ),
        "til_tanlang": "🌐 Выберите язык:",
        "sifat_tanlang": "🎚 Выберите качество улучшения:",
        "rasm_qabul": "✅ Фото принято!\n\n",
        "qoldi": "Осталось сегодня: {} шт",
        "jarayon": "⏳ Улучшение в качестве {}...\nПодождите...",
        "tayyor": "✨ Готово! Качество: {}\n🤖 Улучшено через {}\n📊 Осталось сегодня: {} шт",
        "limit_tugadi_bepul": (
            "⛔ Дневной лимит исчерпан! ({} шт/день)\n\n"
            "⭐ С Premium:\n"
            "  • 30 фото в день\n"
            "  • Качество 4K\n"
            "  • Всего {:,} сум/мес"
        ),
        "limit_tugadi_premium": "⛔ Дневной лимит исчерпан! (30 шт/день)\n⏰ Лимит обновится завтра.",
        "premium_tugma": "⭐ Получить Premium",
        "premium_mavjud": "✅ Вы уже Premium!\n📅 Действует до: {}",
        "premium_taklif": (
            "⭐ Premium подписка — {:,} сум/мес\n\n"
            "✅ Возможности Premium:\n"
            "  • 30 фото в день (обычно: 5)\n"
            "  • Качество 4K\n"
            "  • Приоритетная обработка\n\n"
            "👇 Оплатить:"
        ),
        "tolov_malumot": (
            "💳 Данные для оплаты:\n\n"
            "💰 Сумма: {:,} сум\n"
            "🏦 Карта: <code>{}</code>\n"
            "👤 Владелец: {}\n\n"
            "📌 После оплаты:\n"
            "1️⃣ Отправьте чек (скриншот) боту\n"
            "2️⃣ Админ проверит и активирует Premium\n"
            "⏳ Подтверждение: 1-24 часа\n\n"
            "❗ В комментарии укажите ID: <code>{}</code>"
        ),
        "chek_qabul": "✅ Чек принят!\n⏳ Админ проверит и скоро ответит.",
        "chek_kutilmoqda": "⏳ Ваша предыдущая оплата уже рассматривается. Подождите!",
        "holat": (
            "📊 Ваш аккаунт:\n\n"
            "👤 Имя: {}\n"
            "🆔 ID: {}\n"
            "⭐ Подписка: {}\n"
            "📅 Premium до: {}\n"
            "📸 Сегодня: {} шт\n"
            "🔢 Осталось: {} шт\n"
            "🖼 Всего: {} шт\n"
            "👥 Рефералы: {} чел → {} бонусных фото"
        ),
        "premium_label": "Premium ✅",
        "oddiy_label": "Обычный",
        "blok": "🚫 Вы заблокированы.",
        "premium_kerak": "🔒 Это качество только для Premium!\n\n⭐ Premium: {:,} сум/мес\n✅ 4K + 30 фото в день",
        "referral_matn": (
            "👥 Реферальная система:\n\n"
            "🔗 Ваша ссылка:\n{}\n\n"
            "✅ За каждого нового пользователя +1 бесплатное фото!\n"
            "📊 Приглашено: {} чел\n"
            "🎁 Получено бонусов: {} фото\n"
            "💰 Остаток бонусов: {} фото"
        ),
        "bonus_xabar": "🎁 Реферальный бонус: +1 фото добавлено! (ваш друг присоединился)",
        "yangi_foydalanuvchi_ref": "🎉 Добро пожаловать! Вы пришли по приглашению {}.",
        "xato": "❌ Ошибка: {}",
        "vaqt_tugadi": "⌛ Время вышло. Попробуйте ещё раз!",
    },
    "en": {
        "til_nomi": "🇬🇧 English",
        "xush_kelibsiz": (
            "👋 Welcome!\n\n"
            "📸 Send me a photo — choose quality,\n"
            "and I'll enhance it with AI!\n\n"
            "📌 Commands:\n"
            "  /premium — Premium subscription\n"
            "  /holat — Your account\n"
            "  /referral — Invite a friend\n"
            "  /til — Change language\n\n"
            "👇 Send a photo:"
        ),
        "til_tanlang": "🌐 Select language:",
        "sifat_tanlang": "🎚 Select enhancement quality:",
        "rasm_qabul": "✅ Photo received!\n\n",
        "qoldi": "Remaining today: {}",
        "jarayon": "⏳ Enhancing in {} quality...\nPlease wait...",
        "tayyor": "✨ Done! Quality: {}\n🤖 Enhanced via {}\n📊 Remaining today: {}",
        "limit_tugadi_bepul": (
            "⛔ Daily free limit reached! ({}/day)\n\n"
            "⭐ With Premium:\n"
            "  • 30 photos/day\n"
            "  • 4K quality\n"
            "  • Only {:,} UZS/month"
        ),
        "limit_tugadi_premium": "⛔ Daily limit reached! (30/day)\n⏰ Limit resets tomorrow.",
        "premium_tugma": "⭐ Get Premium",
        "premium_mavjud": "✅ You are already Premium!\n📅 Expires: {}",
        "premium_taklif": (
            "⭐ Premium subscription — {:,} UZS/month\n\n"
            "✅ Premium features:\n"
            "  • 30 photos/day (free: 5)\n"
            "  • 4K quality\n"
            "  • Priority processing\n\n"
            "👇 Make payment:"
        ),
        "tolov_malumot": (
            "💳 Payment details:\n\n"
            "💰 Amount: {:,} UZS\n"
            "🏦 Card: <code>{}</code>\n"
            "👤 Owner: {}\n\n"
            "📌 After payment:\n"
            "1️⃣ Send receipt (screenshot) to this bot\n"
            "2️⃣ Admin verifies and activates Premium\n"
            "⏳ Confirmation: 1-24 hours\n\n"
            "❗ Include your ID in notes: <code>{}</code>"
        ),
        "chek_qabul": "✅ Receipt accepted!\n⏳ Admin will verify and respond soon.",
        "chek_kutilmoqda": "⏳ Your previous payment is already being reviewed. Please wait!",
        "holat": (
            "📊 Your account:\n\n"
            "👤 Name: {}\n"
            "🆔 ID: {}\n"
            "⭐ Subscription: {}\n"
            "📅 Premium expires: {}\n"
            "📸 Today: {}\n"
            "🔢 Remaining: {}\n"
            "🖼 Total: {}\n"
            "👥 Referrals: {} invited → {} bonus photos"
        ),
        "premium_label": "Premium ✅",
        "oddiy_label": "Free",
        "blok": "🚫 You are banned from this bot.",
        "premium_kerak": "🔒 This quality is Premium only!\n\n⭐ Premium: {:,} UZS/month\n✅ 4K + 30 photos/day",
        "referral_matn": (
            "👥 Referral system:\n\n"
            "🔗 Your link:\n{}\n\n"
            "✅ +1 free photo for each new user!\n"
            "📊 Invited: {}\n"
            "🎁 Earned bonuses: {} photos\n"
            "💰 Bonus balance: {} photos"
        ),
        "bonus_xabar": "🎁 Referral bonus: +1 photo added! (your friend joined)",
        "yangi_foydalanuvchi_ref": "🎉 Welcome! You joined via {}'s invite.",
        "xato": "❌ Error: {}",
        "vaqt_tugadi": "⌛ Timed out. Please try again!",
    },
    "kz": {
        "til_nomi": "🇰🇿 Қазақ",
        "xush_kelibsiz": (
            "👋 Қош келдіңіз!\n\n"
            "📸 Маған сурет жіберіңіз — сапаны таңдаңыз,\n"
            "AI арқылы жақсартамын!\n\n"
            "📌 Командалар:\n"
            "  /premium — Premium жазылым\n"
            "  /holat — Аккаунтыңыз\n"
            "  /referral — Дос шақыру\n"
            "  /til — Тілді өзгерту\n\n"
            "👇 Сурет жіберіңіз:"
        ),
        "til_tanlang": "🌐 Тілді таңдаңыз:",
        "sifat_tanlang": "🎚 Қандай сапада жақсарту керек?",
        "rasm_qabul": "✅ Сурет қабылданды!\n\n",
        "qoldi": "Бүгін қалды: {} дана",
        "jarayon": "⏳ {} сапасында жақсартылуда...\nКүтіңіз...",
        "tayyor": "✨ Дайын! Сапа: {}\n🤖 {} арқылы жақсартылды\n📊 Бүгін қалды: {} дана",
        "limit_tugadi_bepul": (
            "⛔ Күндік тегін лимит бітті! ({} дана/күн)\n\n"
            "⭐ Premium алсаңыз:\n"
            "  • Күніне 30 сурет\n"
            "  • 4K сапа\n"
            "  • Небары {:,} сум/ай"
        ),
        "limit_tugadi_premium": "⛔ Күндік лимит бітті! (30 дана/күн)\n⏰ Лимит ертең жаңарады.",
        "premium_tugma": "⭐ Premium алу",
        "premium_mavjud": "✅ Сіз Premium пайдаланушысысыз!\n📅 Мерзімі: {}",
        "premium_taklif": (
            "⭐ Premium жазылым — {:,} сум/ай\n\n"
            "✅ Premium мүмкіндіктер:\n"
            "  • Күніне 30 сурет (тегін: 5)\n"
            "  • 4K сапа\n"
            "  • Басымдықты өңдеу\n\n"
            "👇 Төлем жасау:"
        ),
        "tolov_malumot": (
            "💳 Төлем деректері:\n\n"
            "💰 Сома: {:,} сум\n"
            "🏦 Карта: <code>{}</code>\n"
            "👤 Иесі: {}\n\n"
            "📌 Төлемнен кейін:\n"
            "1️⃣ Чекті (скриншот) ботқа жіберіңіз\n"
            "2️⃣ Әкімші тексеріп Premium береді\n"
            "⏳ Растау: 1-24 сағат\n\n"
            "❗ Түсініктемеге ID жазыңыз: <code>{}</code>"
        ),
        "chek_qabul": "✅ Чегіңіз қабылданды!\n⏳ Әкімші тексеріп жауап береді.",
        "chek_kutilmoqda": "⏳ Алдыңғы төлеміңіз қаралуда. Күтіңіз!",
        "holat": (
            "📊 Аккаунтыңыз:\n\n"
            "👤 Аты: {}\n"
            "🆔 ID: {}\n"
            "⭐ Жазылым: {}\n"
            "📅 Premium мерзімі: {}\n"
            "📸 Бүгін: {} дана\n"
            "🔢 Қалды: {} дана\n"
            "🖼 Барлығы: {} дана\n"
            "👥 Рефералдар: {} адам → {} бонус сурет"
        ),
        "premium_label": "Premium ✅",
        "oddiy_label": "Тегін",
        "blok": "🚫 Сіз ботта бұғатталғансыз.",
        "premium_kerak": "🔒 Бұл сапа тек Premium үшін!\n\n⭐ Premium: {:,} сум/ай\n✅ 4K + күніне 30 сурет",
        "referral_matn": (
            "👥 Реферал жүйесі:\n\n"
            "🔗 Сіздің сілтемеңіз:\n{}\n\n"
            "✅ Әр жаңа қолданушы үшін +1 тегін сурет!\n"
            "📊 Шақырылды: {} адам\n"
            "🎁 Алынған бонус: {} сурет\n"
            "💰 Бонус қалдығы: {} сурет"
        ),
        "bonus_xabar": "🎁 Реферал бонус: +1 сурет қосылды! (досыңыз қосылды)",
        "yangi_foydalanuvchi_ref": "🎉 Қош келдіңіз! Сіз {} шақыруы арқылы келдіңіз.",
        "xato": "❌ Қате: {}",
        "vaqt_tugadi": "⌛ Уақыт бітті. Қайта көріңіз!",
    },
}

SIFATLAR = {
    "144p":  {"scale": 2, "label": "🔹 144p  — tez/быстро/fast",   "premium": False},
    "720p":  {"scale": 4, "label": "🔷 720p  — yaxshi/хорошо/good","premium": False},
    "1080p": {"scale": 6, "label": "🔶 1080p — yuqori/высокое/high","premium": False},
    "4K":    {"scale": 8, "label": "💎 4K    — maksimal ⭐",        "premium": True},
}

# ═══════════════════════════════════════════
#   DATABASE
# ═══════════════════════════════════════════
DB_FAYL = "database.json"

def db_yukla():
    if os.path.exists(DB_FAYL):
        with open(DB_FAYL, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"users": {}, "pending_payments": {}, "blocked": []}

def db_sayla(data):
    with open(DB_FAYL, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def user_get(user_id: int) -> dict:
    db  = db_yukla()
    uid = str(user_id)
    if uid not in db["users"]:
        db["users"][uid] = {
            "id": user_id, "ism": "", "username": "",
            "til": "uz",
            "premium": False, "premium_tugash": None,
            "bugun_soni": 0, "sana": str(date.today()),
            "jami_rasm": 0,
            "bonus_rasm": 0,
            "referral_soni": 0, "referral_jami_bonus": 0,
            "ref_by": None,
            "qoshilgan": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        db_sayla(db)
    u = db["users"][uid]
    if u.get("sana") != str(date.today()):
        u["bugun_soni"] = 0
        u["sana"] = str(date.today())
        db["users"][uid] = u
        db_sayla(db)
    return db["users"][uid]

def user_yangi(user_id: int, **kwargs):
    db  = db_yukla()
    uid = str(user_id)
    user_get(user_id)
    db["users"][uid].update(kwargs)
    db_sayla(db)

def t(user_id: int, kalit: str) -> str:
    u   = user_get(user_id)
    til = u.get("til", "uz")
    return TILLAR.get(til, TILLAR["uz"]).get(kalit, kalit)

def premium_tekshir(user_id: int) -> bool:
    u = user_get(user_id)
    if not u.get("premium"):
        return False
    tugash = u.get("premium_tugash")
    if tugash and datetime.strptime(tugash, "%Y-%m-%d") < datetime.now():
        user_yangi(user_id, premium=False, premium_tugash=None)
        return False
    return True

def limit_tekshir(user_id: int) -> tuple:
    u      = user_get(user_id)
    limit  = PREMIUM_LIMIT if premium_tekshir(user_id) else BEPUL_LIMIT
    bonus  = u.get("bonus_rasm", 0)
    ishlatilgan = u.get("bugun_soni", 0)
    qoldi  = (limit + bonus) - ishlatilgan
    return qoldi > 0, max(0, qoldi)

def bloklangan_mi(user_id: int) -> bool:
    db = db_yukla()
    return user_id in db.get("blocked", [])

logging.basicConfig(format="%(asctime)s | %(levelname)s | %(message)s", level=logging.INFO)
log = logging.getLogger(__name__)
kutish = {}

async def admin_xabar(ctx, matn: str):
    try:
        await ctx.bot.send_message(chat_id=ADMIN_ID, text=matn)
    except Exception as e:
        log.error(f"Admin xabar xato: {e}")

def foydalanuvchi_sayla(update: Update):
    u = update.effective_user
    user_yangi(u.id, ism=u.full_name,
               username=f"@{u.username}" if u.username else "—")

# ═══════════════════════════════════════════
#   /start — referral qo'llab-quvvatlash
# ═══════════════════════════════════════════
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    foydalanuvchi_sayla(update)
    user_id = update.effective_user.id

    if bloklangan_mi(user_id):
        await update.message.reply_text(t(user_id, "blok"))
        return

    # Referral aniqlash: /start ref_123456
    args = ctx.args
    if args and args[0].startswith("ref_"):
        try:
            ref_id = int(args[0].replace("ref_", ""))
            u      = user_get(user_id)
            if ref_id != user_id and not u.get("ref_by"):
                # Referral bonus — taklif qilganga +1 bonus rasm
                ref_u = user_get(ref_id)
                user_yangi(ref_id,
                    referral_soni=ref_u.get("referral_soni", 0) + 1,
                    referral_jami_bonus=ref_u.get("referral_jami_bonus", 0) + 1,
                    bonus_rasm=ref_u.get("bonus_rasm", 0) + 1
                )
                user_yangi(user_id, ref_by=ref_id)
                try:
                    await ctx.bot.send_message(
                        chat_id=ref_id,
                        text=t(ref_id, "bonus_xabar")
                    )
                except:
                    pass
                ref_ism = ref_u.get("ism", "—")
                await update.message.reply_text(
                    t(user_id, "yangi_foydalanuvchi_ref").format(ref_ism)
                )
        except:
            pass

    # Til tanlash — yangi foydalanuvchi uchun
    u = user_get(user_id)
    if not u.get("til_tanlangan"):
        await til_tanlash_yuborish(update, user_id)
        return

    await update.message.reply_text(t(user_id, "xush_kelibsiz"))

async def til_tanlash_yuborish(update, user_id):
    tugmalar = [
        [InlineKeyboardButton(v["til_nomi"], callback_data=f"til_{k}")]
        for k, v in TILLAR.items()
    ]
    await update.message.reply_text(
        "🌐 Choose your language / Tilni tanlang / Выберите язык / Тілді таңдаңыз:",
        reply_markup=InlineKeyboardMarkup(tugmalar)
    )

# ═══════════════════════════════════════════
#   /til — til o'zgartirish
# ═══════════════════════════════════════════
async def til_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if bloklangan_mi(user_id):
        return
    tugmalar = [
        [InlineKeyboardButton(v["til_nomi"], callback_data=f"til_{k}")]
        for k, v in TILLAR.items()
    ]
    await update.message.reply_text(
        t(user_id, "til_tanlang"),
        reply_markup=InlineKeyboardMarkup(tugmalar)
    )

# ═══════════════════════════════════════════
#   /holat
# ═══════════════════════════════════════════
async def holat(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    foydalanuvchi_sayla(update)
    user_id = update.effective_user.id
    if bloklangan_mi(user_id):
        await update.message.reply_text(t(user_id, "blok"))
        return
    u         = user_get(user_id)
    is_prem   = premium_tekshir(user_id)
    _, qoldi  = limit_tekshir(user_id)
    await update.message.reply_text(
        t(user_id, "holat").format(
            u.get("ism","—"), user_id,
            t(user_id, "premium_label") if is_prem else t(user_id, "oddiy_label"),
            u.get("premium_tugash","—"),
            u.get("bugun_soni", 0), qoldi,
            u.get("jami_rasm", 0),
            u.get("referral_soni", 0),
            u.get("referral_jami_bonus", 0)
        )
    )

# ═══════════════════════════════════════════
#   /referral
# ═══════════════════════════════════════════
async def referral(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    foydalanuvchi_sayla(update)
    user_id  = update.effective_user.id
    if bloklangan_mi(user_id):
        return
    bot_info = await ctx.bot.get_me()
    havola   = f"https://t.me/{bot_info.username}?start=ref_{user_id}"
    u        = user_get(user_id)
    await update.message.reply_text(
        t(user_id, "referral_matn").format(
            havola,
            u.get("referral_soni", 0),
            u.get("referral_jami_bonus", 0),
            u.get("bonus_rasm", 0)
        )
    )

# ═══════════════════════════════════════════
#   /premium
# ═══════════════════════════════════════════
async def premium_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    foydalanuvchi_sayla(update)
    user_id = update.effective_user.id
    if bloklangan_mi(user_id):
        return
    if premium_tekshir(user_id):
        u = user_get(user_id)
        await update.message.reply_text(
            t(user_id, "premium_mavjud").format(u.get("premium_tugash","—"))
        )
        return
    tugmalar = [[InlineKeyboardButton(
        t(user_id, "premium_tugma"), callback_data="tolov_boshlash"
    )]]
    await update.message.reply_text(
        t(user_id, "premium_taklif").format(PREMIUM_NARX),
        reply_markup=InlineKeyboardMarkup(tugmalar)
    )

# ═══════════════════════════════════════════
#   RASM KELDI
# ═══════════════════════════════════════════
async def rasm_keldi(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    foydalanuvchi_sayla(update)
    user_id = update.effective_user.id

    if bloklangan_mi(user_id):
        await update.message.reply_text(t(user_id, "blok"))
        return

    # Til tanlanmagan bo'lsa
    u = user_get(user_id)
    if not u.get("til_tanlangan"):
        await til_tanlash_yuborish(update, user_id)
        return

    o_tdi, qoldi = limit_tekshir(user_id)
    if not o_tdi:
        is_prem = premium_tekshir(user_id)
        if is_prem:
            await update.message.reply_text(t(user_id, "limit_tugadi_premium"))
        else:
            tugmalar = [[InlineKeyboardButton(
                t(user_id, "premium_tugma"), callback_data="tolov_boshlash"
            )]]
            await update.message.reply_text(
                t(user_id, "limit_tugadi_bepul").format(BEPUL_LIMIT, PREMIUM_NARX),
                reply_markup=InlineKeyboardMarkup(tugmalar)
            )
        return

    msg   = await update.message.reply_text(
        t(user_id, "rasm_qabul") + t(user_id, "qoldi").format(qoldi)
    )
    photo = update.message.photo[-1]
    file  = await ctx.bot.get_file(photo.file_id)
    buf   = io.BytesIO()
    await file.download_to_memory(buf)
    kutish[user_id] = buf.getvalue()

    is_prem  = premium_tekshir(user_id)
    tugmalar = []
    for k, v in SIFATLAR.items():
        if v["premium"] and not is_prem:
            tugmalar.append([InlineKeyboardButton(
                f"🔒 {v['label']}", callback_data=f"premium_kerak_{k}"
            )])
        else:
            tugmalar.append([InlineKeyboardButton(v["label"], callback_data=k)])

    await msg.delete()
    await update.message.reply_text(
        t(user_id, "rasm_qabul") + t(user_id, "sifat_tanlang"),
        reply_markup=InlineKeyboardMarkup(tugmalar)
    )

# ═══════════════════════════════════════════
#   CALLBACK HANDLER
# ═══════════════════════════════════════════
async def callback_handler(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query   = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    amal    = query.data

    # ── Til tanlash ──
    if amal.startswith("til_"):
        til = amal.replace("til_", "")
        user_yangi(user_id, til=til, til_tanlangan=True)
        til_ism = TILLAR[til]["til_nomi"]
        await query.edit_message_text(f"✅ {til_ism}")
        await ctx.bot.send_message(
            chat_id=query.message.chat_id,
            text=t(user_id, "xush_kelibsiz")
        )
        return

    # ── To'lov boshlash ──
    if amal == "tolov_boshlash":
        await query.edit_message_text(
            t(user_id, "tolov_malumot").format(
                PREMIUM_NARX, KARTA_RAQAM, KARTA_EGASI, user_id
            ),
            parse_mode="HTML"
        )
        return

    # ── Premium kerak ──
    if amal.startswith("premium_kerak_"):
        tugmalar = [[InlineKeyboardButton(
            t(user_id, "premium_tugma"), callback_data="tolov_boshlash"
        )]]
        await query.edit_message_text(
            t(user_id, "premium_kerak").format(PREMIUM_NARX),
            reply_markup=InlineKeyboardMarkup(tugmalar)
        )
        return

    # ── Admin callback ──
    if amal.startswith("admin_"):
        await admin_callback_ichki(query, ctx)
        return

    # ── Sifat tanlash ──
    if amal not in SIFATLAR:
        return

    sifat = amal
    if user_id not in kutish:
        await query.edit_message_text("⚠️ Avval rasm yuboring!")
        return

    o_tdi, _ = limit_tekshir(user_id)
    if not o_tdi:
        await query.edit_message_text(t(user_id, "limit_tugadi_premium"))
        return

    if SIFATLAR[sifat]["premium"] and not premium_tekshir(user_id):
        tugmalar = [[InlineKeyboardButton(
            t(user_id, "premium_tugma"), callback_data="tolov_boshlash"
        )]]
        await query.edit_message_text(
            t(user_id, "premium_kerak").format(PREMIUM_NARX),
            reply_markup=InlineKeyboardMarkup(tugmalar)
        )
        return

    rasm_bytes = kutish.pop(user_id)
    scale      = SIFATLAR[sifat]["scale"]
    await query.edit_message_text(t(user_id, "jarayon").format(sifat))

    try:
        # Picwish API — scale max 4x
        picwish_scale = min(scale, 4)
        log.info(f"Picwish ga yuborilmoqda | sifat={sifat} scale={picwish_scale}")

        # 1. Task yaratish
        resp = requests.post(
            PICWISH_CREATE_URL,
            headers={"X-API-KEY": PICWISH_KEY},
            files={"image_file": ("rasm.jpg", rasm_bytes, "image/jpeg")},
            data={"sync": 0, "scale": picwish_scale},
            timeout=60
        )
        resp.raise_for_status()
        javob = resp.json()

        if javob.get("status") != 200:
            await query.edit_message_text(
                t(user_id, "xato").format(javob.get("message", str(javob)))
            )
            return

        task_id = javob["data"]["task_id"]

        # 2. Natijani polling bilan kutamiz
        for _ in range(30):
            time.sleep(2)
            tekshir = requests.get(
                PICWISH_RESULT_URL.format(task_id=task_id),
                headers={"X-API-KEY": PICWISH_KEY},
                timeout=30
            )
            tekshir.raise_for_status()
            holat = tekshir.json()
            if holat.get("status") != 200:
                continue
            state = holat["data"].get("state", 0)
            if state == 1:
                natija_url = holat["data"].get("image")
                r = requests.get(natija_url, timeout=60)
                u = user_get(user_id)
                bonus       = u.get("bonus_rasm", 0)
                limit       = PREMIUM_LIMIT if premium_tekshir(user_id) else BEPUL_LIMIT
                ishlatilgan = u.get("bugun_soni", 0)
                if ishlatilgan >= limit and bonus > 0:
                    user_yangi(user_id, bonus_rasm=bonus - 1)
                user_yangi(user_id,
                    bugun_soni=u.get("bugun_soni", 0) + 1,
                    jami_rasm=u.get("jami_rasm", 0) + 1
                )
                _, qoldi = limit_tekshir(user_id)
                await ctx.bot.send_photo(
                    chat_id=query.message.chat_id,
                    photo=io.BytesIO(r.content),
                    caption=t(user_id, "tayyor").format(sifat, BOT_USERNAME, qoldi)
                )
                await query.edit_message_text(f"✅ {sifat} — OK!")
                return
            elif state < 0:
                await query.edit_message_text(t(user_id, "xato").format("ishlov berish xato"))
                return

        await query.edit_message_text(t(user_id, "vaqt_tugadi"))

    except requests.HTTPError as e:
        await query.edit_message_text(t(user_id, "xato").format(e.response.status_code))
    except Exception as e:
        log.error(f"Xato: {e}")
        await query.edit_message_text(t(user_id, "xato").format(str(e)))


# ═══════════════════════════════════════════
#   CHEK KELDI (to'lov tasdiqlash)
# ═══════════════════════════════════════════
async def chek_keldi(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    foydalanuvchi_sayla(update)
    user_id = update.effective_user.id
    if bloklangan_mi(user_id):
        return
    if not update.message.photo and not update.message.document:
        return

    db  = db_yukla()
    uid = str(user_id)
    u   = user_get(user_id)

    if uid in db.get("pending_payments", {}):
        await update.message.reply_text(t(user_id, "chek_kutilmoqda"))
        return

    photo = update.message.photo
    doc   = update.message.document
    fid   = photo[-1].file_id if photo else doc.file_id

    db["pending_payments"][uid] = {
        "user_id": user_id, "ism": u.get("ism","—"),
        "username": u.get("username","—"),
        "vaqt": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "file_id": fid
    }
    db_sayla(db)

    await update.message.reply_text(t(user_id, "chek_qabul"))
    await admin_xabar(ctx,
        f"💳 YANGI TO'LOV!\n\n"
        f"👤 {u.get('ism','—')} | {u.get('username','—')}\n"
        f"🆔 {user_id}\n"
        f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        f"✅ Tasdiqlash: /premium_ber_{user_id}\n"
        f"❌ Rad etish: /premium_rad_{user_id}"
    )


# ═══════════════════════════════════════════
#   ADMIN PANEL
# ═══════════════════════════════════════════
async def admin_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    await admin_panel_yuborish(update.message, ctx)

async def admin_panel_yuborish(message, ctx):
    db    = db_yukla()
    users = db.get("users", {})
    tugmalar = [
        [InlineKeyboardButton("👥 Foydalanuvchilar", callback_data="admin_users")],
        [InlineKeyboardButton("⭐ Premium lar",       callback_data="admin_premiums")],
        [InlineKeyboardButton("💳 Kutayotgan to'lovlar", callback_data="admin_pending")],
        [InlineKeyboardButton("🚫 Bloklangan lar",    callback_data="admin_blocked")],
        [InlineKeyboardButton("📢 Hammaga xabar",     callback_data="admin_broadcast")],
        [InlineKeyboardButton("📊 Statistika",        callback_data="admin_stat")],
    ]
    await message.reply_text(
        f"🔐 ADMIN PANEL\n\n"
        f"👥 Jami: {len(users)}\n"
        f"⭐ Premium: {sum(1 for u in users.values() if u.get('premium'))}\n"
        f"🚫 Bloklangan: {len(db.get('blocked', []))}\n"
        f"💳 Kutayotgan to'lov: {len(db.get('pending_payments', {}))}\n"
        f"📸 Bugun: {sum(u.get('bugun_soni',0) for u in users.values())}",
        reply_markup=InlineKeyboardMarkup(tugmalar)
    )

async def admin_callback_ichki(query, ctx):
    if query.from_user.id != ADMIN_ID:
        await query.answer("❌ Ruxsat yo'q!")
        return
    db   = db_yukla()
    amal = query.data
    orqa = InlineKeyboardMarkup([[InlineKeyboardButton("◀️ Orqaga", callback_data="admin_back")]])

    if amal == "admin_stat":
        users     = db.get("users", {})
        jami_rasm = sum(u.get("jami_rasm", 0) for u in users.values())
        bugun     = sum(u.get("bugun_soni", 0) for u in users.values())
        reflar    = sum(u.get("referral_soni", 0) for u in users.values())
        await query.edit_message_text(
            f"📊 STATISTIKA:\n\n"
            f"👥 Jami foydalanuvchi: {len(users)}\n"
            f"⭐ Premium: {sum(1 for u in users.values() if u.get('premium'))}\n"
            f"🖼 Jami rasm: {jami_rasm}\n"
            f"📸 Bugun: {bugun}\n"
            f"👥 Jami referral: {reflar}",
            reply_markup=orqa
        )

    elif amal == "admin_users":
        users = db.get("users", {})
        matn  = f"👥 FOYDALANUVCHILAR ({len(users)} ta):\n\n"
        for u in list(users.values())[-20:]:
            e = "⭐" if u.get("premium") else "👤"
            matn += f"{e} {u.get('ism','—')} | {u.get('username','—')} | {u['id']}\n"
        await query.edit_message_text(matn[:4000], reply_markup=orqa)

    elif amal == "admin_premiums":
        prems = [u for u in db.get("users", {}).values() if u.get("premium")]
        matn  = f"⭐ PREMIUM ({len(prems)} ta):\n\n"
        for u in prems:
            matn += f"• {u.get('ism','—')} | {u['id']} | {u.get('premium_tugash','—')}\n"
        if not prems:
            matn += "Yo'q."
        await query.edit_message_text(matn[:4000], reply_markup=orqa)

    elif amal == "admin_pending":
        pending = db.get("pending_payments", {})
        if not pending:
            await query.edit_message_text("💳 Kutayotgan to'lov yo'q.", reply_markup=orqa)
            return
        matn = f"💳 KUTAYOTGAN ({len(pending)} ta):\n\n"
        for p in pending.values():
            matn += (
                f"👤 {p.get('ism','—')} | {p.get('username','—')}\n"
                f"🆔 {p['user_id']} | {p.get('vaqt','—')}\n"
                f"✅ /premium_ber_{p['user_id']}\n"
                f"❌ /premium_rad_{p['user_id']}\n\n"
            )
        await query.edit_message_text(matn[:4000], reply_markup=orqa)

    elif amal == "admin_blocked":
        blocked = db.get("blocked", [])
        matn    = f"🚫 BLOKLANGAN ({len(blocked)} ta):\n\n"
        for bid in blocked:
            u    = db["users"].get(str(bid), {})
            matn += f"• {u.get('ism','—')} | {bid} | /blok_ochish_{bid}\n"
        if not blocked:
            matn += "Yo'q."
        await query.edit_message_text(matn[:4000], reply_markup=orqa)

    elif amal == "admin_broadcast":
        ctx.bot_data["broadcast_mode"] = True
        await query.edit_message_text(
            "📢 Hammaga yuboriladigan xabarni yozing:\n(Bekor: /admin)"
        )

    elif amal == "admin_back":
        db    = db_yukla()
        users = db.get("users", {})
        tugmalar = [
            [InlineKeyboardButton("👥 Foydalanuvchilar",     callback_data="admin_users")],
            [InlineKeyboardButton("⭐ Premium lar",           callback_data="admin_premiums")],
            [InlineKeyboardButton("💳 Kutayotgan to'lovlar", callback_data="admin_pending")],
            [InlineKeyboardButton("🚫 Bloklangan lar",       callback_data="admin_blocked")],
            [InlineKeyboardButton("📢 Hammaga xabar",        callback_data="admin_broadcast")],
            [InlineKeyboardButton("📊 Statistika",           callback_data="admin_stat")],
        ]
        await query.edit_message_text(
            f"🔐 ADMIN PANEL\n\n"
            f"👥 Jami: {len(users)}\n"
            f"⭐ Premium: {sum(1 for u in users.values() if u.get('premium'))}\n"
            f"🚫 Bloklangan: {len(db.get('blocked', []))}\n"
            f"💳 Kutayotgan: {len(db.get('pending_payments', {}))}",
            reply_markup=InlineKeyboardMarkup(tugmalar)
        )

# ═══════════════════════════════════════════
#   ADMIN MATN BUYRUQLARI
# ═══════════════════════════════════════════
async def admin_matn(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    matn = update.message.text.strip()
    db   = db_yukla()

    # Broadcast
    if ctx.bot_data.get("broadcast_mode"):
        ctx.bot_data["broadcast_mode"] = False
        users     = db.get("users", {})
        yuborildi = 0
        xato      = 0
        for uid in users:
            try:
                await ctx.bot.send_message(chat_id=int(uid), text=matn)
                yuborildi += 1
                time.sleep(0.05)
            except:
                xato += 1
        await update.message.reply_text(
            f"📢 Yuborildi!\n✅ {yuborildi}\n❌ {xato}"
        )
        return

    if matn.startswith("/premium_ber_"):
        try:
            uid = int(matn.split("_")[-1])
        except:
            await update.message.reply_text("❌ ID noto'g'ri")
            return
        tugash = (datetime.now() + timedelta(days=PREMIUM_KUN)).strftime("%Y-%m-%d")
        user_yangi(uid, premium=True, premium_tugash=tugash)
        db = db_yukla()
        db["pending_payments"].pop(str(uid), None)
        db_sayla(db)
        await update.message.reply_text(f"✅ {uid} ga Premium berildi! ({tugash} gacha)")
        try:
            await ctx.bot.send_message(
                chat_id=uid,
                text=(
                    f"🎉 Premium berildi!\n"
                    f"📅 {PREMIUM_KUN} kun ({tugash} gacha)\n"
                    f"💎 4K va 30 ta/kun ishlata olasiz!"
                )
            )
        except:
            pass

    elif matn.startswith("/premium_rad_"):
        try:
            uid = int(matn.split("_")[-1])
        except:
            await update.message.reply_text("❌ ID noto'g'ri")
            return
        db["pending_payments"].pop(str(uid), None)
        db_sayla(db)
        await update.message.reply_text(f"❌ {uid} rad etildi.")
        try:
            await ctx.bot.send_message(chat_id=uid,
                text="❌ To'lovingiz tasdiqlanmadi. Muammo bo'lsa admin bilan bog'laning.")
        except:
            pass

    elif matn.startswith("/blok_ochish_"):
        try:
            uid = int(matn.split("_")[-1])
        except:
            await update.message.reply_text("❌ ID noto'g'ri")
            return
        blocked = db.get("blocked", [])
        if uid in blocked:
            blocked.remove(uid)
            db["blocked"] = blocked
            db_sayla(db)
        await update.message.reply_text(f"✅ {uid} blokdan chiqarildi!")

    elif matn.startswith("/blok_"):
        try:
            uid = int(matn.replace("/blok_", "").split("_")[0])
        except:
            await update.message.reply_text("❌ ID noto'g'ri")
            return
        db.setdefault("blocked", [])
        if uid not in db["blocked"]:
            db["blocked"].append(uid)
            db_sayla(db)
        await update.message.reply_text(f"🚫 {uid} bloklandi!")

    elif matn.startswith("/bonus_"):
        # /bonus_USER_ID_SONI — qo'lda bonus berish
        parts = matn.replace("/bonus_", "").split("_")
        try:
            uid  = int(parts[0])
            soni = int(parts[1])
        except:
            await update.message.reply_text("Format: /bonus_USER_ID_SONI")
            return
        u = user_get(uid)
        user_yangi(uid, bonus_rasm=u.get("bonus_rasm", 0) + soni)
        await update.message.reply_text(f"✅ {uid} ga {soni} ta bonus rasm berildi!")

# ═══════════════════════════════════════════
#   ISHGA TUSHIRISH
# ═══════════════════════════════════════════
def main():
    if "BU_YERGA" in BOT_TOKEN or "BU_YERGA" in PICWISH_KEY:
        print("=" * 55)
        print("  ⚠️  SOZLAMALARNI TO'LDIRING:")
        print("  BOT_TOKEN, PICWISH_KEY,")
        print("  KARTA_RAQAM, KARTA_EGASI")
        print("=" * 55)
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start",    start))
    app.add_handler(CommandHandler("holat",    holat))
    app.add_handler(CommandHandler("premium",  premium_cmd))
    app.add_handler(CommandHandler("referral", referral))
    app.add_handler(CommandHandler("til",      til_cmd))
    app.add_handler(CommandHandler("admin",    admin_cmd))

    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(MessageHandler(filters.PHOTO & ~filters.User(ADMIN_ID), rasm_keldi))

    # Admin uchun: rasm = chek, matn = buyruq
    app.add_handler(MessageHandler(filters.PHOTO & filters.User(ADMIN_ID), chek_ham_rasm))
    app.add_handler(MessageHandler(filters.TEXT & filters.User(ADMIN_ID), admin_matn))
    # Oddiy foydalanuvchi cheki
    app.add_handler(MessageHandler(
        (filters.PHOTO | filters.Document.ALL) & ~filters.User(ADMIN_ID),
        chek_keldi
    ))

    print(f"✅ Bot ishga tushdi! Admin: {ADMIN_ID}")
    print("   To'xtatish: Ctrl+C")
    app.run_polling()

async def chek_ham_rasm(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    """Admin rasm yuborsa — admin panelga yo'naltirish"""
    await admin_cmd(update, ctx)

if __name__ == "__main__":
    main()