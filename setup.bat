@echo off
echo ========================================
echo Real-Time Fraud Detection System Setup
echo ========================================
echo.

echo [1/5] Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.8+
    exit /b 1
)
echo.

echo [2/5] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    exit /b 1
)
echo.

echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
echo.

echo [4/5] Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    exit /b 1
)
echo.

echo [5/5] Creating environment file...
if not exist .env (
    copy .env.example .env
    echo Created .env file from .env.example
)
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Start Redis: redis-server
echo 2. Train model: python train_model.py
echo 3. Run example: python example_usage.py
echo 4. Start API: python src/api.py
echo.
echo For more information, see README.md
echo.

pause
