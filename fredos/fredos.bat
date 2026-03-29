@echo off
setlocal

set PYTHON_EXE=%~dp0.python\python.exe

if not exist "%PYTHON_EXE%" (
    echo Portable Python not found at %PYTHON_EXE%
    echo Please run scripts\setup_portable_python.ps1 first.
    exit /b 1
)

if "%1"=="run" (
    echo Starting FredOS...
    "%PYTHON_EXE%" -m uvicorn app.main:app
    exit /b 0
)

if "%1"=="dev" (
    echo Starting FredOS in reload mode...
    "%PYTHON_EXE%" -m uvicorn app.main:app --reload
    exit /b 0
)

if "%1"=="test" (
    echo Running tests...
    "%PYTHON_EXE%" -m pytest tests/ -v
    exit /b 0
)

if "%1"=="python" (
    shift
    "%PYTHON_EXE%" %*
    exit /b %ERRORLEVEL%
)

echo Usage:
echo   fredos.bat run      - Start the FastAPI server
echo   fredos.bat dev      - Start the FastAPI server with reload
echo   fredos.bat test     - Run the pytest suite
echo   fredos.bat python   - Run the portable python directly (e.g. fredos.bat python scripts/seed.py)
exit /b 0
