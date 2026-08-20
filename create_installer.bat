@echo off
echo ========================================
echo СОЗДАНИЕ УСТАНОВЩИКА PNG TUBER
echo ========================================

echo.
echo Шаг 1: Установка зависимостей...
pip install pyinstaller pillow

echo.
echo Шаг 2: Создание EXE файла...
pyinstaller --onefile --windowed --icon=icon.ico --name=PNGTuber --add-data="my_photos;my_photos" main.py

echo.
echo Шаг 3: Копирование файлов...
mkdir release
copy dist\PNGTuber.exe release\
xcopy my_photos release\my_photos\ /E /I

echo.
echo Шаг 4: Создание архива...
powershell Compress-Archive -Path release\* -DestinationPath PNGTuber_portable.zip -Force

echo.
echo ========================================
echo ГОТОВО! Файлы в папке release/
echo ========================================
pause
