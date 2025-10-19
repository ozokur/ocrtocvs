#!/bin/bash

echo "================================"
echo "OCR to CSV - Fiş Okuyucu v1.0.0"
echo "================================"
echo ""
echo "Uygulama başlatılıyor..."
echo ""

python3 main.py

if [ $? -ne 0 ]; then
    echo ""
    echo "HATA: Uygulama başlatılırken bir hata oluştu!"
    echo ""
    echo "Lütfen aşağıdaki adımları kontrol edin:"
    echo "1. Python yüklü mü? (python3 --version)"
    echo "2. Gerekli paketler yüklü mü? (pip3 install -r requirements.txt)"
    echo "3. Tesseract OCR yüklü mü? (tesseract --version)"
    echo ""
    read -p "Devam etmek için Enter'a basın..."
fi

