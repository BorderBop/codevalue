@echo off
setlocal enabledelayedexpansion

REM Check if Python is installed
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Python is not found. Please install Python and add it to PATH.
    pause
    exit /b 1
)

REM Check if pip is installed
pip --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo pip is not found. Installing pip...
    python -m ensurepip
)

REM Check if pytest is installed
python -m pytest --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo pytest is not found. Installing pytest...
    pip install pytest
)

REM Install all required Python packages
pip install -r automation\requirements.txt

REM Kill any process using port 8000
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do (
    echo Killing process on port 8000 (PID: %%a)
    taskkill /PID %%a /F
)

REM Activate virtual environment
call automation\venv\Scripts\activate.bat

REM Start FastAPI server in background using python -m uvicorn
start "uvicorn" cmd /c "python -m uvicorn automation.server.backend:app --port 8000 --reload > nul 2>&1"
REM Wait for server to start
ping 127.0.0.1 -n 4 > nul

REM Run all tests
python -m pytest automation\tests
set TEST_RESULT=%ERRORLEVEL%

REM Kill uvicorn server (find by port again)
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do (
    echo Stopping server (PID: %%a)
    taskkill /PID %%a /F
)

exit /b %TEST_RESULT% 
