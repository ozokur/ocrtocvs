# Hızlı Başlangıç Kılavuzu

Bu kılavuz, uygulamayı 5 dakikada çalıştırmanız için hazırlanmıştır.

## 🚀 3 Adımda Başlangıç

### 1️⃣ Tesseract OCR'yi Yükleyin

**Windows:**
- [Buradan indirin](https://github.com/UB-Mannheim/tesseract/wiki) ve kurun
- Kurulum sırasında "Turkish" dil paketini seçin

**Linux:**
```bash
sudo apt-get install tesseract-ocr tesseract-ocr-tur
```

**macOS:**
```bash
brew install tesseract tesseract-lang
```

### 2️⃣ Python Paketlerini Yükleyin

Proje klasöründe şu komutu çalıştırın:

```bash
pip install -r requirements.txt
```

### 3️⃣ Uygulamayı Başlatın

**Windows:**
```bash
python main.py
```
veya `run.bat` dosyasına çift tıklayın

**Linux/macOS:**
```bash
python3 main.py
```
veya:
```bash
chmod +x run.sh
./run.sh
```

## 📝 İlk Kullanım

1. Açılan pencerede **"Klasör Seç"** butonuna tıklayın
2. Fiş görüntülerinin olduğu klasörü seçin
3. **"İşlemi Başlat"** butonuna tıklayın
4. İşlem bitince raporlar seçtiğiniz klasörde oluşur:
   - `fis_raporu_YYYYMMDD_HHMMSS.csv` - Detaylı rapor
   - `fis_ozeti_YYYYMMDD_HHMMSS.txt` - Özet istatistikler

## 🎯 İpuçları

### Daha İyi OCR Sonuçları İçin:
- ✅ Görüntüleri düz bir yüzeyde çekin
- ✅ Yeterli ışık kullanın
- ✅ Fişin tamamını çerçeveye alın
- ✅ Net ve odaklı çekin
- ❌ Bulanık veya eğik görüntülerden kaçının

### Desteklenen Formatlar:
- JPG/JPEG
- PNG
- BMP
- TIFF/TIF

## ❓ Sorun mu Yaşıyorsunuz?

### "Tesseract bulunamadı" hatası
Tesseract'ın PATH'te olduğundan emin olun veya `ocr_processor.py` dosyasına şunu ekleyin:

```python
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### "ModuleNotFoundError" hatası
Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

### GUI açılmıyor (Linux)
```bash
sudo apt install python3-tk
```

## 📚 Daha Fazla Bilgi

- Detaylı kurulum: [INSTALL.md](INSTALL.md)
- Tüm özellikler: [README.md](README.md)
- Versiyon geçmişi: [CHANGELOG.md](CHANGELOG.md)

## 🎉 Başarılar!

Artık fişlerinizi kolayca dijitalleştirebilirsiniz!

---

**İhtiyacınız olduğunda:**
- Log dosyaları: `logs/` klasörü
- Destek: GitHub Issues

