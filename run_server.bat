@echo off
:: ============================================================================
:: CyberSential22 - Development Server Launcher (DEBUG READY)
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

:: 1. Diagnostic: Check if python is in PATH
echo [DEBUG] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo [!] ERROR: 'python' command not found in your PATH.
    echo [i] Please install Python 3.10+ and check "Add Python to PATH" during installation.
    pause
    exit /b 1
)
for /f "delims=" %%i in ('python --version') do set PY_VER=%%i
echo [OK] Using: %PY_VER%

:: 2. Virtual Environment Check/Creation
if not exist ".venv" (
    echo [i] Virtual environment (.venv) not found.
    echo [i] Creating virtual environment (this may take a minute)...
    python -m venv .venv
    if errorlevel 1 (
        color 0C
        echo [!] ERROR: Failed to create virtual environment. 
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created successfully.
)

:: 3. Activation
echo [i] Activating virtual environment...
if not exist ".venv\Scripts\activate.bat" (
    color 0C
    echo [!] ERROR: .venv/Scripts/activate.bat is missing.
    echo [i] Try deleting the .venv folder and running this script again.
    pause
    exit /b 1
)
call .venv\Scripts\activate
if errorlevel 1 (
    color 0C
    echo [!] ERROR: Failed to activate .venv.
    pause
    exit /b 1
)
echo [OK] Environment activated.

:: 4. Dependencies Manager
echo [i] Checking dependencies...
if exist "requirements.txt" (
    echo [i] Synchronizing pip packages (this may take a moment)...
    python -m pip install -q --upgrade pip
    pip install -q -r requirements.txt
) else (
    echo [!] requirements.txt not found! Installing Flask...
    pip install -q flask
    echo flask > requirements.txt
)
echo [OK] Dependencies ready.

:: 5. Flask Configuration
set FLASK_APP=app.py
set FLASK_ENV=development
set FLASK_DEBUG=1
set PYTHONDONTWRITEBYTECODE=1

echo.
echo ======================================================
echo    [STARTED] Server is running at: http://127.0.0.1:5000
echo    [INFO]    Close this window to stop the server.
echo ======================================================
echo.

:: Launch the app
python app.py

:: If it crashes, keep window open
if errorlevel 1 (
    echo.
    echo [!] Application crashed with exit code %errorlevel%.
    pause
)
