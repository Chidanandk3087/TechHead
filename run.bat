@echo off
echo ================================================
echo   Chidanand Khot Portfolio Application
echo ================================================
echo.
echo Starting Flask development server...
echo.
echo Access the application at:
echo   → http://localhost:5000
echo   → http://127.0.0.1:5000
echo.
echo Admin Panel:
echo   → http://localhost:5000/login
echo   → Default: chidanandkhot03@gmail.com / ChidanandK@3087
echo.
echo Press Ctrl+C to stop the server
echo ================================================
echo.

set FLASK_APP=app.py
set FLASK_ENV=development
python app.py