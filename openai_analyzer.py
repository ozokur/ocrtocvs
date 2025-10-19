"""
OpenAI GPT-4o-mini ile akıllı fiş analizi
"""
import os
import base64
from openai import OpenAI
from logger import setup_logger

logger = setup_logger(__name__)


class OpenAIAnalyzer:
    """OpenAI GPT-4o-mini ile fiş analizi yapan sınıf"""
    
    def __init__(self, api_key=None, model="gpt-4o-mini"):
        """
        OpenAI Analyzer başlatıcı
        
        Args:
            api_key: OpenAI API key
            model: Kullanılacak model (varsayılan: gpt-4o-mini - en ucuz)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.model = model
        
        if not self.api_key:
            raise ValueError("OpenAI API key bulunamadı! .env dosyasını kontrol edin.")
        
        self.client = OpenAI(api_key=self.api_key)
        logger.info(f"OpenAI Analyzer başlatıldı (model: {model})")
    
    def encode_image(self, image_path):
        """
        Görüntüyü base64'e çevirir
        
        Args:
            image_path: Görüntü dosya yolu
            
        Returns:
            str: Base64 encoded görüntü
        """
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            logger.error(f"Görüntü encode hatası: {str(e)}")
            return None
    
    def analyze_receipt_from_text(self, ocr_text, filename):
        """
        OCR metninden fiş bilgilerini akıllıca çıkarır
        
        Args:
            ocr_text: Tesseract'tan gelen OCR metni
            filename: Dosya adı
            
        Returns:
            dict: Analiz sonuçları
        """
        try:
            logger.info(f"OpenAI analizi başladı: {filename}")
            
            prompt = f"""Sen bir profesyonel fiş ve fatura analiz uzmanısın. Aşağıdaki OCR metninden DETAYLI bilgileri çıkar:

1. **Firma**: Fişi kesen işletme/mağaza adı (tam adı)
2. **Şube**: Varsa şube bilgisi
3. **Tutar**: Toplam tutar (sadece sayı, örn: 125.50)
4. **Para Birimi**: TL, USD, EUR vb.
5. **Tarih**: İşlem tarihi (DD/MM/YYYY formatında)
6. **Saat**: İşlem saati (varsa, HH:MM formatında)
7. **Tür**: Fiş türü (market, akaryakıt, restoran, elektronik, eczane, giyim, kafe, diğer)
8. **Ödeme Yöntemi**: Nakit, Kredi Kartı, Banka Kartı vb. (varsa)
9. **Vergi No**: Firma vergi numarası (varsa)
10. **Fiş No**: Fiş/fatura numarası (varsa)
11. **KDV**: KDV tutarı (varsa)
12. **Notlar**: Özel notlar veya ek bilgiler (varsa)

OCR Metni:
{ocr_text}

Yanıtı sadece şu JSON formatında ver (başka açıklama ekleme):
{{
    "firma": "...",
    "sube": "...",
    "tutar": 123.45,
    "para_birimi": "TL",
    "tarih": "DD/MM/YYYY",
    "saat": "HH:MM",
    "tur": "market",
    "odeme_yontemi": "...",
    "vergi_no": "...",
    "fis_no": "...",
    "kdv": 12.34,
    "notlar": "..."
}}

Eğer bir bilgi bulunamazsa null kullan. Sadece JSON döndür, başka açıklama ekleme."""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Sen bir fiş ve fatura analiz uzmanısın. Verilen metinden firma, tutar, tarih ve tür bilgilerini doğru bir şekilde çıkarırsın."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,  # Düşük temperature = daha tutarlı sonuçlar
                max_tokens=200
            )
            
            result_text = response.choices[0].message.content.strip()
            logger.debug(f"OpenAI yanıtı: {result_text}")
            
            # JSON'u parse et
            import json
            # JSON kısmını bul ve parse et
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0].strip()
            
            result = json.loads(result_text)
            
            logger.info(f"OpenAI analizi tamamlandı: {filename}")
            return result
            
        except Exception as e:
            logger.error(f"OpenAI analiz hatası: {str(e)}")
            return None
    
    def analyze_receipt_from_image(self, image_path, filename):
        """
        Görüntüden doğrudan fiş analizi yapar (Vision API)
        NOT: Bu daha pahalıdır, OCR+Text analizi daha ucuzdur
        
        Args:
            image_path: Görüntü dosya yolu
            filename: Dosya adı
            
        Returns:
            dict: Analiz sonuçları
        """
        try:
            logger.info(f"OpenAI Vision analizi başladı: {filename}")
            
            # Görüntüyü encode et
            base64_image = self.encode_image(image_path)
            if not base64_image:
                return None
            
            prompt = """Bu fişten/makbuzdan DETAYLI bilgileri çıkar:

1. **Firma**: İşletme/mağaza adı (tam adı)
2. **Şube**: Şube bilgisi (varsa)
3. **Tutar**: TOPLAM tutar (sadece sayı, örn: 125.50)
4. **KDV**: KDV tutarı (varsa)
5. **Para Birimi**: TL, USD, EUR vb.
6. **Tarih**: İşlem tarihi (DD/MM/YYYY formatında)
7. **Saat**: İşlem saati (HH:MM formatında, varsa)
8. **Tür**: Fiş türü (market, akaryakıt, restoran, elektronik, eczane, giyim, kafe, diğer)
9. **Ödeme Yöntemi**: Nakit, Kredi Kartı, Banka Kartı (varsa)
10. **Fiş No**: Fiş/fatura numarası (varsa)
11. **Vergi No**: Firma vergi numarası (varsa)
12. **Notlar**: Özel notlar (varsa)

SADECE JSON formatında yanıt ver (açıklama ekleme):
{
    "firma": "...",
    "sube": "...",
    "tutar": 123.45,
    "kdv": 12.34,
    "para_birimi": "TL",
    "tarih": "DD/MM/YYYY",
    "saat": "HH:MM",
    "tur": "market",
    "odeme_yontemi": "...",
    "fis_no": "...",
    "vergi_no": "...",
    "notlar": "..."
}

Bulunamayan bilgiler için null kullan."""

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Vision destekli model
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                temperature=0.1,
                max_tokens=200
            )
            
            result_text = response.choices[0].message.content.strip()
            logger.debug(f"OpenAI Vision yanıtı: {result_text}")
            
            # JSON'u parse et
            import json
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0].strip()
            
            result = json.loads(result_text)
            
            logger.info(f"OpenAI Vision analizi tamamlandı: {filename}")
            return result
            
        except Exception as e:
            logger.error(f"OpenAI Vision analiz hatası: {str(e)}")
            return None
    
    def get_cost_estimate(self, input_tokens, output_tokens):
        """
        Maliyet tahmini (gpt-4o-mini fiyatları)
        
        Args:
            input_tokens: Giriş token sayısı
            output_tokens: Çıkış token sayısı
            
        Returns:
            float: Tahmini maliyet (USD)
        """
        # gpt-4o-mini fiyatları (Ekim 2024)
        input_cost = 0.150 / 1_000_000  # $0.150 per 1M input tokens
        output_cost = 0.600 / 1_000_000  # $0.600 per 1M output tokens
        
        total_cost = (input_tokens * input_cost) + (output_tokens * output_cost)
        return total_cost


def is_openai_available():
    """OpenAI'ın kullanılabilir olup olmadığını kontrol eder"""
    try:
        api_key = os.getenv('OPENAI_API_KEY')
        return api_key is not None and len(api_key) > 0
    except:
        return False

