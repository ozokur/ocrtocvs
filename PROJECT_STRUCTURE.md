# Proje Yapısı ve Dosya Açıklamaları

Bu doküman, projedeki tüm dosyaları ve görevlerini açıklar.

## 📁 Ana Dosyalar

### Uygulama Dosyaları

| Dosya | Açıklama |
|-------|----------|
| `main.py` | Ana uygulama dosyası - GUI ve kullanıcı arayüzü |
| `ocr_processor.py` | OCR işlemleri - Görüntülerden metin çıkarma |
| `data_extractor.py` | Veri çıkarma - Firma, tutar, tür analizi |
| `csv_reporter.py` | CSV rapor oluşturma ve istatistikler |
| `logger.py` | Log sistemi - Hata takibi ve debug |
| `config.py` | Konfigürasyon ayarları ve sabitler |

### Dokümantasyon

| Dosya | Açıklama |
|-------|----------|
| `README.md` | Proje ana dokümantasyonu |
| `INSTALL.md` | Detaylı kurulum kılavuzu (Windows/Linux/macOS) |
| `QUICKSTART.md` | Hızlı başlangıç kılavuzu (5 dakika) |
| `CHANGELOG.md` | Versiyon geçmişi ve değişiklikler |
| `PROJECT_STRUCTURE.md` | Bu dosya - Proje yapısı |

### Bağımlılıklar ve Konfigürasyon

| Dosya | Açıklama |
|-------|----------|
| `requirements.txt` | Python paket bağımlılıkları |
| `.gitignore` | Git için ignore edilecek dosyalar |

### Çalıştırma Scriptleri

| Dosya | Açıklama |
|-------|----------|
| `run.bat` | Windows için başlatma scripti |
| `run.sh` | Linux/macOS için başlatma scripti |

## 🏗️ Modül Yapısı

```
OCR to CSV Application
│
├── UI Layer (main.py)
│   ├── Tkinter GUI
│   ├── Folder Selection Dialog
│   ├── Progress Tracking
│   └── User Messages
│
├── Processing Layer
│   ├── OCR Module (ocr_processor.py)
│   │   ├── Image Preprocessing
│   │   ├── Text Extraction
│   │   └── Directory Processing
│   │
│   └── Data Extraction (data_extractor.py)
│       ├── Amount Extraction
│       ├── Date Extraction
│       ├── Company Extraction
│       └── Type Classification
│
├── Output Layer (csv_reporter.py)
│   ├── CSV Report Generation
│   ├── Summary Report
│   └── Statistics Calculation
│
└── Support Layer
    ├── Logger (logger.py)
    │   ├── File Logging
    │   └── Console Logging
    │
    └── Config (config.py)
        ├── Version Info
        ├── OCR Settings
        └── Output Settings
```

## 📊 Veri Akışı

```
Kullanıcı Klasör Seçer
         ↓
    main.py (GUI)
         ↓
ocr_processor.py
    • Görüntüleri bulur
    • Ön işleme yapar
    • OCR uygular
         ↓
data_extractor.py
    • Firma çıkarır
    • Tutar bulur
    • Tür belirler
    • Tarih çıkarır
         ↓
csv_reporter.py
    • CSV raporu oluşturur
    • Özet rapor hazırlar
    • İstatistikleri hesaplar
         ↓
    Raporlar Kaydedilir
    (Seçilen klasörde)
```

## 🔧 Modül Detayları

### main.py
**Sınıflar:**
- `OCRApp`: Ana uygulama sınıfı
  - `_create_ui()`: UI elemanlarını oluşturur
  - `_select_folder()`: Klasör seçim dialogu
  - `_start_processing()`: İşlem başlatır
  - `_process_images()`: Görüntüleri işler (thread)

**Bağımlılıklar:** tkinter, threading

### ocr_processor.py
**Sınıflar:**
- `OCRProcessor`: OCR işlemleri
  - `preprocess_image()`: Görüntü ön işleme
  - `extract_text()`: Metin çıkarma
  - `process_directory()`: Toplu işlem

**Bağımlılıklar:** pytesseract, PIL, opencv-python

**OCR İşlem Adımları:**
1. Görüntü okuma
2. Gri tonlamaya çevirme
3. Gürültü azaltma
4. Kontrast artırma (CLAHE)
5. Adaptive threshold
6. Tesseract OCR uygulama

### data_extractor.py
**Sınıflar:**
- `DataExtractor`: Veri çıkarma
  - `extract_amount()`: Tutar çıkarma (regex)
  - `extract_date()`: Tarih çıkarma (regex)
  - `extract_company()`: Firma belirleme
  - `extract_type()`: Fiş türü belirleme
  - `extract_all()`: Tüm verileri çıkarma

**Desteklenen Fiş Türleri:**
- Market
- Akaryakıt
- Restoran
- Elektronik
- Eczane
- Giyim
- Diğer

### csv_reporter.py
**Sınıflar:**
- `CSVReporter`: Rapor oluşturma
  - `create_report()`: CSV raporu
  - `create_summary_report()`: Özet rapor
  - `_log_statistics()`: İstatistik loglama

**Bağımlılıklar:** pandas

**Çıktı Formatı:**
- CSV: UTF-8 with BOM (Excel uyumlu)
- Sütunlar: Dosya Adı, Tarih, Firma, Tür, Tutar, Para Birimi, Durum

### logger.py
**Fonksiyonlar:**
- `setup_logger()`: Logger yapılandırma

**Log Seviyeleri:**
- DEBUG: Detaylı debug bilgisi
- INFO: Genel bilgi mesajları
- WARNING: Uyarılar
- ERROR: Hatalar
- CRITICAL: Kritik hatalar

**Log Yerleri:**
- Dosya: `logs/YYYYMMDD_ocr_app.log`
- Console: Sadece INFO ve üzeri

### config.py
**Sabitler:**
- `VERSION`: Uygulama versiyonu
- `APP_NAME`: Uygulama adı
- `LOG_LEVEL`: Log seviyesi
- `SUPPORTED_IMAGE_EXTENSIONS`: Desteklenen formatlar
- `TESSERACT_LANG`: OCR dil ayarı
- `OUTPUT_FIELDS`: CSV sütunları

## 📦 Bağımlılıklar

```
pytesseract==0.3.10    # OCR wrapper
Pillow==10.1.0         # Görüntü işleme
opencv-python==4.8.1.78 # Görüntü ön işleme
pandas==2.1.3          # CSV işlemleri
python-dateutil==2.8.2 # Tarih işlemleri
```

## 🗂️ Runtime Klasörleri

İlk çalıştırmada otomatik oluşturulur:

| Klasör | İçerik |
|--------|--------|
| `logs/` | Log dosyaları (YYYYMMDD_ocr_app.log) |
| Seçilen klasör | CSV ve özet raporları |

## 🔒 .gitignore Kapsamı

- Python cache dosyaları (`__pycache__/`, `*.pyc`)
- Log dosyaları (`logs/`, `*.log`)
- Virtual environment (`venv/`, `env/`)
- IDE dosyaları (`.vscode/`, `.idea/`)
- Output dosyaları (`*.csv`, `fis_*.txt`)

## 📈 Genişletme Noktaları

### Yeni Fiş Türü Eklemek
`data_extractor.py` içinde `self.receipt_types` sözlüğüne ekleyin.

### Yeni Veri Alanı Eklemek
1. `data_extractor.py` içinde extraction methodu yazın
2. `config.py` içinde `OUTPUT_FIELDS` listesine ekleyin
3. `data_extractor.extract_all()` içinde çağırın

### OCR Ayarlarını Değiştirmek
`config.py` içinde `TESSERACT_LANG` ve `ocr_processor.py` içinde custom_config ayarlayın.

### UI Özelleştirmek
`main.py` içinde `_create_ui()` methodunu düzenleyin.

## 🧪 Test Önerileri

1. **Farklı görüntü kaliteleri** test edin
2. **Farklı fiş türleri** deneyin
3. **Çok sayıda dosya** ile performans test edin
4. **Hatalı/bozuk görüntüler** ile hata yönetimini test edin
5. **Farklı dillerde** fişler deneyin

## 📞 Destek

Her modül kendi log mesajlarını üretir. Sorun yaşarsanız:
1. `logs/` klasöründe güncel log dosyasını kontrol edin
2. DEBUG seviyesinde detaylı bilgi bulabilirsiniz
3. Hata mesajlarını GitHub Issues'da paylaşın

---

**Proje Versiyonu:** 1.0.0  
**Son Güncelleme:** 19 Ekim 2025

