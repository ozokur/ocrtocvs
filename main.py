"""
OCR to CSV - Fiş Okuyucu
Ana uygulama dosyası
"""
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from threading import Thread
from datetime import datetime
from logger import setup_logger
from config import VERSION, APP_NAME, SUPPORTED_IMAGE_EXTENSIONS, USE_AI_OCR
from ocr_processor import OCRProcessor
from ocr_processor_vision import VisionOnlyProcessor
from data_extractor import DataExtractor
from csv_reporter import CSVReporter
from excel_manager import ExcelManager

# AI OCR modülünü import et (varsa)
try:
    from ocr_processor_ai import AIProcessor, is_paddleocr_available
    AI_AVAILABLE = is_paddleocr_available()
except ImportError:
    AI_AVAILABLE = False

logger = setup_logger(__name__)


class OCRApp:
    """Ana uygulama sınıfı"""
    
    def __init__(self, root):
        """
        Uygulama başlatıcı
        
        Args:
            root: Tkinter root penceresi
        """
        self.root = root
        self.root.title(f"{APP_NAME} v{VERSION}")
        self.root.geometry("700x550")
        self.root.resizable(False, False)
        
        # OCR motoru seçimi - Vision mode kontrolü
        try:
            from config_openai import OPENAI_ANALYSIS_MODE, SKIP_TESSERACT
            self.vision_mode = (OPENAI_ANALYSIS_MODE == "vision" and SKIP_TESSERACT)
        except:
            self.vision_mode = False
        
        self.use_ai_ocr = False  # Varsayılan değer (hatayı önlemek için)
        
        if self.vision_mode:
            # Vision-only mode: Tesseract gereksiz
            self.ocr_processor = VisionOnlyProcessor()
            logger.info("🎨 Vision-Only Mode: Sadece OpenAI Vision kullanılıyor (Tesseract YOK)")
        elif USE_AI_OCR and AI_AVAILABLE:
            try:
                from config import AI_OCR_LANG, AI_OCR_USE_GPU
                self.ocr_processor = AIProcessor(
                    use_angle_cls=True,
                    lang=AI_OCR_LANG,
                    use_gpu=AI_OCR_USE_GPU
                )
                self.use_ai_ocr = True
                logger.info("AI OCR (PaddleOCR) aktif")
            except Exception as e:
                logger.warning(f"AI OCR başlatılamadı, Tesseract'a geçiliyor: {e}")
                self.ocr_processor = OCRProcessor()
                self.use_ai_ocr = False
        else:
            self.ocr_processor = OCRProcessor()
            self.use_ai_ocr = False
            logger.info("Tesseract OCR aktif")
        
        self.data_extractor = DataExtractor()
        self.csv_reporter = CSVReporter()
        
        # Seçilen klasör ve Excel
        self.selected_directory = None
        self.selected_excel = None
        self.is_processing = False
        self.excel_manager = None
        
        # UI oluştur
        self._create_ui()
        
        logger.info(f"{APP_NAME} v{VERSION} başlatıldı")
        logger.info(f"OCR Motoru: {'AI (PaddleOCR)' if self.use_ai_ocr else 'Tesseract'}")
    
    def _create_ui(self):
        """Kullanıcı arayüzünü oluşturur"""
        
        # Başlık
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame, 
            text=APP_NAME, 
            font=('Arial', 20, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(pady=20)
        
        version_label = tk.Label(
            title_frame, 
            text=f"Versiyon {VERSION}", 
            font=('Arial', 10),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        version_label.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor='se')
        
        # Ana içerik frame
        content_frame = tk.Frame(self.root, padx=30, pady=30)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Açıklama ve sistem bilgisi
        if self.vision_mode:
            system_info = "🎨 Sadece OpenAI Vision (Tesseract kullanılmıyor)"
            cost_info = "💰 Maliyet: ~$0.01/fiş (Vision mode)"
        else:
            ocr_engine = "🤖 AI OCR (PaddleOCR)" if USE_AI_OCR and AI_AVAILABLE else "📝 Tesseract OCR"
            try:
                from config_openai import USE_OPENAI
                ai_status = "✨ OpenAI GPT-4o-mini" if USE_OPENAI else "Regex"
                cost_info = "💰 Maliyet: ~$0.0001/fiş"
            except:
                ai_status = "Regex"
                cost_info = "💰 Maliyet: Ücretsiz"
            system_info = f"🔍 OCR: {ocr_engine} + 🤖 Analiz: {ai_status}"
        
        info_text = (
            "Bu program, klasördeki fiş görüntülerini okuyarak\n"
            "firma, tutar ve tür bilgilerini çıkarır ve Excel raporu oluşturur.\n\n"
            f"⚡ Aktif Sistem: {system_info}\n"
            f"{cost_info}"
        )
        info_label = tk.Label(
            content_frame, 
            text=info_text,
            font=('Arial', 11),
            justify=tk.LEFT,
            wraplength=600
        )
        info_label.pack(pady=(0, 20))
        
        # Klasör seçimi
        folder_frame = tk.Frame(content_frame)
        folder_frame.pack(fill=tk.X, pady=10)
        
        self.folder_label = tk.Label(
            folder_frame,
            text="Klasör seçilmedi",
            font=('Arial', 10),
            fg='gray',
            anchor='w',
            relief=tk.SUNKEN,
            padx=10,
            pady=8
        )
        self.folder_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        select_button = tk.Button(
            folder_frame,
            text="Klasör Seç",
            font=('Arial', 11),
            bg='#3498db',
            fg='white',
            padx=20,
            pady=8,
            command=self._select_folder,
            cursor='hand2'
        )
        select_button.pack(side=tk.RIGHT)
        
        # Excel seçimi (opsiyonel - update için)
        excel_frame = tk.Frame(content_frame)
        excel_frame.pack(fill=tk.X, pady=10)
        
        excel_info = tk.Label(
            excel_frame,
            text="📊 Varolan Excel'e eklemek için (opsiyonel):",
            font=('Arial', 9),
            fg='#666'
        )
        excel_info.pack(anchor='w')
        
        excel_select_frame = tk.Frame(excel_frame)
        excel_select_frame.pack(fill=tk.X, pady=5)
        
        self.excel_label = tk.Label(
            excel_select_frame,
            text="Excel seçilmedi (yeni dosya oluşturulacak)",
            font=('Arial', 9),
            fg='gray',
            anchor='w',
            relief=tk.SUNKEN,
            padx=10,
            pady=6
        )
        self.excel_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        select_excel_button = tk.Button(
            excel_select_frame,
            text="Excel Seç",
            font=('Arial', 9),
            bg='#27ae60',
            fg='white',
            padx=15,
            pady=6,
            command=self._select_excel,
            cursor='hand2'
        )
        select_excel_button.pack(side=tk.RIGHT)
        
        clear_excel_button = tk.Button(
            excel_select_frame,
            text="Temizle",
            font=('Arial', 9),
            bg='#e74c3c',
            fg='white',
            padx=15,
            pady=6,
            command=self._clear_excel,
            cursor='hand2'
        )
        clear_excel_button.pack(side=tk.RIGHT, padx=(0, 5))
        
        # İşlem butonu
        self.process_button = tk.Button(
            content_frame,
            text="İşlemi Başlat",
            font=('Arial', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            padx=40,
            pady=12,
            command=self._start_processing,
            cursor='hand2',
            state=tk.DISABLED
        )
        self.process_button.pack(pady=30)
        
        # Progress bar
        self.progress_frame = tk.Frame(content_frame)
        self.progress_frame.pack(fill=tk.X, pady=10)
        
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            mode='indeterminate',
            length=640
        )
        self.progress_bar.pack()
        
        self.status_label = tk.Label(
            content_frame,
            text="",
            font=('Arial', 10),
            fg='#7f8c8d'
        )
        self.status_label.pack(pady=5)
        
        # Log alanı
        log_label = tk.Label(
            content_frame,
            text="İşlem Durumu:",
            font=('Arial', 10, 'bold'),
            anchor='w'
        )
        log_label.pack(fill=tk.X, pady=(10, 5))
        
        log_frame = tk.Frame(content_frame)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(log_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_text = tk.Text(
            log_frame,
            height=8,
            font=('Consolas', 9),
            yscrollcommand=scrollbar.set,
            state=tk.DISABLED,
            bg='#ecf0f1'
        )
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.log_text.yview)
    
    def _log_message(self, message):
        """
        Log mesajı ekler
        
        Args:
            message: Log mesajı
        """
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def _select_folder(self):
        """Klasör seçim dialogunu açar"""
        folder = filedialog.askdirectory(title="Fiş görüntülerinin bulunduğu klasörü seçin")
        
        if folder:
            self.selected_directory = folder
            self.folder_label.config(text=folder, fg='black')
            self.process_button.config(state=tk.NORMAL)
            logger.info(f"Klasör seçildi: {folder}")
            self._log_message(f"✓ Klasör seçildi: {folder}")
    
    def _select_excel(self):
        """Varolan Excel dosyası seçim dialogunu açar"""
        excel_file = filedialog.askopenfilename(
            title="Güncellenecek Excel dosyasını seçin (opsiyonel)",
            filetypes=[("Excel Dosyaları", "*.xlsx"), ("Tüm Dosyalar", "*.*")]
        )
        
        if excel_file:
            self.selected_excel = excel_file
            filename = os.path.basename(excel_file)
            self.excel_label.config(text=f"📊 {filename}", fg='green')
            logger.info(f"Excel seçildi: {excel_file}")
            self._log_message(f"✓ Excel seçildi: {filename} (güncelleme modu)")
    
    def _clear_excel(self):
        """Excel seçimini temizler"""
        self.selected_excel = None
        self.excel_manager = None
        self.excel_label.config(text="Excel seçilmedi (yeni dosya oluşturulacak)", fg='gray')
        logger.info("Excel seçimi temizlendi")
        self._log_message("✓ Excel seçimi temizlendi - yeni dosya oluşturulacak")
    
    def _start_processing(self):
        """İşlemi başlatır"""
        if self.is_processing:
            messagebox.showwarning("Uyarı", "İşlem zaten devam ediyor!")
            return
        
        if not self.selected_directory:
            messagebox.showerror("Hata", "Lütfen önce klasör seçin!")
            return
        
        # UI güncellemeleri
        self.is_processing = True
        self.process_button.config(state=tk.DISABLED)
        self.progress_bar.start()
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        # İşlemi ayrı thread'de başlat
        thread = Thread(target=self._process_images)
        thread.start()
    
    def _process_images(self):
        """Görüntüleri işler"""
        try:
            logger.info("İşlem başlatıldı")
            self._update_status("İşlem başlatılıyor...")
            self._log_message("İşlem başlatıldı...")
            
            # OCR/Görüntü listeleme işlemi
            if self.vision_mode:
                self._update_status("Görüntüler listeleniyor (Vision mode)...")
                self._log_message("\n🎨 Görüntüler listeleniyor (Tesseract atlandı - Vision direkt işleyecek)...")
            else:
                self._update_status("Görüntüler okunuyor (OCR)...")
                self._log_message("\n📷 Görüntüler okunuyor...")
            
            ocr_results = self.ocr_processor.process_directory(
                self.selected_directory,
                SUPPORTED_IMAGE_EXTENSIONS
            )
            
            if not ocr_results:
                raise Exception("Hiçbir görüntü bulunamadı!")
            
            if self.vision_mode:
                self._log_message(f"✓ {len(ocr_results)} görüntü bulundu (Vision ile analiz edilecek)")
            else:
                self._log_message(f"✓ {len(ocr_results)} görüntü okundu")
            
            # Veri çıkarma
            self._update_status("Fiş bilgileri çıkarılıyor...")
            
            # Analiz mesajı
            if self.vision_mode:
                self._log_message("\n🎨 OpenAI Vision ile görüntüler analiz ediliyor...")
                self._log_message("   (Tesseract kullanılmıyor - direkt Vision API)")
            else:
                try:
                    from config_openai import USE_OPENAI
                    if USE_OPENAI:
                        self._log_message("\n✨ OpenAI GPT-4o-mini ile akıllı analiz ediliyor...")
                    else:
                        self._log_message("\n🔍 Fiş bilgileri analiz ediliyor...")
                except:
                    self._log_message("\n🔍 Fiş bilgileri analiz ediliyor...")
            
            data_list = []
            for filename, text in ocr_results.items():
                # Görüntü yolunu da gönder (OpenAI Vision için)
                image_path = os.path.join(self.selected_directory, filename)
                data = self.data_extractor.extract_all(filename, text, image_path)
                data_list.append(data)
            
            self._log_message(f"✓ {len(data_list)} fiş analiz edildi")
            
            # Excel Manager'ı başlat
            if self.selected_excel:
                self._log_message(f"\n📊 Varolan Excel güncelleniyor: {os.path.basename(self.selected_excel)}")
                self.excel_manager = ExcelManager(self.selected_excel)
            else:
                self._log_message("\n📊 Yeni Excel oluşturuluyor...")
                self.excel_manager = ExcelManager()
            
            # Mükerrer kontrol ve ekleme
            self._update_status("Mükerrer kontrol yapılıyor...")
            added, duplicates = self.excel_manager.add_records(data_list)
            
            if duplicates > 0:
                self._log_message(f"⚠️ {duplicates} mükerrer kayıt atlandı")
            self._log_message(f"✓ {added} yeni kayıt eklendi")
            
            # Excel raporu oluştur
            self._update_status("Excel raporu oluşturuluyor...")
            self._log_message("\n📊 Excel raporu oluşturuluyor...")
            
            # Excel'i kaydet
            excel_output = os.path.join(
                self.selected_directory,
                f"fis_raporu_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            )
            
            if self.selected_excel:
                # Varolan dosyayı güncelle
                excel_output = self.selected_excel
            
            excel_path = self.excel_manager.save_to_excel(excel_output, styled=True)
            
            if excel_path:
                self._log_message(f"✓ Excel raporu: {os.path.basename(excel_path)}")
            
            # İstatistikleri göster
            stats = self.excel_manager.get_statistics()
            if stats:
                self._log_message("\n📈 İstatistikler:")
                self._log_message(f"  • Toplam kayıt: {stats.get('total_count', 0)}")
                self._log_message(f"  • Toplam tutar: {stats.get('total_amount', 0):.2f} TL")
                self._log_message(f"  • AI ile analiz: {stats.get('ai_analyzed', 0)}")
                self._log_message(f"  • Farklı firma: {stats.get('unique_companies', 0)}")
            
            # Başarı mesajı
            self._update_status("İşlem tamamlandı!")
            self._log_message("\n✅ İşlem başarıyla tamamlandı!")
            
            # Başarı mesajı
            message = f"İşlem tamamlandı!\n\n"
            message += f"📊 Analiz edilen: {len(data_list)} fiş\n"
            message += f"✅ Eklenen: {added} yeni kayıt\n"
            if duplicates > 0:
                message += f"⚠️ Mükerrer: {duplicates} kayıt atlandı\n"
            message += f"\n💰 Toplam tutar: {stats.get('total_amount', 0):.2f} TL\n"
            message += f"📁 Rapor: {os.path.basename(excel_path)}"
            
            self.root.after(0, lambda: messagebox.showinfo("Başarılı", message))
            
            logger.info("İşlem başarıyla tamamlandı")
            
        except Exception as e:
            error_msg = f"Hata: {str(e)}"
            logger.error(error_msg)
            self._update_status("Hata oluştu!")
            self._log_message(f"\n❌ {error_msg}")
            
            self.root.after(0, lambda: messagebox.showerror("Hata", error_msg))
        
        finally:
            # UI güncellemeleri
            self.root.after(0, self._processing_finished)
    
    def _update_status(self, message):
        """
        Durum mesajını günceller
        
        Args:
            message: Durum mesajı
        """
        self.root.after(0, lambda: self.status_label.config(text=message))
    
    def _processing_finished(self):
        """İşlem bittiğinde UI'yi günceller"""
        self.is_processing = False
        self.progress_bar.stop()
        self.process_button.config(state=tk.NORMAL)


def main():
    """Ana fonksiyon"""
    try:
        # Tkinter uygulamasını başlat
        root = tk.Tk()
        app = OCRApp(root)
        root.mainloop()
        
    except Exception as e:
        logger.critical(f"Uygulama başlatma hatası: {str(e)}")
        messagebox.showerror("Kritik Hata", f"Uygulama başlatılamadı:\n{str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

