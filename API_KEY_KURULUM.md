# 🔑 OpenAI API Key Kurulumu

## 📋 Gereklilik

OpenAI Vision kullanmak için API key gereklidir.

## 🚀 Hızlı Kurulum

### 1. .env.local Dosyası Oluşturun

Proje klasöründe `.env.local` adında bir dosya oluşturun:

```bash
# Windows (PowerShell):
copy .env.example .env.local

# Linux/macOS:
cp .env.example .env.local
```

### 2. API Key'inizi Ekleyin

`.env.local` dosyasını açın ve API key'inizi yazın:

```
OPENAI_API_KEY=sk-proj-YOUR-API-KEY-HERE
OPENAI_MODEL=gpt-4o-mini
USE_OPENAI=True
```

### 3. Uygulamayı Başlatın

```bash
python main.py
```

Uygulama otomatik olarak `.env.local` dosyasından API key'i okuyacak!

## 🔒 Güvenlik

### ✅ Yapılanlar:
- `.env.local` dosyası `.gitignore`'a eklendi
- API key asla Git'e gitmeyecek
- Güvenli ve korumalı

### ❌ YAPMAYINIZ:
- API key'i doğrudan kod dosyasına yazmayın
- `.env.local` dosyasını commit etmeyin
- API key'i başkalarıyla paylaşmayın

## 📁 Dosya Yapısı

```
ocrtocvs/
├── .env.example      # Örnek şablon (Git'te)
├── .env.local        # Sizin API key'iniz (Git'te YOK)
├── .gitignore        # .env.local burada ignore edildi
└── config_openai.py  # API key'i .env.local'dan okur
```

## 🔍 Sorun Giderme

### "API key bulunamadı" Hatası

**Çözüm:**
1. `.env.local` dosyasının proje kök dizininde olduğundan emin olun
2. Dosya içinde `OPENAI_API_KEY=sk-proj-...` satırının olduğunu kontrol edin
3. Boşluk veya tırnak işareti olmadan yazın

### API Key Çalışmıyor

**Test edin:**
```bash
python test_openai.py
```

Eğer başarısız olursa:
1. API key'in doğru olduğunu kontrol edin
2. OpenAI hesabınızda kredi olduğunu kontrol edin
3. API key'in aktif olduğunu doğrulayın

## 💡 Alternatif: Environment Variable

`.env.local` yerine sistem environment variable kullanabilirsiniz:

### Windows:
```powershell
$env:OPENAI_API_KEY="sk-proj-YOUR-KEY"
python main.py
```

### Linux/macOS:
```bash
export OPENAI_API_KEY="sk-proj-YOUR-KEY"
python main.py
```

## 📊 API Key Nasıl Alınır?

1. [OpenAI Platform](https://platform.openai.com/) adresine gidin
2. Hesabınıza giriş yapın
3. **API Keys** bölümüne gidin
4. **Create new secret key** tıklayın
5. Key'i kopyalayın ve `.env.local` dosyasına yapıştırın

## 💰 Maliyet Kontrolü

API key'iniz için:
- [Usage Dashboard](https://platform.openai.com/usage) - Kullanım takibi
- [Billing](https://platform.openai.com/settings/organization/billing) - Fatura ayarları
- Limit koyabilirsiniz (örn: aylık $5)

## ⚠️ Önemli Notlar

1. **API key'inizi asla paylaşmayın**
2. **Git'e commit etmeyin**
3. **Screenshot'larda göstermeyin**
4. **Public'e atmayın**

## ✅ Güvenlik Kontrol Listesi

- [x] API key .env.local dosyasında
- [x] .env.local .gitignore'da
- [x] config_openai.py sadece environment variable okuyor
- [x] Örnek şablon .env.example olarak sağlandı

---

**Durum:** ✅ Güvenli Kurulum Hazır  
**API Key:** .env.local dosyasında (Git'te YOK)  
**Güvenlik:** ✅ Korumalı

