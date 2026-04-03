@echo off
:: ============================================================================
:: CyberSential22 - Development Server Launcher
:: ============================================================================
:: Project: Password Strength Checker
:: Description: Activates virtual environment, installs dependencies,
::              sets up Flask environment, and launches the server.
:: ============================================================================

setlocal
title CyberSential22 - Password Strength Checker Server
color 0B
cls

echo ======================================================
echo    CyberSential22 - Password Strength Checker
echo    Status: Preparing Server Environment...
echo ======================================================
echo.

:: 1. Virtual Environment Check/Creation
if not exist ".venv" (
    echo [i] Virtual environment (.venv) not found.
    echo [i] Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        color 0C
        echo [!] ERROR: Failed to create virtual environment. 
        echo [i] Ensure Python 3.10+ is installed and accessible via 'python' command.
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created successfully.
)

:: 2. Activation
echo [i] Activating virtual environment...
call .venv\Scripts\activate
if errorlevel 1 (
    color 0C
    echo [!] ERROR: Failed to activate .venv.
    pause
    exit /b 1
)

:: 3. Dependencies Manager
echo [i] Checking dependencies...
if exist "requirements.txt" (
    echo [i] Synchronizing pip packages...
    pip install -q --upgrade pip
    pip install -q -r requirements.txt
) else (
    echo [!] requirements.txt not found! Installing default Core packages...
    pip install -q flask
    echo flask > requirements.txt
    echo [OK] requirements.txt generated.
)

:: 4. Flask Configuration
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
