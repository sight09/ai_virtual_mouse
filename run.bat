@echo off
REM AI Virtual Mouse - Windows Launcher
REM This script sets up and runs the Virtual Mouse application

echo.
echo ================================
echo  AI Virtual Mouse - Launcher
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11+ from https://www.python.org/
    pause
    exit /b 1
)

REM Check if venv exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate venv
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if requirements are installed
pip show mediapipe >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo.
echo ================================
echo  Starting AI Virtual Mouse
echo ================================
echo.

REM Run the application
python main.py

REM Keep window open if there was an error
if errorlevel 1 (
    echo.
    echo ERROR: Application exited with error code %ERRORLEVEL%
    pause
)
