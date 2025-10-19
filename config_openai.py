"""
OpenAI API Konfigürasyonu
"""
import os
from dotenv import load_dotenv

# .env.local dosyasını yükle (varsa)
load_dotenv('.env.local')

# OpenAI API Key - .env.local dosyasından veya environment variable'dan okunur
# NOT: GÜVENLİK İÇİN API KEY'İ DOĞRUDAN YAZMAYINIZ!
# Bunun yerine .env.local dosyası oluşturun ve içine yazın:
# OPENAI_API_KEY=sk-proj-...

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

# Eğer .env.local yoksa uyarı ver
if not OPENAI_API_KEY:
    print("⚠️ UYARI: OPENAI_API_KEY bulunamadı!")
    print("Lütfen .env.local dosyası oluşturun ve API key'inizi ekleyin.")
    print("Örnek: .env.example dosyasına bakın")

# OpenAI Model (gpt-4o-mini = en ucuz ve hızlı)
OPENAI_MODEL = "gpt-4o-mini"

# OpenAI kullan mı?
USE_OPENAI = True  # True: OpenAI ile akıllı analiz, False: Sadece regex

# Analiz modu
# "text": OCR + OpenAI text analizi (UCUZ)
# "vision": OpenAI Vision ile direkt görüntü analizi (PAHALI - Tesseract gereksiz)
OPENAI_ANALYSIS_MODE = "vision"  # ← SADECE OPENAI (Tesseract yok)

# Vision mode aktif - Tesseract bypass
SKIP_TESSERACT = True  # Vision modunda Tesseract atlanır

