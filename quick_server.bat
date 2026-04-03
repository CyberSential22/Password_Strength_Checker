@echo off
:: ============================================================================
:: CyberSential22 - Quick Server Launcher
:: ============================================================================
setlocal
cd /d "%~dp0"
title CyberSential22 - Fast Start
cls

echo ======================================================
echo    CYBERSENTIAL22 - QUICK SERVER START
echo ======================================================
echo.

:: 1. Activate Environment
if not exist .venv\Scripts\activate.bat (
    echo [!] ERROR: Virtual environment not found.
    echo Please run 'run_server.bat' to initialise the project.
    pause
    exit /b 1
)

echo [1/3] Activating environment...
call .venv\Scripts\activate.bat

:: 2. Check Dependencies
echo [2/3] Verifying dependencies...
if exist requirements.txt (
    pip install -r requirements.txt --quiet --no-deps >nul 2>&1
    if %errorlevel% neq 0 (
        echo [!] Missing dependencies detected. Installing...
        pip install -r requirements.txt
    ) else (
        echo [OK] Dependencies are up to date.
    )
)

:: 3. Live Run
echo [3/3] Starting server...
echo.

python app.py
if %errorlevel% neq 0 (
    echo.
    echo [!] Server exited with code %errorlevel%.
    pause
)
