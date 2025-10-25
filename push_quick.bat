@echo off
REM Push rapido senza conferme - usa con cautela!
title Quick Push to GitHub
echo Push rapido in corso...
echo.

git add .
git commit -m "Quick update: %date% %time%"
git push

if errorlevel 1 (
    echo.
    echo Errore durante il push!
    pause
    exit /b 1
)

echo.
echo ✓ Push completato!
timeout /t 2 >nul
