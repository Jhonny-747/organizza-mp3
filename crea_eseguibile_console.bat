@echo off
REM Versione alternativa che crea exe con console (per debug)
title Creazione Eseguibile MP3 Organizer (con console)
echo ========================================
echo Creazione Eseguibile con Console
echo (utile per vedere eventuali errori)
echo ========================================
echo.

REM Verifica Python
python --version
if errorlevel 1 (
    echo ERRORE: Python non trovato!
    pause
    exit /b 1
)

REM Installa dipendenze
echo.
echo Installazione dipendenze...
pip install pyinstaller mutagen

REM Pulisci
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "MP3_Organizer_Console.spec" del /q MP3_Organizer_Console.spec

REM Crea exe CON console (senza --windowed)
echo.
echo Creazione eseguibile con console...
python -m PyInstaller --onefile --name "MP3_Organizer_Console" --clean --noconfirm organizza_mp3_gui.py

echo.
if exist "dist\MP3_Organizer_Console.exe" (
    echo ✓ Eseguibile creato: dist\MP3_Organizer_Console.exe
    echo.
    echo Questo exe mostra la console per il debug.
) else (
    echo ✗ Errore nella creazione
)
echo.
pause
