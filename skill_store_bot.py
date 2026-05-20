from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

TOKEN = '8817568211:AAEuq4B3fvS0ja1piEZre7sMkOfjKbU_K9M'


ADMIN_ID = 8491750678



users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
أهلاً وسهلاً بك في متجر سكوير ستور الإلكتروني 🎮

أرسل المعلومات التالية:

• رقم الطلب
• اسم الحساب
• منصة الجهاز
"""
    await update.message.reply_text(text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    users[user.id] = update.message.text

    keyboard = [
        [
            InlineKeyboardButton("✅ معلومات صحيحة", callback_data=f"yes_{user.id}"),
            InlineKeyboardButton("❌ معلومات خاطئة", callback_data=f"no_{user.id}")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    text = f"""
طلب جديد 🔔

اسم العميل:
{user.full_name}

يوزر العميل:
@{user.username}

المعلومات:
{update.message.text}
"""

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=text,
        reply_markup=reply_markup
    )

    await update.message.reply_text("⏳ جاري التحقق من المعلومات...")

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data.startswith("yes_"):
        user_id = int(data.split("_")[1])

        users[user_id] = True

        await context.bot.send_message(
            chat_id=user_id,
            text="""
تم التحقق من المعلومات ✅

قم بتسجيل الدخول،
وراح يتم إعطاؤك الرمز خلال 5 دقائق كحد أقصى يا غالي 🌹
"""
        )

        await query.message.reply_text(
            f"ارسل الرمز للعميل:\n/usercode {user_id} الرمز"
        )

    elif data.startswith("no_"):
        user_id = int(data.split("_")[1])

        keyboard = [
            [
                InlineKeyboardButton(
                    "📞 تواصل واتساب",
                    url="https://wa.me/966575700277"
                )
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await context.bot.send_message(
            chat_id=user_id,
            text="""
يا غالي المعلومات اللي أرسلتها غير صحيحة ❌

إذا أنت متأكد أو فيه خطأ بسيط،
تواصل معنا واتساب 👇
""",
            reply_markup=reply_markup
        )

async def usercode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    try:
        user_id = int(context.args[0])

        code = " ".join(context.args[1:])

        await context.bot.send_message(
            chat_id=user_id,
            text=f"🔐 الرمز:\n\n{code}"
        )

        await update.message.reply_text("تم إرسال الرمز ✅")

    except:
        await update.message.reply_text("خطأ")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("usercode", usercode))
app.add_handler(CallbackQueryHandler(buttons))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("البوت شغال 🔥")

app.run_polling()
