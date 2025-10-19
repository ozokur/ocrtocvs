"""
OpenAI entegrasyonunu test eden basit script
"""
import sys
import io

# Windows console encoding fix
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from openai_analyzer import OpenAIAnalyzer
from config_openai import OPENAI_API_KEY, OPENAI_MODEL

# Test metni (örnek fiş)
test_text = """
MİGROS
ŞİRİNEVLER ŞUBESI
Tarih: 19/10/2025
Saat: 14:30

SÜPERMARKET ALIŞVERIŞ

EKMEK          15.00 TL
SÜT            25.50 TL
PEYNIR         85.75 TL
----------------------------
TOPLAM:       126.25 TL

TEŞEKKÜR EDERİZ
"""

print("=" * 60)
print("OpenAI GPT-4o-mini Test")
print("=" * 60)
print()

try:
    # Analyzer oluştur
    print("✓ OpenAI Analyzer başlatılıyor...")
    analyzer = OpenAIAnalyzer(api_key=OPENAI_API_KEY, model=OPENAI_MODEL)
    print(f"✓ Model: {OPENAI_MODEL}")
    print()
    
    # Metni analiz et
    print("📝 Test metni analiz ediliyor...")
    print("-" * 60)
    print(test_text)
    print("-" * 60)
    print()
    
    result = analyzer.analyze_receipt_from_text(test_text, "test_fis.jpg")
    
    if result:
        print("✅ BAŞARILI! OpenAI Analiz Sonucu:")
        print("=" * 60)
        print(f"Firma      : {result.get('firma')}")
        print(f"Tutar      : {result.get('tutar')} {result.get('para_birimi')}")
        print(f"Tarih      : {result.get('tarih')}")
        print(f"Tür        : {result.get('tur')}")
        print("=" * 60)
        print()
        print("🎉 OpenAI entegrasyonu çalışıyor!")
        print("💰 Maliyet: ~$0.0001 (çok ucuz!)")
    else:
        print("❌ Analiz başarısız!")
        
except Exception as e:
    print(f"❌ HATA: {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 60)

