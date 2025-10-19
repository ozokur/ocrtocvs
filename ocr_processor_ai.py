"""
AI OCR işlemleri modülü - PaddleOCR kullanarak görüntülerden metin çıkarma
"""
import os
import numpy as np
from PIL import Image
import cv2
from logger import setup_logger

logger = setup_logger(__name__)

# PaddleOCR'ı lazy import (isteğe bağlı kullanım için)
try:
    from paddleocr import PaddleOCR
    PADDLEOCR_AVAILABLE = True
    logger.info("PaddleOCR başarıyla import edildi")
except ImportError as e:
    PADDLEOCR_AVAILABLE = False
    logger.warning(f"PaddleOCR import edilemedi: {e}")


class AIProcessor:
    """AI tabanlı OCR işlemlerini yöneten sınıf"""
    
    def __init__(self, use_angle_cls=True, lang='en', use_gpu=False):
        """
        AI OCR Processor başlatıcı
        
        Args:
            use_angle_cls: Metin yönlendirme sınıflandırması kullan
            lang: Dil kodu ('en' veya 'ch' için Çince, 'tr' için Türkçe vb)
            use_gpu: GPU kullan (varsa)
        """
        if not PADDLEOCR_AVAILABLE:
            raise ImportError("PaddleOCR kurulu değil. pip install paddleocr ile kurun.")
        
        logger.info(f"AI OCR Processor başlatılıyor (dil: {lang}, GPU: {use_gpu})")
        
        try:
            # PaddleOCR'ı başlat
            self.ocr = PaddleOCR(
                use_angle_cls=use_angle_cls,
                lang=lang,
                use_gpu=use_gpu,
                show_log=False  # PaddleOCR log'larını gizle
            )
            logger.info("PaddleOCR modeli yüklendi")
            
        except Exception as e:
            logger.error(f"PaddleOCR başlatma hatası: {str(e)}")
            raise
    
    def extract_text(self, image_path):
        """
        Görüntüden AI OCR ile metin çıkarır
        
        Args:
            image_path: Görüntü dosya yolu
            
        Returns:
            str: Çıkarılan metin
        """
        try:
            logger.info(f"AI OCR işlemi başladı: {image_path}")
            
            # PaddleOCR ile OCR yap
            result = self.ocr.ocr(image_path, cls=True)
            
            if not result or not result[0]:
                logger.warning(f"Metin bulunamadı: {image_path}")
                return ""
            
            # Sonuçları birleştir
            text_lines = []
            for line in result[0]:
                if line and len(line) >= 2:
                    text = line[1][0]  # Metin
                    confidence = line[1][1]  # Güven skoru
                    
                    # Düşük güven skorlarını filtrele (opsiyonel)
                    if confidence > 0.5:
                        text_lines.append(text)
                        logger.debug(f"Tespit edilen: '{text}' (güven: {confidence:.2f})")
            
            full_text = '\n'.join(text_lines)
            
            logger.info(f"AI OCR tamamlandı: {image_path} - {len(full_text)} karakter çıkarıldı")
            logger.debug(f"Çıkarılan metin: {full_text[:200]}...")
            
            return full_text
            
        except Exception as e:
            logger.error(f"AI OCR hatası ({image_path}): {str(e)}")
            return ""
    
    def extract_text_with_boxes(self, image_path):
        """
        Görüntüden metin ve konum bilgilerini çıkarır
        
        Args:
            image_path: Görüntü dosya yolu
            
        Returns:
            list: [(metin, koordinatlar, güven_skoru), ...]
        """
        try:
            logger.debug(f"AI OCR (detaylı) başladı: {image_path}")
            
            result = self.ocr.ocr(image_path, cls=True)
            
            if not result or not result[0]:
                return []
            
            detailed_results = []
            for line in result[0]:
                if line and len(line) >= 2:
                    box = line[0]  # Koordinatlar [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
                    text = line[1][0]  # Metin
                    confidence = line[1][1]  # Güven skoru
                    
                    detailed_results.append({
                        'text': text,
                        'box': box,
                        'confidence': confidence
                    })
            
            logger.debug(f"AI OCR (detaylı) tamamlandı: {len(detailed_results)} metin bloğu")
            return detailed_results
            
        except Exception as e:
            logger.error(f"AI OCR (detaylı) hatası ({image_path}): {str(e)}")
            return []
    
    def process_directory(self, directory_path, supported_extensions):
        """
        Klasördeki tüm görüntüleri AI OCR ile işler
        
        Args:
            directory_path: Klasör yolu
            supported_extensions: Desteklenen dosya uzantıları listesi
            
        Returns:
            dict: {dosya_adı: çıkarılan_metin} şeklinde sözlük
        """
        results = {}
        
        try:
            logger.info(f"Klasör işleme başladı (AI OCR): {directory_path}")
            
            # Klasördeki dosyaları listele
            files = [f for f in os.listdir(directory_path) 
                    if os.path.isfile(os.path.join(directory_path, f))]
            
            # Görüntü dosyalarını filtrele
            image_files = [f for f in files 
                          if os.path.splitext(f)[1].lower() in supported_extensions]
            
            logger.info(f"{len(image_files)} görüntü dosyası bulundu")
            
            # Her görüntüyü işle
            for idx, filename in enumerate(image_files, 1):
                file_path = os.path.join(directory_path, filename)
                logger.info(f"İşleniyor ({idx}/{len(image_files)}): {filename}")
                
                text = self.extract_text(file_path)
                results[filename] = text
            
            logger.info(f"Klasör işleme tamamlandı (AI OCR): {len(results)} dosya işlendi")
            
        except Exception as e:
            logger.error(f"Klasör işleme hatası (AI OCR): {str(e)}")
        
        return results
    
    def compare_with_tesseract(self, image_path, tesseract_result):
        """
        AI OCR sonucunu Tesseract ile karşılaştırır (debug amaçlı)
        
        Args:
            image_path: Görüntü dosya yolu
            tesseract_result: Tesseract OCR sonucu
            
        Returns:
            dict: Karşılaştırma sonuçları
        """
        try:
            ai_result = self.extract_text(image_path)
            
            comparison = {
                'tesseract_length': len(tesseract_result),
                'ai_length': len(ai_result),
                'tesseract_text': tesseract_result[:200],
                'ai_text': ai_result[:200],
                'difference_percent': abs(len(ai_result) - len(tesseract_result)) / max(len(tesseract_result), len(ai_result), 1) * 100
            }
            
            logger.debug(f"Karşılaştırma: Tesseract={comparison['tesseract_length']} char, "
                        f"AI={comparison['ai_length']} char, "
                        f"Fark={comparison['difference_percent']:.1f}%")
            
            return comparison
            
        except Exception as e:
            logger.error(f"Karşılaştırma hatası: {str(e)}")
            return {}


def is_paddleocr_available():
    """PaddleOCR'ın kullanılabilir olup olmadığını kontrol eder"""
    return PADDLEOCR_AVAILABLE

