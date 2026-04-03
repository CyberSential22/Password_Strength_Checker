@echo off
:: ============================================================================
:: CyberSential22 - Project Initialiser (Repair Mode)
:: ============================================================================
setlocal
cd /d "%~dp0"
title CyberSential22 - Initialising...
cls

echo ======================================================
echo    CYBERSENTIAL22 - PROJECT INITIALISER
echo ======================================================
echo.

:: 1. Verify Python
echo [1/4] Checking Python installation...
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] FATAL ERROR: Python command not found.
    echo Please install Python 3.10+ and add it to your PATH.
    pause
    exit /b 1
)

:: 2. Manage Virtual Environment
if exist .venv if not exist .venv\Scripts\activate.bat (
    echo [i] Broken environment detected. Wiping .venv...
    rd /s /q .venv
)

if not exist .venv (
    echo [2/4] Creating fresh virtual environment...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo [!] FATAL ERROR: Failed to create virtual environment.
        pause
        exit /b 1
    )
) else (
    echo [2/4] Virtual environment already exists.
)

:: 3. Activate and Install
echo [3/4] Activating environment...
call .venv\Scripts\activate.bat

echo [4/4] Synchronizing dependencies...
python -m pip install -q --upgrade pip
if exist requirements.txt (
    pip install -r requirements.txt
) else (
    echo [!] Warning: requirements.txt not found.
)

echo.
echo [COMPLETE] Environment is ready.
echo [i] Starting development server...
echo.

python app.py
if %errorlevel% neq 0 (
    echo.
    echo [!] Server exited with code %errorlevel%.
    pause
)
