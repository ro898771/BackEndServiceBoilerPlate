@echo off
setlocal

REM ─── Get the directory of this batch file ────────────────────────────────────
set "BASE_DIR=%~dp0"

REM ─── Define environment paths ────────────────────────────────────────────────
set "ENV_DIR=%BASE_DIR%.venv"
set "ENV_PYTHON=%ENV_DIR%\Scripts\python.exe"

REM ─── Check if virtual environment exists ─────────────────────────────────────
if not exist "%ENV_PYTHON%" (
    echo Virtual environment not found or Python executable missing.
    pause
    exit /b 1
)

REM ─── Start Django on all interfaces (intranet / LAN access) ──────────────────
echo Starting Django server on 0.0.0.0:8000 ...
echo Anyone on the same network can connect via http://YOUR_IP:8000
echo Press Ctrl+C to stop the server.
echo.

"%ENV_PYTHON%" "%BASE_DIR%manage.py" runserver 0.0.0.0:8000

pause
