import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters
)
import yt_dlp

TOKEN = "8175731761:AAGNViWN41PeN_XZmkJomV7lMpbr3zeOj14"
ADMIN_ID = 5994435969

# Til sozlamalari
LANGUAGES = {
    "🇺🇿 O'zbek": "uz",
    "🇷🇺 Русский": "ru",
    "🇬🇧 English": "en"
}

MESSAGES = {
    "send_instagram": {
        "uz": "Instagram havolasini yuboring.",
        "ru": "Отправьте ссылку Instagram.",
        "en": "Send the Instagram link."
    },
    "error": {
        "uz": "❌ Xatolik yuz berdi.",
        "ru": "❌ Произошла ошибка.",
        "en": "❌ An error occurred."
    },
    "admin_panel": {
        "uz": "👑 Siz admin paneldasiz.",
        "ru": "👑 Вы в админ-панели.",
        "en": "👑 You are in the admin panel."
    }
}

# Video yuklab olish
def download_instagram_video(url):
    ydl_opts = {
        'outtmpl': 'video.%(ext)s',
        'format': 'mp4',
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[lang] for lang in LANGUAGES.keys()]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Tilni tanlang / Выберите язык / Select language:", reply_markup=markup)

# Til tanlash
async def handle_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang_key = update.message.text
    if lang_key in LANGUAGES:
        context.user_data["lang"] = LANGUAGES[lang_key]
        lang_code = context.user_data["lang"]
        if update.effective_user.id == ADMIN_ID:
            await update.message.reply_text(MESSAGES["admin_panel"][lang_code])
        else:
            await update.message.reply_text(MESSAGES["send_instagram"][lang_code])
        return

    await handle_message(update, context)  # Aks holda oddiy xabarga o'tkazadi

# Asosiy handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    lang_code = context.user_data.get("lang", "uz")

    if "instagram.com" in text:
        await update.message.reply_text("⌛")
        try:
            filepath = download_instagram_video(text)
            await update.message.reply_video(video=open(filepath, 'rb'))
            os.remove(filepath)
        except Exception:
            await update.message.reply_text(MESSAGES["error"][lang_code])
    else:
        await update.message.reply_text(MESSAGES["send_instagram"][lang_code])

# Botni ishga tushirish
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_language))
app.run_polling()






