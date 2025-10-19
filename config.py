"""
Konfigürasyon ayarları
"""

# Versiyon bilgisi
VERSION = "1.0.0"
APP_NAME = "OCR to CSV - Fiş Okuyucu"

# Log ayarları
LOG_LEVEL = "DEBUG"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = "ocr_app.log"

# OCR ayarları
SUPPORTED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']
TESSERACT_LANG = 'eng'  # İngilizce (tur dil paketi kurulursa 'tur+eng' yapılabilir)

# AI OCR ayarları (PaddleOCR)
USE_AI_OCR = False  # True: PaddleOCR kullan, False: Tesseract kullan (şimdilik Tesseract)
AI_OCR_LANG = 'en'  # PaddleOCR dil kodu ('en', 'ch', 'tr', vb.)
AI_OCR_USE_GPU = False  # GPU kullan (CUDA gerektirir)
AI_OCR_CONFIDENCE_THRESHOLD = 0.5  # Minimum güven skoru (0.0-1.0)

# CSV ayarları
CSV_DELIMITER = ','
CSV_ENCODING = 'utf-8-sig'  # Excel için BOM ile UTF-8

# Çıkarılacak veri alanları (Detaylı)
OUTPUT_FIELDS = [
    'Dosya Adı', 'Tarih', 'Saat', 'Firma', 'Şube', 'Tür', 
    'Tutar', 'KDV', 'Para Birimi', 'Ödeme Yöntemi', 
    'Fiş No', 'Vergi No', 'Notlar', 'Durum'
]

