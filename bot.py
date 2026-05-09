from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = "8732837294:AAFyQ6069wbi3UvH8Jm7kCM6SJKxuLgq8Gs"

DOLLAR = 12500

user_data = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🪟 Plastmassa Profil", callback_data="plast"),
            InlineKeyboardButton("🔩 Alyuminiy Profil", callback_data="alyum"),
        ],
        [
            InlineKeyboardButton("⚡ Tezkor Hisob-kitob", callback_data="fast"),
        ],
        [
            InlineKeyboardButton("📞 Biz bilan bog'lanish", callback_data="contact"),
        ],
    ]

    text = (
        "Assalomu Aleykum!\n\n"
        "Men Arka tayyorlashga kerak bo'ladigan profil uzunligi va narxini "
        "hisoblab beruvchi botman.\n\n"
        "Kerakli bo'limni tanlang 👇"
    )

    await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if query.data == "home":
        keyboard = [
            [
                InlineKeyboardButton("🪟 Plastmassa Profil", callback_data="plast"),
                InlineKeyboardButton("🔩 Alyuminiy Profil", callback_data="alyum"),
            ],
            [
                InlineKeyboardButton("⚡ Tezkor Hisob-kitob", callback_data="fast"),
            ],
            [
                InlineKeyboardButton("📞 Biz bilan bog'lanish", callback_data="contact"),
            ],
        ]

        await query.message.reply_text(
            "🏠 Bosh menyu",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif query.data == "contact":
        keyboard = [
            [
                InlineKeyboardButton("⬅️ Orqaga", callback_data="home"),
            ]
        ]

        await query.message.reply_text(
            "📞 Biz bilan bog'lanish uchun:\n\n"
            "+998997194009\n"
            "+998912404009\n\n"
            "Telegram yoki telefon orqali murojaat qilishingiz mumkin.",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif query.data == "plast":
        user_data[user_id] = {
            "type": "plast",
            "step": "length",
            "price": 4,
            "extra": 25,
        }

        keyboard = [
            [
                InlineKeyboardButton("🏠 Bosh menyu", callback_data="home"),
            ]
        ]

        await query.message.reply_text(
            "🪟 Plastmassa Profil\n\n"
            "Arka uzunligini kiriting.\n"
            "Masalan: 3.75",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif query.data == "alyum":
        user_data[user_id] = {
            "type": "alyum",
            "step": "length",
            "price": 3,
            "extra": 40,
        }

        keyboard = [
            [
                InlineKeyboardButton("🏠 Bosh menyu", callback_data="home"),
            ]
        ]

        await query.message.reply_text(
            "🔩 Alyuminiy Profil\n\n"
            "Arka uzunligini kiriting.\n"
            "Masalan: 3.75",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif query.data == "fast":
        user_data[user_id] = {
            "type": "fast",
            "step": "fast_length",
        }

        keyboard = [
            [
                InlineKeyboardButton("🏠 Bosh menyu", callback_data="home"),
            ]
        ]

        await query.message.reply_text(
            "⚡ Tezkor Hisob-kitob\n\n"
            "Arka uzunligini kiriting.\n"
            "Masalan: 3.75",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )


async def messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id not in user_data:
        return

    text = update.message.text

    try:
        number = float(text.replace(",", "."))
    except:
        await update.message.reply_text("❌ Faqat son kiriting.")
        return

    data = user_data[user_id]

    # PLAST / ALYUM
    if data["step"] == "length":
        length = number

        one_dollar = length * data["price"]
        one_sum = one_dollar * DOLLAR

        keyboard = [
            [
                InlineKeyboardButton("🏠 Bosh menyu", callback_data="home"),
            ]
        ]

        profil = "🪟 Plastmassa" if data["type"] == "plast" else "🔩 Alyuminiy"

        await update.message.reply_text(
            f"{profil} Profil\n\n"
            f"📏 Uzunlik: {length} metr\n\n"
            f"💵 1 metr narxi: {data['price']}$\n"
            f"💰 Dollar kursi: {DOLLAR} so'm\n\n"
            f"💲 Jami: {one_dollar}$\n"
            f"💸 So'mda: {int(one_sum):,} so'm",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

        del user_data[user_id]

    # FAST STEP 1
    elif data["step"] == "fast_length":
        data["length"] = number
        data["step"] = "fast_price"

        await update.message.reply_text(
            "💵 1 metr uchun narx kiriting.\n\n"
            "Masalan:\n"
            "3\n"
            "4\n"
            "13000"
        )

    # FAST STEP 2
    elif data["step"] == "fast_price":
        data["price"] = number
        data["step"] = "fast_count"

        await update.message.reply_text(
            "🔢 Nechta arka borligini kiriting."
        )

    # FAST STEP 3
    elif data["step"] == "fast_count":
        count = int(number)

        length = data["length"]
        price = data["price"]

        one = length * price
        total = one * count

        if price < 100:
            one_sum = one * DOLLAR
            total_sum = total * DOLLAR

            result = (
                f"⚡ Tezkor Hisob-kitob\n\n"
                f"📏 Uzunlik: {length} metr\n"
                f"💵 1 metr narxi: {price}$\n"
                f"🔢 Soni: {count} ta\n\n"
                f"📦 1 donasi: {one}$\n"
                f"📦 {count} donasi: {total}$\n\n"
                f"💸 So'mda:\n"
                f"{int(total_sum):,} so'm"
            )

        else:
            result = (
                f"⚡ Tezkor Hisob-kitob\n\n"
                f"📏 Uzunlik: {length} metr\n"
                f"💵 1 metr narxi: {price:,} so'm\n"
                f"🔢 Soni: {count} ta\n\n"
                f"📦 1 donasi: {int(one):,} so'm\n"
                f"📦 {count} donasi: {int(total):,} so'm"
            )

        keyboard = [
            [
                InlineKeyboardButton("🏠 Bosh menyu", callback_data="home"),
            ]
        ]

        await update.message.reply_text(
            result,
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

        del user_data[user_id]


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, messages))

    print("Bot ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()
