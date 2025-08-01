# MP4 Downloader Bot 🎥

Bu Telegram botu, YouTube ve benzeri platformlardan video indirmenizi sağlayan kullanıcı dostu bir araçtır.

## Özellikler 🚀

- **Tam Video İndirme**: Videoları tam uzunlukta indirebilme
- **Bölüm İndirme**: Videolardan belirli zaman aralıklarını kesip indirme
- **Telegram Uyumlu**: 50MB boyut sınırına uygun indirme
- **Kolay Kullanım**: Basit ve anlaşılır arayüz
- **Otomatik Temizleme**: İndirilen dosyaların otomatik silinmesi

## Kurulum 📥

1. Repository'yi klonlayın:
```bash
git clone https://github.com/sh3rly13/mp4_downloader_bot.git
```

2. Gerekli Python paketlerini yükleyin:
```bash
pip install python-telegram-bot yt-dlp
```

3. FFmpeg'i yükleyin ve PATH'e ekleyin:
   - Windows için:
     1. [FFmpeg İndirme Sayfası](https://ffmpeg.org/download.html)'ndan FFmpeg'i indirin
     2. İndirilen zip dosyasını çıkartın (örn: `C:\ffmpeg`)
     3. Sistem PATH'ine FFmpeg'i ekleyin:
        - Windows arama çubuğuna "Ortam Değişkenleri" yazın
        - "Sistem Ortam Değişkenlerini Düzenle"yi seçin
        - "Ortam Değişkenleri" butonuna tıklayın
        - "Sistem değişkenleri" altında "Path" seçin ve "Düzenle"ye tıklayın
        - "Yeni" butonuna tıklayıp FFmpeg'in bin klasörünü ekleyin (örn: `C:\ffmpeg\bin`)
        - Tüm pencereleri "Tamam" diyerek kapatın
        - Değişikliklerin etkili olması için bilgisayarı yeniden başlatın
   
   - Mac için:
     1. Homebrew kullanarak (önerilen yöntem):
        ```bash
        # Önce Homebrew'i kurun (kurulu değilse)
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        
        # FFmpeg'i yükleyin
        brew install ffmpeg
        ```
     2. Manuel kurulum için:
        - [FFmpeg İndirme Sayfası](https://ffmpeg.org/download.html)'ndan Mac için derlenmiş sürümü indirin
        - İndirilen dosyayı çıkartın
        - Terminal'i açın ve şu komutları çalıştırın:
          ```bash
          sudo mkdir -p /usr/local/bin
          sudo mv /yol/ffmpeg /usr/local/bin/
          sudo chmod +x /usr/local/bin/ffmpeg
          ```
   
   - Linux için:
     ```bash
     sudo apt-get install ffmpeg
     ```
     Linux'ta otomatik olarak PATH'e eklenir

4. Bot token'ınızı ayarlayın:
   - `moonyDownloadBot.py` dosyasındaki `TOKEN` değişkenini kendi bot token'ınızla değiştirin

## Kullanım 💡

1. Bot'u başlatın:
```bash
python moonyDownloadBot.py
```

2. Telegram'da bot ile sohbet başlatın ve `/start` komutunu kullanın
3. İndirme seçeneklerinden birini seçin:
   - **Full Mp4**: Tam video indirme
   - **Video içindeki Bölüm**: Belirli bir zaman aralığını indirme

### Bölüm İndirme Formatı 📝

```
URL başlangıç_süresi bitiş_süresi
Örnek: https://youtube.com/... 00:00:30 00:01:30
```

## Sistem Gereksinimleri 🖥️

- Python 3.7+
- FFmpeg
- İnternet bağlantısı
- Yeterli disk alanı

## Katkıda Bulunma 🤝

1. Bu repository'yi fork edin
2. Yeni bir branch oluşturun (`git checkout -b yeni-ozellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik eklendi'`)
4. Branch'inizi push edin (`git push origin yeni-ozellik`)
5. Pull Request oluşturun

## Lisans 📄

Bu proje MIT lisansı altında lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına bakınız.

## İletişim 📬

GitHub Issues üzerinden hata raporları ve öneriler için iletişime geçebilirsiniz.

## Güvenlik ⚠️

- Bot'u rate-limiting ile koruyun
- Disk alanı kullanımını kontrol edin
- Sistem kaynaklarını monitör edin

---
⭐ Eğer bu projeyi beğendiyseniz yıldız vermeyi unutmayın!
