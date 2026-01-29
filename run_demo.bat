@echo off
echo ============================================================
echo   REAL-TIME FRAUD DETECTION SYSTEM
echo ============================================================
echo.

echo Checking for Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8+ from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo Python found!
echo.
echo Running Fraud Detection Demo...
echo.
python demo.py

echo.
pause
