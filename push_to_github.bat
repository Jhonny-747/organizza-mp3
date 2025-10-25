@echo off
title Push to GitHub
color 0A
echo ========================================
echo   Push Automatico su GitHub
echo ========================================
echo.

REM Verifica se git è installato
git --version >nul 2>&1
if errorlevel 1 (
    echo ERRORE: Git non trovato!
    echo Installa Git da https://git-scm.com/
    echo.
    pause
    exit /b 1
)

REM Mostra lo stato corrente
echo [1/4] Controllo modifiche...
echo.
git status
echo.

REM Chiedi conferma
set /p confirm="Vuoi procedere con il commit e push? (s/n): "
if /i not "%confirm%"=="s" (
    echo Operazione annullata.
    pause
    exit /b 0
)

echo.
echo [2/4] Aggiunta file modificati...
git add .

REM Chiedi il messaggio di commit
echo.
set /p commit_msg="Inserisci il messaggio di commit: "
if "%commit_msg%"=="" (
    set commit_msg=Update files
)

echo.
echo [3/4] Creazione commit...
git commit -m "%commit_msg%"

if errorlevel 1 (
    echo.
    echo Nessuna modifica da committare o errore nel commit.
    pause
    exit /b 1
)

echo.
echo [4/4] Push su GitHub...
git push

if errorlevel 1 (
    echo.
    echo ERRORE durante il push!
    echo Verifica la connessione e le credenziali.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   ✓ Push completato con successo!
echo ========================================
echo.
pause
