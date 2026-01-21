@echo off
REM AEIS Backend Startup Script for Windows

echo ========================================
echo  AEIS - Aadhaar Enrolment Intelligence
echo  Backend Server Startup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo [1/3] Checking Python version...
python --version
echo.

REM Check if requirements are installed
echo [2/3] Checking dependencies...
python -c "import flask, pandas, numpy, scipy, matplotlib, seaborn" 2>nul
if %errorlevel% neq 0 (
    echo WARNING: Some dependencies are missing
    echo Installing requirements...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
) else (
    echo All dependencies are installed
)
echo.

REM Start the backend server
echo [3/3] Starting AEIS Backend Server...
echo.
echo Backend will start on: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
echo ----------------------------------------
echo.

cd backend
python app.py

pause
