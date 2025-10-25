@echo off
title Organizzatore MP3
echo Avvio Organizzatore MP3...
echo.

REM Verifica se Python è installato
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRORE: Python non trovato!
    echo Installa Python da https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM Verifica e installa dipendenze
echo Controllo dipendenze...
pip show mutagen >nul 2>&1
if errorlevel 1 (
    echo Installazione mutagen...
    pip install mutagen
)

REM Avvia l'applicazione
echo.
echo Avvio interfaccia grafica...
python organizza_mp3_gui.py

if errorlevel 1 (
    echo.
    echo Si è verificato un errore!
    pause
)
