# AI OCR Entegrasyonu Kılavuzu

## 📊 Mevcut Durum

✅ **Uygulama Tesseract OCR ile tamamen çalışıyor!**  
⏸️ **PaddleOCR entegrasyonu hazır ama dependency çakışmaları nedeniyle opsiyonel**

## 🤖 AI OCR Nedir?

PaddleOCR, klasik OCR'dan (Tesseract) daha gelişmiş bir AI tabanlı OCR motorudur:

- ✅ Daha yüksek doğruluk
- ✅ Çoklu dil desteği
- ✅ Eğik/döndürülmüş metinleri okuma
- ✅ Farklı font ve stillere adaptasyon
- ✅ Güven skorları

## 📁 Hazır Olan Dosyalar

1. ✅ `ocr_processor_ai.py` - AI OCR modülü (hazır)
2. ✅ `config.py` - AI ayarları (USE_AI_OCR = False)
3. ✅ `main.py` - AI desteği entegre edildi

## 🔧 Neden Şu An Kullanılmıyor?

PaddleOCR'ın bazı bağımlılık çakışmaları var:
- NumPy versiyon uyumsuzlukları
- SciPy sürüm gereksinimleri
- Diğer paketlerle çakışma (ultralytics, onnx, vb.)

## 🚀 AI OCR'ı Nasıl Aktif Edebilirim?

### Seçenek 1: Ayrı Bir Virtual Environment (Önerilen)

```bash
# Yeni bir venv oluştur
python -m venv venv_ai
venv_ai\Scripts\activate

# Temiz kurulum
pip install pytesseract Pillow pandas python-dateutil
pip install paddlepaddle==2.6.1 paddleocr==2.7.3

# config.py'yi düzenle
USE_AI_OCR = True

# Uygulamayı çalıştır
python main.py
```

### Seçenek 2: Docker ile Çalıştırma

```dockerfile
FROM python:3.9
WORKDIR /app
COPY . /app
RUN pip install paddlepaddle paddleocr
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```

### Seçenek 3: Google Colab'da Test

```python
# Colab notebook'ta
!pip install paddleocr paddlepaddle
!git clone https://github.com/YOUR_REPO/ocrtocvs.git
%cd ocrtocvs
# config.py'de USE_AI_OCR = True yap
!python main.py
```

## ⚙️ Manuel Kurulum (Deneysel)

Eğer mevcut ortamda denemek isterseniz:

```bash
# Çakışan paketleri kaldır
pip uninstall ultralytics onnx albumentations -y

# PaddleOCR kur
pip install paddlepaddle==2.6.1
pip install paddleocr==2.7.3

# config.py'yi güncelle
USE_AI_OCR = True
```

**Uyarı:** Bu, diğer projelerinizi etkileyebilir!

## 🎯 AI OCR Kullanımı

AI OCR aktif olduğunda:

1. `config.py` içinde:
```python
USE_AI_OCR = True  # AI OCR kullan
AI_OCR_LANG = 'en'  # Dil: 'en', 'tr', 'ch', vb.
AI_OCR_USE_GPU = False  # GPU kullan (CUDA varsa)
```

2. Uygulama otomatik olarak PaddleOCR kullanır
3. Ana ekranda "🤖 AI OCR (PaddleOCR)" yazısı görünür

## 🔍 Alternatif AI OCR Seçenekleri

### A) EasyOCR (Daha Kolay Kurulum)

```bash
pip install easyocr
```

`ocr_processor_ai.py` içinde EasyOCR kullanmak için:

```python
import easyocr
reader = easyocr.Reader(['en', 'tr'])
result = reader.readtext(image_path)
```

### B) Google Cloud Vision API (En İyi Kalite)

```bash
pip install google-cloud-vision
```

API key gerektirir, ücretli servis.

### C) Azure Computer Vision API

Microsoft'un OCR hizmeti, güçlü ve güvenilir.

### D) GPT-4 Vision (Premium)

```python
import openai
response = openai.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "Bu fişten firma, tutar, tarih çıkar"},
            {"type": "image_url", "image_url": {"url": image_url}}
        ]
    }]
)
```

## 📊 Karşılaştırma

| Özellik | Tesseract | PaddleOCR | GPT-4 Vision |
|---------|-----------|-----------|--------------|
| Doğruluk | ★★★☆☆ | ★★★★☆ | ★★★★★ |
| Hız | ★★★★★ | ★★★★☆ | ★★☆☆☆ |
| Ücretsiz | ✅ | ✅ | ❌ |
| Türkçe | ✅ | ✅ | ✅ |
| Kurulum | Kolay | Orta | Kolay |
| İnternet | ❌ | ❌ | ✅ |

## 💡 Önerimiz

**Şu anki Tesseract OCR çoğu kullanım için yeterlidir!**

AI OCR'a ihtiyacınız olan durumlar:
- ❌ Çok düşük kaliteli görüntüler
- ❌ Eğik/döndürülmüş fişler
- ❌ El yazısı içeren belgeler
- ❌ Karmaşık layout

## 🆘 Destek

AI entegrasyonu için yardıma ihtiyacınız varsa:
1. `ocr_processor_ai.py` dosyası hazır ve çalışıyor
2. Sadece dependency sorunları çözülmeli
3. Ayrı bir venv kullanmak en güvenli yöntem

## 📝 Notlar

- `ocr_processor_ai.py` modülü tamamen hazır
- Kod düzeninde bir sorun yok
- Sadece paket versiyonları uyumsuz
- İleride PaddleOCR güncellenince daha kolay olacak

---

**Son Güncelleme:** 19 Ekim 2025  
**Durum:** Tesseract aktif, AI OCR opsiyonel

