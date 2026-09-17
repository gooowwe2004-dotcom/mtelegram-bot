import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import yt_dlp

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# سحب التوكن من إعدادات موقع Render تلقائياً
TOKEN = os.environ.get("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك! أرسل لي أي رابط وسأقوم بتحميله.")

async def download_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if not url.startswith("http"):
        await update.message.reply_text("الرجاء إرسال رابط صالح.")
        return
    msg = await update.message.reply_text("جاري التحميل... ⏳")
    ydl_opts = {'outtmpl': '%(id)s.%(ext)s', 'format': 'best', 'max_filesize': 50 * 1024 * 1024}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        await msg.edit_text("جاري الإرسال... 📤")
        with open(filename, 'rb') as f:
            await update.message.reply_video(video=f)
        os.remove(filename)
        await msg.delete()
    except Exception as e:
        await msg.edit_text("حدث خطأ، قد يكون الفيديو كبيراً جداً أو الرابط غير مدعوم.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), download_media))
    print("Bot is running...")
    app.run_polling()
