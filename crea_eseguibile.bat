@echo off
title Creazione Eseguibile MP3 Organizer
echo ========================================
echo Creazione Eseguibile MP3 Organizer
echo ========================================
echo.

REM Verifica Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRORE: Python non trovato!
    pause
    exit /b 1
)

REM Installa PyInstaller
echo Installazione PyInstaller...
pip install pyinstaller mutagen

REM Crea l'eseguibile
echo.
echo Creazione eseguibile...
pyinstaller --onefile --windowed --name "MP3_Organizer" --icon=NONE organizza_mp3_gui.py

echo.
echo ========================================
if exist "dist\MP3_Organizer.exe" (
    echo ✓ Eseguibile creato con successo!
    echo.
    echo Trovi il file in: dist\MP3_Organizer.exe
    echo.
    echo Puoi copiarlo ovunque e usarlo senza Python!
) else (
    echo ✗ Errore nella creazione dell'eseguibile
)
echo ========================================
echo.
pause
