@echo off
:: ============================================================================
:: CyberSential22 - Quick Server Launcher (DEBUG READY)
:: ============================================================================

setlocal
title Password Strength Checker (Quick Start)
color 0B
cls

echo ======================================================
echo    CyberSential22 - Quick Start Server
echo ======================================================
echo.

:: 1. Diagnostic: Check if python is in PATH
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo [!] ERROR: 'python' command not found.
    pause
    exit /b 1
)

:: 2. Virtual Environment Activation
if exist ".venv\Scripts\activate.bat" (
    echo [i] Activating .venv...
    call .venv\Scripts\activate
) else (
    color 0C
    echo [!] ERROR: Virtual environment (.venv) not found.
    echo [i] Please run 'run_server.bat' first to initialize.
    echo.
    pause
    exit /b 1
)

:: 3. Flask Environment Setup
set FLASK_APP=app.py
set FLASK_ENV=development
set FLASK_DEBUG=1
set PYTHONDONTWRITEBYTECODE=1

echo.
echo [STARTED] Server is running at: http://127.0.0.1:5000
echo [INFO]    Close this window to stop the server.
echo.

:: Launch the app
python app.py

:: If it crashes, keep window open
if errorlevel 1 (
    echo.
    echo [!] Application crashed with exit code %errorlevel%.
    pause
)
