# Kurulum Kılavuzu

Bu doküman, OCR to CSV - Fiş Okuyucu uygulamasının detaylı kurulum adımlarını içerir.

## Windows Kurulumu

### 1. Python Kurulumu

1. [Python.org](https://www.python.org/downloads/) adresinden Python 3.8 veya üzeri sürümü indirin
2. Kurulum sırasında "Add Python to PATH" seçeneğini işaretleyin
3. Kurulumu tamamlayın
4. Komut satırında şunu çalıştırarak kontrol edin:
   ```
   python --version
   ```

### 2. Git Kurulumu (Opsiyonel)

1. [Git for Windows](https://git-scm.com/download/win) indirin ve kurun
2. Projeyi klonlayın:
   ```
   git clone https://github.com/KULLANICI_ADI/ocrtocvs.git
   cd ocrtocvs
   ```

Veya ZIP olarak indirin ve çıkartın.

### 3. Tesseract OCR Kurulumu

1. [Tesseract Windows installer](https://github.com/UB-Mannheim/tesseract/wiki) sayfasına gidin
2. En son sürümü indirin (örn: `tesseract-ocr-w64-setup-5.3.x.exe`)
3. Kurulum sırasında:
   - "Additional language data" seçeneğinde **Turkish** seçin
   - Kurulum yolunu not edin (varsayılan: `C:\Program Files\Tesseract-OCR`)
4. Kurulum tamamlandıktan sonra PATH'e eklendiğini kontrol edin:
   ```
   tesseract --version
   ```

**Eğer PATH'te yoksa:**
1. "Sistem Ortam Değişkenleri"ni açın
2. "Path" değişkenine şunu ekleyin: `C:\Program Files\Tesseract-OCR`
3. Komut satırını yeniden başlatın

**Alternatif:** Eğer PATH'e eklemek istemiyorsanız, `ocr_processor.py` dosyasının başına şunu ekleyin:

```python
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### 4. Python Paketlerini Yükleme

Proje klasöründe:

```bash
pip install -r requirements.txt
```

### 5. Uygulamayı Çalıştırma

```bash
python main.py
```

---

## Linux Kurulumu (Ubuntu/Debian)

### 1. Sistem Güncellemesi

```bash
sudo apt update
sudo apt upgrade
```

### 2. Python ve pip Kurulumu

```bash
sudo apt install python3 python3-pip
python3 --version
```

### 3. Tesseract OCR Kurulumu

```bash
sudo apt install tesseract-ocr
sudo apt install tesseract-ocr-tur  # Türkçe dil paketi
sudo apt install tesseract-ocr-eng  # İngilizce dil paketi

# Kontrol
tesseract --version
```

### 4. Gerekli Sistem Kütüphaneleri

OpenCV için:

```bash
sudo apt install libgl1-mesa-glx
sudo apt install libglib2.0-0
```

### 5. Projeyi İndirme

```bash
git clone https://github.com/KULLANICI_ADI/ocrtocvs.git
cd ocrtocvs
```

### 6. Python Paketlerini Yükleme

```bash
pip3 install -r requirements.txt
```

### 7. Uygulamayı Çalıştırma

```bash
python3 main.py
```

---

## macOS Kurulumu

### 1. Homebrew Kurulumu

Eğer Homebrew yüklü değilse:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Python Kurulumu

```bash
brew install python@3.11
python3 --version
```

### 3. Tesseract OCR Kurulumu

```bash
brew install tesseract
brew install tesseract-lang  # Tüm dil paketleri

# Veya sadece Türkçe
brew install tesseract --with-all-languages

# Kontrol
tesseract --version
```

### 4. Projeyi İndirme

```bash
git clone https://github.com/KULLANICI_ADI/ocrtocvs.git
cd ocrtocvs
```

### 5. Python Paketlerini Yükleme

```bash
pip3 install -r requirements.txt
```

### 6. Uygulamayı Çalıştırma

```bash
python3 main.py
```

---

## Virtual Environment Kullanımı (Önerilen)

Projenin kendi izole Python ortamında çalışması için:

### Windows:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

Virtual environment'tan çıkmak için:
```bash
deactivate
```

---

## Kurulum Sonrası Test

1. Uygulamayı başlatın: `python main.py`
2. "Klasör Seç" butonuna tıklayın
3. Örnek bir fiş görüntüsü içeren klasör seçin
4. "İşlemi Başlat" butonuna tıklayın
5. Raporların oluştuğunu kontrol edin

---

## Yaygın Sorunlar ve Çözümleri

### Sorun: "Tesseract is not installed or it's not in your PATH"

**Çözüm:**
- Tesseract'ın doğru kurulduğunu kontrol edin
- PATH'e eklendiğini kontrol edin
- Manuel olarak yolu belirtin (yukarıda anlatıldığı gibi)

### Sorun: "ImportError: No module named 'cv2'"

**Çözüm:**
```bash
pip install opencv-python
```

### Sorun: "Could not find pytesseract module"

**Çözüm:**
```bash
pip install pytesseract
```

### Sorun: Türkçe karakterler yanlış okuyor

**Çözüm:**
- Tesseract Türkçe dil paketinin kurulu olduğunu kontrol edin
- `config.py` içinde `TESSERACT_LANG = 'tur+eng'` olduğundan emin olun

### Sorun: GUI açılmıyor (Linux)

**Çözüm:**
```bash
sudo apt install python3-tk
```

---

## Geliştirme Ortamı Kurulumu

Projeyi geliştirmek için ek paketler:

```bash
pip install pytest pytest-cov
pip install black flake8
pip install pylint
```

---

## Güncelleme

Projeyi güncellemek için:

```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

---

## Kaldırma

### Windows:
1. Proje klasörünü silin
2. Python paketlerini kaldırın: `pip uninstall -r requirements.txt -y`
3. Tesseract'ı "Programlar ve Özellikler"den kaldırın

### Linux/macOS:
```bash
rm -rf ocrtocvs/
pip3 uninstall -r requirements.txt -y
# Tesseract kaldırma (opsiyonel):
# Ubuntu: sudo apt remove tesseract-ocr
# macOS: brew uninstall tesseract
```

---

## Destek

Kurulum sırasında sorun yaşarsanız:
1. Log dosyalarını kontrol edin (`logs/` klasörü)
2. GitHub'da issue açın
3. Hata mesajını ve sistem bilgilerinizi paylaşın

---

**Başarılı kurulumlar dileriz!** 🎉

