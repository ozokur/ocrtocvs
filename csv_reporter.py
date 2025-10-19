"""
CSV rapor oluşturma modülü
"""
import os
import pandas as pd
from datetime import datetime
from logger import setup_logger
from config import CSV_DELIMITER, CSV_ENCODING, OUTPUT_FIELDS

logger = setup_logger(__name__)


class CSVReporter:
    """CSV rapor oluşturan sınıf"""
    
    def __init__(self):
        """CSV Reporter başlatıcı"""
        self.delimiter = CSV_DELIMITER
        self.encoding = CSV_ENCODING
        logger.info("CSV Reporter başlatıldı")
    
    def create_report(self, data_list, output_directory):
        """
        Veri listesinden CSV raporu oluşturur
        
        Args:
            data_list: Fiş verilerini içeren liste
            output_directory: Çıktı klasörü
            
        Returns:
            str: Oluşturulan CSV dosya yolu
        """
        try:
            logger.info("CSV rapor oluşturma başladı")
            
            if not data_list:
                logger.warning("Veri listesi boş, rapor oluşturulamadı")
                return None
            
            # DataFrame oluştur
            df = pd.DataFrame(data_list)
            
            # Sütun sırasını ayarla
            df = df[OUTPUT_FIELDS]
            
            # Tutar sütununu formatla
            df['Tutar'] = df['Tutar'].apply(lambda x: f"{x:.2f}" if isinstance(x, (int, float)) else x)
            
            # Çıktı dosya adı oluştur
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"fis_raporu_{timestamp}.csv"
            output_path = os.path.join(output_directory, output_filename)
            
            # CSV dosyasını kaydet
            df.to_csv(
                output_path, 
                index=False, 
                sep=self.delimiter, 
                encoding=self.encoding
            )
            
            logger.info(f"CSV rapor oluşturuldu: {output_path}")
            logger.info(f"Toplam kayıt sayısı: {len(df)}")
            
            # Özet istatistikler
            self._log_statistics(df)
            
            return output_path
            
        except Exception as e:
            logger.error(f"CSV rapor oluşturma hatası: {str(e)}")
            return None
    
    def _log_statistics(self, df):
        """
        Rapor istatistiklerini loglar
        
        Args:
            df: pandas DataFrame
        """
        try:
            logger.info("=== Rapor İstatistikleri ===")
            
            # Toplam tutar
            total_amount = df['Tutar'].apply(
                lambda x: float(x) if isinstance(x, str) else x
            ).sum()
            logger.info(f"Toplam tutar: {total_amount:.2f} TL")
            
            # Başarılı/başarısız işlemler
            status_counts = df['Durum'].value_counts()
            for status, count in status_counts.items():
                logger.info(f"{status}: {count} adet")
            
            # Tür dağılımı
            type_counts = df['Tür'].value_counts()
            logger.info("Tür dağılımı:")
            for receipt_type, count in type_counts.items():
                logger.info(f"  {receipt_type}: {count} adet")
            
            logger.info("=== İstatistikler Sonu ===")
            
        except Exception as e:
            logger.error(f"İstatistik hesaplama hatası: {str(e)}")
    
    def create_summary_report(self, data_list, output_directory):
        """
        Özet rapor oluşturur
        
        Args:
            data_list: Fiş verilerini içeren liste
            output_directory: Çıktı klasörü
            
        Returns:
            str: Oluşturulan özet dosya yolu
        """
        try:
            logger.info("Özet rapor oluşturma başladı")
            
            if not data_list:
                logger.warning("Veri listesi boş, özet rapor oluşturulamadı")
                return None
            
            df = pd.DataFrame(data_list)
            
            # Özet istatistikler
            summary = {
                'Toplam Fiş Sayısı': len(df),
                'Başarılı İşlem': len(df[df['Durum'] == 'Başarılı']),
                'Toplam Tutar': df['Tutar'].sum(),
                'Ortalama Tutar': df['Tutar'].mean(),
                'En Yüksek Tutar': df['Tutar'].max(),
                'En Düşük Tutar': df['Tutar'].min(),
            }
            
            # Özet dosyası oluştur
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            summary_filename = f"fis_ozeti_{timestamp}.txt"
            summary_path = os.path.join(output_directory, summary_filename)
            
            with open(summary_path, 'w', encoding='utf-8') as f:
                f.write("=" * 50 + "\n")
                f.write("FIŞ RAPORU ÖZETİ\n")
                f.write("=" * 50 + "\n\n")
                
                for key, value in summary.items():
                    if 'Tutar' in key:
                        f.write(f"{key}: {value:.2f} TL\n")
                    else:
                        f.write(f"{key}: {value}\n")
                
                f.write("\n" + "=" * 50 + "\n")
                f.write("TÜR DAĞILIMI\n")
                f.write("=" * 50 + "\n\n")
                
                type_counts = df['Tür'].value_counts()
                for receipt_type, count in type_counts.items():
                    percentage = (count / len(df)) * 100
                    f.write(f"{receipt_type}: {count} adet ({percentage:.1f}%)\n")
                
                f.write("\n" + "=" * 50 + "\n")
                f.write(f"Rapor Tarihi: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                f.write("=" * 50 + "\n")
            
            logger.info(f"Özet rapor oluşturuldu: {summary_path}")
            
            return summary_path
            
        except Exception as e:
            logger.error(f"Özet rapor oluşturma hatası: {str(e)}")
            return None

