@echo off
:: ============================================================================
:: CyberSential22 - Quick Server Launcher
:: ============================================================================
:: Project: Password Strength Checker
:: Description: Skip dependency checks and initialization for a faster,
::              immediate server launch.
:: ============================================================================

setlocal
title Password Strength Checker (Quick Start)
color 0B
cls

echo ======================================================
echo    CyberSential22 - Quick Start Server
echo ======================================================
echo.

:: 1. Virtual Environment Activation
if exist ".venv\Scripts\activate" (
    echo [i] Activating .venv...
    call .venv\Scripts\activate
) else (
    color 0C
    echo [!] ERROR: Virtual environment (.venv) not found.
    echo [i] Please run 'run_server.bat' first to initialize.
    pause
    exit /b 1
)

:: 2. Flask Environment Setup
set FLASK_APP=app.py
set FLASK_ENV=development
set FLASK_DEBUG=1
set PYTHONDONTWRITEBYTECODE=1

echo.
echo [STARTED] Server is running at: http://127.0.0.1:5000
echo [INFO]    Press Ctrl+C to stop the process.
echo.

python app.py
pause
