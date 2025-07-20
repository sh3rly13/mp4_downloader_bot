import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
import yt_dlp
import os
import sys

# Bot token'ınızı buraya ekleyin
TOKEN = "123:tokenApiBilgisi"

# downloads klasörünü oluştur
DOWNLOAD_DIR = 'E:\\moonyDownloader\\download'
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Merhaba!")
    await show_menu(update)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "full":
        await query.message.reply_text(
            "Lütfen video URL'sini gönderin."
        )
        context.user_data['mode'] = 'full'
    elif query.data == "section":
        await query.message.reply_text(
            "Lütfen video URL'sini ve başlangıç-bitiş süresini şu formatta gönderin:\n"
            "URL başlangıç_süresi bitiş_süresi\n"
            "Örnek: https://youtube.com/... 00:00:30 00:01:30"
        )
        context.user_data['mode'] = 'section'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'mode' not in context.user_data:
        await update.message.reply_text("Lütfen önce /start komutunu kullanın.")
        return

    message_text = update.message.text
    mode = context.user_data['mode']

    if mode == 'full':
        url = message_text.strip()
        try:
            await download_video(update, url)
        except Exception as e:
            await update.message.reply_text(f"Hata oluştu: {str(e)}")

    elif mode == 'section':
        try:
            parts = message_text.split()
            if len(parts) != 3:
                await update.message.reply_text("Hatalı format! Lütfen 'URL başlangıç_süresi bitiş_süresi' formatında girin.")
                return
            url = parts[0]
            start_time = parts[1]
            end_time = parts[2]
            await download_video_section(update, url, start_time, end_time)
        except Exception as e:
            await update.message.reply_text(f"Hata oluştu: {str(e)}")

async def download_video(update: Update, url: str):
    try:
        await update.message.reply_text("Video indiriliyor...")
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
            'restrictfilenames': True  # Dosya adındaki özel karakterleri kaldırır
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_path = ydl.prepare_filename(info)
            
            # Dosya boyutu kontrolü (Telegram limiti: 50MB)
            if os.path.getsize(video_path) > 50 * 1024 * 1024:
                await update.message.reply_text("Video boyutu 50MB'dan büyük! Daha küçük bir video seçin veya video içindeki bölüm seçeneğini kullanın.")
                os.remove(video_path)
                # Menüyü tekrar göster
                await show_menu(update)
                return
                
            await update.message.reply_video(
                video=open(video_path, 'rb'),
                caption="İşte videonuz!"
            )
            # İndirilen dosyayı temizle
            os.remove(video_path)
            # Menüyü tekrar göster
            await show_menu(update)
    except Exception as e:
        await update.message.reply_text(f"Video indirilirken hata oluştu: {str(e)}")
        # Hata durumunda da menüyü göster
        await show_menu(update)

async def show_menu(update: Update):
    keyboard = [
        [
            InlineKeyboardButton("Full Mp4", callback_data="full"),
            InlineKeyboardButton("Video içindeki Bölüm", callback_data="section")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Video indirme seçeneklerinden birini seçin:",
        reply_markup=reply_markup
    )

async def download_video_section(update: Update, url: str, start_time: str, end_time: str):
    try:
        await update.message.reply_text("Video bölümü indiriliyor...")
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s_section.%(ext)s'),
            'restrictfilenames': True  # Dosya adındaki özel karakterleri kaldırır
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_path = ydl.prepare_filename(info)
            
            # Güvenli bir dosya adı oluştur
            safe_title = "".join(c for c in info['title'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            output_path = os.path.join(DOWNLOAD_DIR, f"section_{safe_title}.mp4")
            
            import subprocess
            cmd = [
                'ffmpeg', '-i', video_path,
                '-ss', start_time,
                '-to', end_time,
                '-c', 'copy',
                output_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # ffmpeg hata kontrolü
            if result.returncode != 0:
                raise Exception(f"FFmpeg hatası: {result.stderr}")
            
            # Dosya boyutu kontrolü
            if os.path.getsize(output_path) > 50 * 1024 * 1024:
                await update.message.reply_text("Video bölümü 50MB'dan büyük! Lütfen daha kısa bir bölüm seçin.")
                os.remove(video_path)
                os.remove(output_path)
                # Menüyü tekrar göster
                await show_menu(update)
                return
                
            await update.message.reply_video(
                video=open(output_path, 'rb'),
                caption="İşte video bölümünüz!"
            )
            # Dosyaları temizle
            os.remove(video_path)
            os.remove(output_path)
            # Menüyü tekrar göster
            await show_menu(update)
    except Exception as e:
        await update.message.reply_text(f"Video bölümü indirilirken hata oluştu: {str(e)}")
        # Hata durumunda da menüyü göster
        await show_menu(update)

def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f'Update {update} caused error {context.error}')

def cleanup_downloads():
    """Download klasöründeki tüm dosyaları temizler"""
    if os.path.exists(DOWNLOAD_DIR):
        for file in os.listdir(DOWNLOAD_DIR):
            file_path = os.path.join(DOWNLOAD_DIR, file)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Dosya silinirken hata oluştu: {e}")

def main() -> None:
    # Windows için event loop politikasını ayarla
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # Başlangıçta downloads klasörünü temizle
    cleanup_downloads()
    
    # Bot uygulamasını oluştur
    app = Application.builder().token(TOKEN).build()
    
    # Handler'ları ekle
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)
    
    print("Bot başlatılıyor...")
    
    # Bot'u başlat ve çalışır durumda tut
    app.run_polling(poll_interval=3.0, timeout=30)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nBot kapatılıyor...')
        sys.exit(0)
    except Exception as e:
        print(f'Beklenmeyen hata: {e}')
        sys.exit(1)
