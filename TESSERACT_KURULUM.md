# Tesseract Kurulum Durumu

## ✅ Kurulum Tamamlandı

**Tesseract Versiyonu:** 5.5.0.20241111  
**Kurulum Yolu:** `C:\Program Files\Tesseract-OCR\tesseract.exe`  
**Durum:** Çalışıyor ✓

## Yüklü Dil Paketleri

- ✅ **eng** - İngilizce (kurulu)
- ⚠️ **tur** - Türkçe (henüz kurulmadı)

## Türkçe Dil Paketi İçin (Opsiyonel)

Türkçe karakterleri daha iyi tanımak için Türkçe dil paketini ekleyebilirsiniz:

### Manuel Kurulum:

1. [Türkçe dil paketini indirin](https://github.com/tesseract-ocr/tessdata/raw/main/tur.traineddata)

2. Dosyayı şu klasöre kopyalayın:
   ```
   C:\Program Files\Tesseract-OCR\tessdata\
   ```

3. `config.py` dosyasında şu satırı değiştirin:
   ```python
   TESSERACT_LANG = 'eng'  # Bunu değiştirin
   ```
   Şöyle yapın:
   ```python
   TESSERACT_LANG = 'tur+eng'  # Türkçe + İngilizce
   ```

### Not:

Program şu anda İngilizce OCR ile çalışıyor ve çoğu Türk fişinde kullanılan sayılar ve temel metinler için yeterlidir. Türkçe karakterler (ç, ğ, ı, ş, ü, ö) içeren metinler için Türkçe dil paketi önerilir.

## Test

Tesseract'ın çalıştığını doğrulayın:

```bash
python test_app.py
```

Veya uygulamayı başlatın:

```bash
python main.py
```

---

**Kurulum Tarihi:** 19 Ekim 2025  
**Durum:** ✅ Başarılı

