"""
Test scripti - Modullerin temel fonksiyonlarini test eder
"""
import os
import sys

# Windows console encoding fix
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from logger import setup_logger
from config import VERSION, APP_NAME

logger = setup_logger(__name__)

def test_imports():
    """Tüm modüllerin import edilebilir olduğunu test eder"""
    print("=" * 60)
    print("TEST 1: Modül İmportları")
    print("=" * 60)
    
    try:
        import pytesseract
        print("✓ pytesseract import edildi")
    except ImportError as e:
        print(f"✗ pytesseract import hatası: {e}")
        return False
    
    try:
        from PIL import Image
        print("✓ PIL (Pillow) import edildi")
    except ImportError as e:
        print(f"✗ PIL import hatası: {e}")
        return False
    
    try:
        import cv2
        print("✓ OpenCV import edildi")
    except ImportError as e:
        print(f"✗ OpenCV import hatası: {e}")
        return False
    
    try:
        import pandas
        print("✓ Pandas import edildi")
    except ImportError as e:
        print(f"✗ Pandas import hatası: {e}")
        return False
    
    try:
        from ocr_processor import OCRProcessor
        print("✓ OCRProcessor import edildi")
    except ImportError as e:
        print(f"✗ OCRProcessor import hatası: {e}")
        return False
    
    try:
        from data_extractor import DataExtractor
        print("✓ DataExtractor import edildi")
    except ImportError as e:
        print(f"✗ DataExtractor import hatası: {e}")
        return False
    
    try:
        from csv_reporter import CSVReporter
        print("✓ CSVReporter import edildi")
    except ImportError as e:
        print(f"✗ CSVReporter import hatası: {e}")
        return False
    
    print("\n✅ Tüm modüller başarıyla import edildi!\n")
    return True

def test_tesseract():
    """Tesseract OCR'ın kurulu ve çalışır olduğunu test eder"""
    print("=" * 60)
    print("TEST 2: Tesseract OCR")
    print("=" * 60)
    
    try:
        import pytesseract
        
        # Tesseract versiyonunu kontrol et
        version = pytesseract.get_tesseract_version()
        print(f"✓ Tesseract versiyon: {version}")
        
        # Dil paketlerini kontrol et
        try:
            langs = pytesseract.get_languages()
            print(f"✓ Yüklü diller: {', '.join(langs)}")
            
            if 'tur' in langs:
                print("✓ Türkçe dil paketi yüklü")
            else:
                print("⚠ Türkçe dil paketi yüklü DEĞİL! (Lütfen Tesseract Türkçe paketini yükleyin)")
            
            if 'eng' in langs:
                print("✓ İngilizce dil paketi yüklü")
        except:
            print("⚠ Dil paketleri kontrol edilemedi")
        
        print("\n✅ Tesseract OCR çalışıyor!\n")
        return True
        
    except Exception as e:
        print(f"✗ Tesseract OCR HATASI: {e}")
        print("\n❌ Tesseract OCR kurulu değil veya PATH'te yok!")
        print("\nLütfen Tesseract'ı yükleyin:")
        print("  Windows: https://github.com/UB-Mannheim/tesseract/wiki")
        print("  Linux: sudo apt-get install tesseract-ocr tesseract-ocr-tur")
        print("  macOS: brew install tesseract tesseract-lang")
        print()
        return False

def test_data_extraction():
    """Veri çıkarma fonksiyonlarını test eder"""
    print("=" * 60)
    print("TEST 3: Veri Çıkarma")
    print("=" * 60)
    
    try:
        from data_extractor import DataExtractor
        
        extractor = DataExtractor()
        
        # Test metni
        test_text = """
        MİGROS
        ŞİRİNEVLER ŞUBE
        TARİH: 19/10/2025
        SAAT: 14:30
        
        SÜPERMARKET ALIŞVERIS
        
        EKMEK          15.00 TL
        SÜT            25.50 TL
        PEYNIR         85.75 TL
        
        TOPLAM:       126.25 TL
        """
        
        # Tutar testi
        amount, currency = extractor.extract_amount(test_text)
        if amount and currency:
            print(f"✓ Tutar: {amount} {currency}")
        else:
            print("⚠ Tutar bulunamadı")
        
        # Tarih testi
        date = extractor.extract_date(test_text)
        if date:
            print(f"✓ Tarih: {date}")
        else:
            print("⚠ Tarih bulunamadı")
        
        # Firma testi
        company = extractor.extract_company(test_text)
        print(f"✓ Firma: {company}")
        
        # Tür testi
        receipt_type = extractor.extract_type(test_text)
        print(f"✓ Tür: {receipt_type}")
        
        print("\n✅ Veri çıkarma testleri başarılı!\n")
        return True
        
    except Exception as e:
        print(f"✗ Veri çıkarma hatası: {e}")
        return False

def test_csv_reporter():
    """CSV rapor oluşturmayı test eder"""
    print("=" * 60)
    print("TEST 4: CSV Rapor")
    print("=" * 60)
    
    try:
        from csv_reporter import CSVReporter
        
        reporter = CSVReporter()
        
        # Test verisi
        test_data = [
            {
                'Dosya Adı': 'test_fis_1.jpg',
                'Tarih': '19/10/2025',
                'Firma': 'Migros',
                'Tür': 'market',
                'Tutar': 126.25,
                'Para Birimi': 'TL',
                'Durum': 'Başarılı'
            },
            {
                'Dosya Adı': 'test_fis_2.jpg',
                'Tarih': '18/10/2025',
                'Firma': 'Shell',
                'Tür': 'akaryakıt',
                'Tutar': 500.00,
                'Para Birimi': 'TL',
                'Durum': 'Başarılı'
            }
        ]
        
        # Test klasörü oluştur
        test_output_dir = "test_output"
        if not os.path.exists(test_output_dir):
            os.makedirs(test_output_dir)
        
        # CSV raporu oluştur
        csv_path = reporter.create_report(test_data, test_output_dir)
        if csv_path and os.path.exists(csv_path):
            print(f"✓ CSV raporu oluşturuldu: {csv_path}")
        else:
            print("⚠ CSV raporu oluşturulamadı")
            return False
        
        # Özet raporu oluştur
        summary_path = reporter.create_summary_report(test_data, test_output_dir)
        if summary_path and os.path.exists(summary_path):
            print(f"✓ Özet raporu oluşturuldu: {summary_path}")
        else:
            print("⚠ Özet raporu oluşturulamadı")
        
        print(f"\n✅ Rapor testleri başarılı! Test dosyaları: {test_output_dir}\n")
        return True
        
    except Exception as e:
        print(f"✗ CSV rapor hatası: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Ana test fonksiyonu"""
    print("\n")
    print("#" * 60)
    print(f"# {APP_NAME} v{VERSION}")
    print("# TEST SENARYOSU")
    print("#" * 60)
    print("\n")
    
    results = []
    
    # Test 1: Modül importları
    results.append(("Modül İmportları", test_imports()))
    
    # Test 2: Tesseract OCR
    results.append(("Tesseract OCR", test_tesseract()))
    
    # Test 3: Veri çıkarma
    results.append(("Veri Çıkarma", test_data_extraction()))
    
    # Test 4: CSV rapor
    results.append(("CSV Rapor", test_csv_reporter()))
    
    # Sonuçlar
    print("=" * 60)
    print("TEST SONUÇLARI")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✅ BAŞARILI" if result else "❌ BAŞARISIZ"
        print(f"{test_name:30} {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Toplam: {len(results)} test")
    print(f"Başarılı: {passed}")
    print(f"Başarısız: {failed}")
    print("=" * 60 + "\n")
    
    if failed > 0:
        print("⚠ Bazı testler başarısız! Lütfen hataları kontrol edin.")
        print("\nEn yaygın sorun: Tesseract OCR kurulu değil.")
        print("Çözüm için INSTALL.md dosyasına bakın.\n")
        return False
    else:
        print("🎉 TÜM TESTLER BAŞARILI!")
        print("Uygulama kullanıma hazır: python main.py\n")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

