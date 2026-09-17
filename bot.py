import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import yt_dlp

# إعداد السجلات لمتابعة الأخطاء
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# توكن البوت الخاص بك
TOKEN = 8749758017:AAHaHL9NQ4yvZiEiv61C1OQlG4-6r5IBGvc"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أهلاً بك! أرسل لي أي رابط من يوتيوب، تيك توك، إنستغرام أو أي منصة أخرى وسأقوم بتحميله لك مباشرة."
    )

async def download_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    
    # التحقق من أن الرسالة عبارة عن رابط
    if not url.startswith("http://") and not url.startswith("https://"):
        await update.message.reply_text("الرجاء إرسال رابط صالح.")
        return

    msg = await update.message.reply_text("جاري معالجة الرابط وتحميل الملف... ⏳")

    output_template = '%(id)s.%(ext)s'
    
    ydl_opts = {
        'outtmpl': output_template,
        'format': 'best', # اختيار أفضل جودة متاحة
        'max_filesize': 50 * 1024 * 1024, # حد أقصى 50 ميجابايت لرفع تيليجرام العادي
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        await msg.edit_text("جاري إرسال الملف... 📤")

        with open(filename, 'rb') as video_file:
            await update.message.reply_video(video=video_file)

        # حذف الملف من السيرفر بعد الإرسال لتوفير المساحة
        os.remove(filename)
        await msg.delete()

    except Exception as e:
        logging.error(f"Error: {e}")
        await msg.edit_text("حدث خطأ أثناء التحميل. تأكد أن الرابط مدعوم أو أن حجم الفيديو مناسب.")
        # تنظيف الملف في حال بقائه
        if 'filename' in locals() and os.path.exists(filename):
            os.remove(filename)

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), download_media))

    print("البوت يعمل الآن...")
    application.run_polling()

if __name__ == '__main__':
    main()
