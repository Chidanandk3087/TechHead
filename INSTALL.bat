@echo off
echo ================================================
echo   Portfolio Website - Quick Start
echo ================================================
echo.

echo [1/3] Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)
echo ✓ Python found!
echo.

echo [2/3] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed!
echo.

echo [3/3] Setting up database...
python setup_complete.py
if errorlevel 1 (
    echo ERROR: Failed to setup database
    pause
    exit /b 1
)
echo.

echo ================================================
echo   Setup Complete! 🎉
echo ================================================
echo.
echo Your portfolio is ready to run!
echo.
echo To start the application:
echo   1. Run: python app.py
echo   2. Open browser: http://localhost:5000
echo   3. Admin login: chidanandkhot03@gmail.com / ChidanandK@3087
echo.
echo IMPORTANT: Configure email settings in app.py
echo See EMAIL_SETUP.md for instructions
echo.
echo ================================================
pause
