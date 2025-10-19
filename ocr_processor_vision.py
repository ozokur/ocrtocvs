"""
Vision-only OCR - Sadece OpenAI Vision kullanır, Tesseract gereksiz
"""
import os
from logger import setup_logger

logger = setup_logger(__name__)


class VisionOnlyProcessor:
    """Sadece OpenAI Vision kullanan sınıf - Tesseract yok"""
    
    def __init__(self):
        """Vision Only Processor başlatıcı"""
        logger.info("Vision-Only Processor başlatıldı (Tesseract kullanılmıyor)")
    
    def extract_text(self, image_path):
        """
        Bu modda metin çıkarmaya gerek yok - Vision direkt görüntü analiz eder
        
        Args:
            image_path: Görüntü dosya yolu
            
        Returns:
            str: Boş string (Vision mode için gerek yok)
        """
        logger.debug(f"Vision mode: {image_path} - Tesseract atlandı")
        return ""  # Vision direkt görüntüyü işler
    
    def process_directory(self, directory_path, supported_extensions):
        """
        Klasördeki görüntüleri listeler (metin çıkarmaz)
        
        Args:
            directory_path: Klasör yolu
            supported_extensions: Desteklenen dosya uzantıları listesi
            
        Returns:
            dict: {dosya_adı: ""} şeklinde sözlük (metin boş)
        """
        results = {}
        
        try:
            logger.info(f"Klasör tarama başladı (Vision-only): {directory_path}")
            
            # Klasördeki dosyaları listele
            files = [f for f in os.listdir(directory_path) 
                    if os.path.isfile(os.path.join(directory_path, f))]
            
            # Görüntü dosyalarını filtrele
            image_files = [f for f in files 
                          if os.path.splitext(f)[1].lower() in supported_extensions]
            
            logger.info(f"{len(image_files)} görüntü dosyası bulundu")
            
            # Dosya listesini döndür (metin çıkarma yok)
            for filename in image_files:
                results[filename] = ""  # Vision direkt görüntüyü işleyecek
            
            logger.info(f"Dosya listesi hazır: {len(results)} dosya")
            
        except Exception as e:
            logger.error(f"Dosya listeleme hatası: {str(e)}")
        
        return results

