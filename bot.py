async def download_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if not url.startswith("http"):
        await update.message.reply_text("الرجاء إرسال رابط صالح.")
        return
        
    msg = await update.message.reply_text("جاري التحميل... ⏳")
    
    # خيارات محسنة لـ yt-dlp لتجنب أخطاء التحميل
    ydl_opts = {
        'outtmpl': '%(id)s.%(ext)s',
        'format': 'best[filesize<50M]/best', # اختيار أفضل جودة تحت 50 ميغابايت تلقائياً
        'noplaylist': True,
    }
    
    filename = None
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
        await msg.edit_text("جاري الإرسال... 📤")
        
        with open(filename, 'rb') as f:
            await update.message.reply_video(video=f)
            
    except Exception as e:
        await msg.edit_text(f"حدث خطأ أثناء التحميل. تأكد أن الرابط مدعوم أو أن حجم الفيديو مناسب.")
        
    finally:
        # تنظيف الملفات المؤكد وجودها لحذفها من السيرفر
        if filename and os.path.exists(filename):
            try:
                os.remove(filename)
            except:
                pass
        try:
            await msg.delete()
        except:
            pass
