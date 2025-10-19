"""
Veri çıkarma modülü - Fişlerden firma, tutar, tür bilgilerini çıkarır
"""
import re
from datetime import datetime
from logger import setup_logger

logger = setup_logger(__name__)

# OpenAI entegrasyonu (opsiyonel)
try:
    from openai_analyzer import OpenAIAnalyzer
    from config_openai import OPENAI_API_KEY, OPENAI_MODEL, USE_OPENAI, OPENAI_ANALYSIS_MODE
    OPENAI_AVAILABLE = True
    logger.info("OpenAI entegrasyonu aktif")
except ImportError:
    OPENAI_AVAILABLE = False
    USE_OPENAI = False
    logger.info("OpenAI entegrasyonu yok, regex kullanılacak")


class DataExtractor:
    """Fiş verilerini çıkaran sınıf"""
    
    def __init__(self):
        """Data Extractor başlatıcı"""
        logger.info("Data Extractor başlatıldı")
        
        # OpenAI analyzer'ı başlat (varsa)
        self.openai_analyzer = None
        if OPENAI_AVAILABLE and USE_OPENAI:
            try:
                self.openai_analyzer = OpenAIAnalyzer(api_key=OPENAI_API_KEY, model=OPENAI_MODEL)
                logger.info(f"OpenAI Analyzer aktif (model: {OPENAI_MODEL})")
            except Exception as e:
                logger.warning(f"OpenAI Analyzer başlatılamadı: {e}")
                self.openai_analyzer = None
        
        # Tutar regex pattern'leri
        self.amount_patterns = [
            r'(?:TOPLAM|TOTAL|TUTAR|AMOUNT|TL|₺)\s*[:=]?\s*(\d{1,3}(?:[.,]\d{3})*[.,]\d{2})',
            r'(\d{1,3}(?:[.,]\d{3})*[.,]\d{2})\s*(?:TL|₺)',
            r'(?:TOPLAM|TOTAL)\s*.*?(\d{1,3}(?:[.,]\d{3})*[.,]\d{2})',
        ]
        
        # Tarih regex pattern'leri
        self.date_patterns = [
            r'(\d{2}[./\-]\d{2}[./\-]\d{4})',
            r'(\d{2}[./\-]\d{2}[./\-]\d{2})',
            r'(\d{4}[./\-]\d{2}[./\-]\d{2})',
        ]
        
        # Bilinen firma kelimeleri (küçük harf)
        self.known_companies = [
            'migros', 'carrefour', 'bim', 'a101', 'şok', 'metro',
            'tesco', 'real', 'kipa', 'macro', 'makro', 'aldi',
            'lidl', 'gratis', 'rossmann', 'watsons', 'mediamarkt',
            'teknosa', 'vatan', 'arçelik', 'vestel', 'samsung',
            'shell', 'opet', 'bp', 'total', 'petrol', 'benzin'
        ]
        
        # Fiş türleri
        self.receipt_types = {
            'market': ['market', 'süpermarket', 'gıda', 'migros', 'carrefour', 'bim', 'a101', 'şok'],
            'akaryakıt': ['akaryakıt', 'benzin', 'mazot', 'shell', 'opet', 'bp', 'petrol'],
            'restoran': ['restoran', 'restaurant', 'cafe', 'kafe', 'yemek', 'food'],
            'elektronik': ['elektronik', 'teknoloji', 'mediamarkt', 'teknosa', 'vatan'],
            'eczane': ['eczane', 'pharmacy', 'ilaç'],
            'giyim': ['mağaza', 'store', 'giyim', 'tekstil', 'ayakkabı'],
        }
    
    def extract_amount(self, text):
        """
        Metinden tutar bilgisini çıkarır
        
        Args:
            text: OCR ile çıkarılan metin
            
        Returns:
            tuple: (tutar, para_birimi)
        """
        try:
            logger.debug("Tutar çıkarma işlemi başladı")
            
            for pattern in self.amount_patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                amounts = []
                
                for match in matches:
                    amount_str = match.group(1)
                    # Nokta ve virgülleri standartlaştır
                    amount_str = amount_str.replace('.', '').replace(',', '.')
                    try:
                        amount = float(amount_str)
                        amounts.append(amount)
                    except ValueError:
                        continue
                
                if amounts:
                    # En büyük tutarı al (genellikle toplam)
                    max_amount = max(amounts)
                    logger.debug(f"Tutar bulundu: {max_amount}")
                    return max_amount, 'TL'
            
            logger.warning("Tutar bulunamadı")
            return None, None
            
        except Exception as e:
            logger.error(f"Tutar çıkarma hatası: {str(e)}")
            return None, None
    
    def extract_date(self, text):
        """
        Metinden tarih bilgisini çıkarır
        
        Args:
            text: OCR ile çıkarılan metin
            
        Returns:
            str: Tarih (DD/MM/YYYY formatında)
        """
        try:
            logger.debug("Tarih çıkarma işlemi başladı")
            
            for pattern in self.date_patterns:
                match = re.search(pattern, text)
                if match:
                    date_str = match.group(1)
                    logger.debug(f"Tarih bulundu: {date_str}")
                    
                    # Tarihi standartlaştır
                    date_str = date_str.replace('-', '/').replace('.', '/')
                    return date_str
            
            logger.warning("Tarih bulunamadı")
            return None
            
        except Exception as e:
            logger.error(f"Tarih çıkarma hatası: {str(e)}")
            return None
    
    def extract_company(self, text):
        """
        Metinden firma bilgisini çıkarır
        
        Args:
            text: OCR ile çıkarılan metin
            
        Returns:
            str: Firma adı
        """
        try:
            logger.debug("Firma çıkarma işlemi başladı")
            
            text_lower = text.lower()
            lines = text.split('\n')
            
            # İlk 10 satırda bilinen firmaları ara
            for line in lines[:10]:
                line_lower = line.lower().strip()
                for company in self.known_companies:
                    if company in line_lower:
                        # Satırdaki firma adını çek
                        company_name = line.strip()
                        if company_name:
                            logger.debug(f"Firma bulundu: {company_name}")
                            return company_name
            
            # Bulunamadıysa ilk satırı döndür
            if lines and lines[0].strip():
                company_name = lines[0].strip()
                logger.debug(f"Firma (ilk satır): {company_name}")
                return company_name
            
            logger.warning("Firma bulunamadı")
            return "Bilinmeyen Firma"
            
        except Exception as e:
            logger.error(f"Firma çıkarma hatası: {str(e)}")
            return "Hata"
    
    def extract_type(self, text):
        """
        Metinden fiş türünü çıkarır
        
        Args:
            text: OCR ile çıkarılan metin
            
        Returns:
            str: Fiş türü
        """
        try:
            logger.debug("Tür çıkarma işlemi başladı")
            
            text_lower = text.lower()
            
            # Her tür için anahtar kelimeleri kontrol et
            type_scores = {}
            for receipt_type, keywords in self.receipt_types.items():
                score = sum(1 for keyword in keywords if keyword in text_lower)
                if score > 0:
                    type_scores[receipt_type] = score
            
            if type_scores:
                # En yüksek skora sahip türü döndür
                best_type = max(type_scores, key=type_scores.get)
                logger.debug(f"Tür bulundu: {best_type}")
                return best_type
            
            logger.warning("Tür belirlenemedi")
            return "Diğer"
            
        except Exception as e:
            logger.error(f"Tür çıkarma hatası: {str(e)}")
            return "Hata"
    
    def extract_all(self, filename, text, image_path=None):
        """
        Tüm bilgileri çıkarır (OpenAI veya regex ile)
        
        Args:
            filename: Dosya adı
            text: OCR ile çıkarılan metin
            image_path: Görüntü yolu (OpenAI Vision için opsiyonel)
            
        Returns:
            dict: Çıkarılan tüm bilgiler
        """
        logger.info(f"Veri çıkarma başladı: {filename}")
        
        # OpenAI ile akıllı analiz dene
        if self.openai_analyzer:
            try:
                logger.info(f"OpenAI ile analiz ediliyor: {filename}")
                
                if OPENAI_ANALYSIS_MODE == "vision" and image_path:
                    # Vision API kullan (direkt görüntü analizi)
                    logger.info(f"🎨 Vision mode: Görüntü analiz ediliyor {filename}")
                    ai_result = self.openai_analyzer.analyze_receipt_from_image(image_path, filename)
                elif text:
                    # Text analizi kullan (UCUZ - text varsa)
                    ai_result = self.openai_analyzer.analyze_receipt_from_text(text, filename)
                else:
                    # Text yok ama vision mode değilse hata
                    logger.warning(f"Text boş ve vision mode değil: {filename}")
                    ai_result = None
                
                if ai_result:
                    # OpenAI sonucunu formatla (detaylı)
                    result = {
                        'Dosya Adı': filename,
                        'Tarih': ai_result.get('tarih') or 'N/A',
                        'Saat': ai_result.get('saat') or 'N/A',
                        'Firma': ai_result.get('firma') or 'Bilinmeyen Firma',
                        'Şube': ai_result.get('sube') or 'N/A',
                        'Tür': ai_result.get('tur') or 'Diğer',
                        'Tutar': float(ai_result.get('tutar', 0)) if ai_result.get('tutar') else 0.0,
                        'KDV': float(ai_result.get('kdv', 0)) if ai_result.get('kdv') else 0.0,
                        'Para Birimi': ai_result.get('para_birimi') or 'TL',
                        'Ödeme Yöntemi': ai_result.get('odeme_yontemi') or 'N/A',
                        'Fiş No': ai_result.get('fis_no') or 'N/A',
                        'Vergi No': ai_result.get('vergi_no') or 'N/A',
                        'Notlar': ai_result.get('notlar') or '',
                        'Durum': '✨ AI Analiz - Başarılı'
                    }
                    
                    logger.info(f"✨ OpenAI analizi başarılı: {filename}")
                    logger.debug(f"AI çıkarılan veri: {result}")
                    
                    return result
                else:
                    logger.warning(f"OpenAI analizi başarısız, regex'e geçiliyor: {filename}")
                    
            except Exception as e:
                logger.error(f"OpenAI analiz hatası, regex'e geçiliyor: {str(e)}")
        
        # Regex ile klasik analiz (fallback)
        amount, currency = self.extract_amount(text)
        date = self.extract_date(text)
        company = self.extract_company(text)
        receipt_type = self.extract_type(text)
        
        # Durum belirleme
        status = "Başarılı"
        if amount is None:
            status = "Tutar bulunamadı"
        elif company == "Bilinmeyen Firma":
            status = "Firma belirsiz"
        
        result = {
            'Dosya Adı': filename,
            'Tarih': date or 'N/A',
            'Saat': 'N/A',
            'Firma': company,
            'Şube': 'N/A',
            'Tür': receipt_type,
            'Tutar': amount if amount else 0.0,
            'KDV': 0.0,
            'Para Birimi': currency or 'N/A',
            'Ödeme Yöntemi': 'N/A',
            'Fiş No': 'N/A',
            'Vergi No': 'N/A',
            'Notlar': '',
            'Durum': status
        }
        
        logger.info(f"Veri çıkarma tamamlandı: {filename} - {status}")
        logger.debug(f"Çıkarılan veri: {result}")
        
        return result

