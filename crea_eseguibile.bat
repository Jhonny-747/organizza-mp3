@echo off
title Creazione Eseguibile MP3 Organizer
color 0B
echo ========================================
echo Creazione Eseguibile MP3 Organizer
echo ========================================
echo.

REM Verifica Python
echo [1/5] Verifica Python...
python --version
if errorlevel 1 (
    echo.
    echo ERRORE: Python non trovato!
    echo Installa Python da https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)
echo ✓ Python trovato
echo.

REM Verifica file sorgente
echo [2/5] Verifica file sorgente...
if not exist "organizza_mp3_gui.py" (
    echo.
    echo ERRORE: File organizza_mp3_gui.py non trovato!
    echo Assicurati di essere nella cartella corretta.
    echo.
    pause
    exit /b 1
)
echo ✓ File sorgente trovato
echo.

REM Installa dipendenze
echo [3/5] Installazione dipendenze...
pip install --upgrade pip
pip install pyinstaller mutagen
if errorlevel 1 (
    echo.
    echo ERRORE: Impossibile installare le dipendenze!
    pause
    exit /b 1
)
echo ✓ Dipendenze installate
echo.

REM Pulisci build precedenti
echo [4/5] Pulizia build precedenti...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "MP3_Organizer.spec" del /q MP3_Organizer.spec
echo ✓ Pulizia completata
echo.

REM Crea l'eseguibile
echo [5/5] Creazione eseguibile...
echo Questo potrebbe richiedere alcuni minuti...
echo.
python -m PyInstaller --onefile --windowed --name "MP3_Organizer" --clean --noconfirm organizza_mp3_gui.py

echo.
echo ========================================
if exist "dist\MP3_Organizer.exe" (
    echo.
    echo    ✓✓✓ SUCCESSO! ✓✓✓
    echo.
    echo Eseguibile creato in: dist\MP3_Organizer.exe
    echo.
    echo Puoi copiare il file .exe ovunque e usarlo
    echo senza bisogno di Python installato!
    echo.
    
    REM Mostra dimensione file
    for %%A in ("dist\MP3_Organizer.exe") do (
        set size=%%~zA
        set /a sizeMB=%%~zA/1024/1024
    )
    echo Dimensione: !sizeMB! MB circa
    echo.
) else (
    echo.
    echo    ✗✗✗ ERRORE ✗✗✗
    echo.
    echo Impossibile creare l'eseguibile.
    echo.
    echo Possibili cause:
    echo - Antivirus che blocca PyInstaller
    echo - Permessi insufficienti
    echo - Dipendenze mancanti
    echo.
    echo Prova a:
    echo 1. Disattivare temporaneamente l'antivirus
    echo 2. Eseguire come amministratore
    echo 3. Controllare i messaggi di errore sopra
    echo.
)
echo ========================================
echo.
pause
