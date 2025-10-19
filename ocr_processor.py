"""
OCR işlemleri modülü - Görüntülerden metin çıkarma
"""
import os
import sys
import pytesseract
from PIL import Image
import cv2
import numpy as np
from logger import setup_logger
from config import TESSERACT_LANG

# Windows için Tesseract yolunu ayarla
if sys.platform == 'win32':
    tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    if os.path.exists(tesseract_path):
        pytesseract.pytesseract.tesseract_cmd = tesseract_path

logger = setup_logger(__name__)


class OCRProcessor:
    """OCR işlemlerini yöneten sınıf"""
    
    def __init__(self):
        """OCR Processor başlatıcı"""
        self.lang = TESSERACT_LANG
        logger.info("OCR Processor başlatıldı")
        
    def preprocess_image(self, image_path):
        """
        Görüntüyü OCR için ön işlemden geçirir
        
        Args:
            image_path: Görüntü dosya yolu
            
        Returns:
            numpy.ndarray: İşlenmiş görüntü
        """
        try:
            logger.debug(f"Görüntü ön işleme başladı: {image_path}")
            
            # Görüntüyü oku
            img = cv2.imread(image_path)
            
            if img is None:
                logger.error(f"Görüntü okunamadı: {image_path}")
                return None
            
            # Gri tonlamaya çevir
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Gürültü azaltma
            denoised = cv2.fastNlMeansDenoising(gray)
            
            # Kontrast artırma (CLAHE)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            enhanced = clahe.apply(denoised)
            
            # Adaptive threshold
            binary = cv2.adaptiveThreshold(
                enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                cv2.THRESH_BINARY, 11, 2
            )
            
            logger.debug(f"Görüntü ön işleme tamamlandı: {image_path}")
            return binary
            
        except Exception as e:
            logger.error(f"Görüntü ön işleme hatası ({image_path}): {str(e)}")
            return None
    
    def extract_text(self, image_path):
        """
        Görüntüden OCR ile metin çıkarır
        
        Args:
            image_path: Görüntü dosya yolu
            
        Returns:
            str: Çıkarılan metin
        """
        try:
            logger.info(f"OCR işlemi başladı: {image_path}")
            
            # Görüntüyü ön işle
            processed_img = self.preprocess_image(image_path)
            
            if processed_img is None:
                # Ön işleme başarısız, orijinal görüntüyü dene
                logger.warning(f"Ön işleme başarısız, orijinal görüntü kullanılıyor: {image_path}")
                img = Image.open(image_path)
            else:
                # NumPy array'i PIL Image'a çevir
                img = Image.fromarray(processed_img)
            
            # OCR uygula
            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(
                img, 
                lang=self.lang, 
                config=custom_config
            )
            
            logger.info(f"OCR tamamlandı: {image_path} - {len(text)} karakter çıkarıldı")
            logger.debug(f"Çıkarılan metin: {text[:200]}...")  # İlk 200 karakter
            
            return text
            
        except Exception as e:
            logger.error(f"OCR hatası ({image_path}): {str(e)}")
            return ""
    
    def process_directory(self, directory_path, supported_extensions):
        """
        Klasördeki tüm görüntüleri işler
        
        Args:
            directory_path: Klasör yolu
            supported_extensions: Desteklenen dosya uzantıları listesi
            
        Returns:
            dict: {dosya_adı: çıkarılan_metin} şeklinde sözlük
        """
        results = {}
        
        try:
            logger.info(f"Klasör işleme başladı: {directory_path}")
            
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
            
            logger.info(f"Klasör işleme tamamlandı: {len(results)} dosya işlendi")
            
        except Exception as e:
            logger.error(f"Klasör işleme hatası: {str(e)}")
        
        return results

