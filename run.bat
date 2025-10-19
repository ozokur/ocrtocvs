@echo off
echo ================================
echo OCR to CSV - Fis Okuyucu v1.0.0
echo ================================
echo.
echo Uygulama baslatiliyor...
echo.

python main.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo HATA: Uygulama baslatilirken bir hata olustu!
    echo.
    echo Lutfen asagidaki adimlari kontrol edin:
    echo 1. Python yuklu mu? (python --version)
    echo 2. Gerekli paketler yuklu mu? (pip install -r requirements.txt)
    echo 3. Tesseract OCR yuklu mu? (tesseract --version)
    echo.
    pause
)

