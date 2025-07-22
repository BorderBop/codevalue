@echo off
setlocal enabledelayedexpansion

REM Kill any process using port 8000
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do (
    echo Killing process on port 8000 (PID: %%a)
    taskkill /PID %%a /F
)

REM Activate virtual environment
call automation\venv\Scripts\activate.bat

REM Start FastAPI server in background
start "uvicorn" cmd /c "uvicorn automation.server.backend:app --port 8000 --reload > nul 2>&1"
REM Wait for server to start
ping 127.0.0.1 -n 4 > nul

REM Run all tests
pytest automation\tests
set TEST_RESULT=%ERRORLEVEL%

REM Kill uvicorn server (find by port again)
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do (
    echo Stopping server (PID: %%a)
    taskkill /PID %%a /F
)

exit /b %TEST_RESULT% 