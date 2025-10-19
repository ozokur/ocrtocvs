# OCR to CSV - Fiş Okuyucu

Fiş ve fatura görüntülerini OCR ile okuyarak firma, tutar ve tür bilgilerini çıkaran ve CSV raporu oluşturan masaüstü uygulaması.

## 🎯 Özellikler

### 🚀 Ana Özellikler
- 📁 **Klasör Seçimi**: Kullanıcı dostu arayüz ile klasör seçimi
- 📷 **OCR Desteği**: Tesseract OCR ile Türkçe ve İngilizce metin çıkarma
- 🤖 **AI Analiz**: OpenAI GPT-4o-mini ile akıllı fiş analizi (~$0.0001/fiş)
- 📊 **Excel Desteği**: Varolan Excel'e ekleme veya yeni oluşturma
- 🔒 **Mükerrer Kontrol**: Aynı fiş tekrar eklenmez (hash tabanlı)

### 🔍 Detaylı Analiz (12 Alan)
AI ile otomatik olarak çıkarılan bilgiler:
  - ✅ Firma adı (tam ad, %95 doğruluk)
  - ✅ Şube bilgisi
  - ✅ Tutar (akıllı çıkarım)
  - ✅ KDV tutarı
  - ✅ Para birimi
  - ✅ Tarih (otomatik parse)
  - ✅ Saat
  - ✅ Fiş türü (market, akaryakıt, restoran, vb.)
  - ✅ Ödeme yöntemi (nakit, kredi kartı, vb.)
  - ✅ Fiş numarası
  - ✅ Vergi numarası
  - ✅ Özel notlar

### 📈 Raporlama
- 📊 **Renkli Excel**: Stil uygulanmış, profesyonel görünüm
- 📝 **Özet Sayfası**: Otomatik istatistikler ve grafikler
- 📈 **İstatistikler**: Toplam tutar, ortalama, tür dağılımı
- 🪵 **Detaylı Loglama**: Debug ve hata takibi için kapsamlı log sistemi

### 💎 Ekstra Özellikler
- 🎨 **Modern GUI**: Tkinter tabanlı modern ve kullanımı kolay arayüz
- ⚡ **Çok Hızlı**: GPT-4o-mini ile saniyeler içinde analiz
- 🔄 **Sürekli Güncelleme**: Aynı Excel'i sürekli güncelleyin
- 🔐 **Güvenli**: API key korumalı, veriler saklanmaz

## 📋 Gereksinimler

- Python 3.8 veya üzeri
- Tesseract OCR

## 🚀 Kurulum

### 1. Python Bağımlılıklarını Yükleyin

```bash
pip install -r requirements.txt
```

### 2. Tesseract OCR'yi Yükleyin

#### Windows:
1. [Tesseract OCR Windows installer](https://github.com/UB-Mannheim/tesseract/wiki) adresinden indirin
2. Kurulum sırasında Türkçe dil paketini seçin
3. Kurulum sonrası Tesseract'ın PATH'e eklendiğinden emin olun

Alternatif olarak, `pytesseract` konfigürasyonunda Tesseract yolunu manuel belirtin:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt-get install tesseract-ocr
sudo apt-get install tesseract-ocr-tur  # Türkçe dil paketi
```

#### macOS:
```bash
brew install tesseract
brew install tesseract-lang  # Tüm dil paketleri
```

Detaylı kurulum kılavuzu için [INSTALL.md](INSTALL.md) dosyasına bakın.

## 💻 Kullanım

### Uygulamayı Başlatma

```bash
python main.py
```

### Adım Adım Kullanım

1. **Klasör Seç** butonuna tıklayın
2. Fiş görüntülerinin bulunduğu klasörü seçin
3. **İşlemi Başlat** butonuna tıklayın
4. İşlem tamamlanınca raporlar seçilen klasörde oluşturulur

### Desteklenen Görüntü Formatları

- JPG/JPEG
- PNG
- BMP
- TIFF/TIF

## 📂 Proje Yapısı

```
ocrtocvs/
├── main.py              # Ana uygulama ve GUI
├── ocr_processor.py     # OCR işlemleri
├── data_extractor.py    # Veri çıkarma ve analiz
├── csv_reporter.py      # CSV rapor oluşturma
├── logger.py            # Log sistemi
├── config.py            # Konfigürasyon ayarları
├── requirements.txt     # Python bağımlılıkları
├── CHANGELOG.md         # Sürüm değişiklikleri
├── INSTALL.md           # Detaylı kurulum kılavuzu
└── README.md           # Bu dosya
```

## 📊 Çıktı Dosyaları

### CSV Raporu (`fis_raporu_YYYYMMDD_HHMMSS.csv`)

Her fiş için detaylı bilgiler:
- Dosya Adı
- Tarih
- Firma
- Tür
- Tutar
- Para Birimi
- Durum

### Özet Raporu (`fis_ozeti_YYYYMMDD_HHMMSS.txt`)

Toplu istatistikler:
- Toplam fiş sayısı
- Başarılı/başarısız işlem sayısı
- Toplam tutar
- Ortalama tutar
- Tür dağılımı

## 🪵 Log Dosyaları

Log dosyaları `logs/` klasöründe günlük olarak oluşturulur:
- Format: `YYYYMMDD_ocr_app.log`
- Seviye: DEBUG, INFO, WARNING, ERROR, CRITICAL

## ⚙️ Konfigürasyon

`config.py` dosyasından ayarları değiştirebilirsiniz:

```python
VERSION = "1.0.0"              # Uygulama versiyonu
LOG_LEVEL = "DEBUG"            # Log seviyesi
TESSERACT_LANG = 'tur+eng'     # OCR dil desteği
CSV_ENCODING = 'utf-8-sig'     # CSV kodlaması
```

## 🔧 Sorun Giderme

### Tesseract bulunamadı hatası

```python
# ocr_processor.py dosyasına ekleyin:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### OCR kalitesi düşük

- Görüntülerin kalitesini artırın (min 300 DPI)
- Görüntüleri düz yüzeyde, iyi ışıkta çekin
- Bulanık veya eğik görüntülerden kaçının

### Tutar/firma bulunamadı

- Fiş görüntüsünün net olduğundan emin olun
- `data_extractor.py` içindeki pattern'leri ihtiyacınıza göre düzenleyin

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Commit edin (`git commit -m 'Add some AmazingFeature'`)
4. Push edin (`git push origin feature/AmazingFeature`)
5. Pull Request açın

## 📝 Lisans

Bu proje açık kaynaklıdır ve herkes tarafından kullanılabilir.

## 📧 İletişim

Sorularınız için issue açabilirsiniz.

## 🙏 Teşekkürler

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [Pytesseract](https://github.com/madmaze/pytesseract)
- [OpenCV](https://opencv.org/)
- [Pandas](https://pandas.pydata.org/)

---

**Versiyon**: 1.0.0  
**Tarih**: 19 Ekim 2025
