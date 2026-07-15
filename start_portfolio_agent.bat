@echo off
REM Start Dynamic Portfolio Optimization Agent
REM This script activates the virtual environment and starts the Flask app

echo ======================================================================
echo Starting Portfolio Optimization Agent
echo ======================================================================
echo.

REM Navigate to portfolio-agent directory
cd /d "%~dp0"

REM Check if venv exists
if not exist "venv\Scripts\activate.bat" (
    echo Error: Virtual environment not found
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if required packages are installed
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
)

REM Set PYTHONPATH for proper imports
set PYTHONPATH=.

REM Start the agent
echo.
echo ======================================================================
echo Portfolio Agent starting on http://localhost:5000
echo ======================================================================
echo.
echo Access the dashboard at:
echo   Local:   http://localhost:5000
echo   Network: http://%COMPUTERNAME%:5000
echo.
echo Press Ctrl+C to stop the server
echo.

python web_ui/app.py

pause
