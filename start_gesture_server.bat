@echo off
setlocal enabledelayedexpansion

echo ========================================
echo Starting environment activation...
echo ========================================

REM Check if Conda is installed
where conda >nul 2>&1
if %ERRORLEVEL% equ 0 (
    REM Conda is installed - get active environment
    for /f "tokens=*" %%i in ('conda info --envs ^| findstr "*"') do (
        set "CONDA_ENV=%%i"
        for /f "tokens=1" %%a in ("!CONDA_ENV!") do (
            set "ENV_NAME=%%a"
        )
    )
    echo [INFO] Found Conda environment: !ENV_NAME!
    call conda activate !ENV_NAME!
) else (
    REM Check for venv/virtualenv
    if exist "venv\Scripts\activate.bat" (
        echo [INFO] Found venv environment
        call venv\Scripts\activate.bat
    ) else if exist ".venv\Scripts\activate.bat" (
        echo [INFO] Found .venv environment
        call .venv\Scripts\activate.bat
    ) else (
        echo [ERROR] No virtual environment found! Please create one first.
        echo.
        echo You can create it using:
        echo - For venv: python -m venv venv
        echo - For Conda: conda create --name your_env_name
        echo.
        echo Press any key to exit...
        pause >nul
        exit /b 1
    )
)

echo.
echo ========================================
echo Running Python script...
echo ========================================

REM Run the Python script
python ZEGGS/server.py %*

set SCRIPT_EXIT_CODE=%ERRORLEVEL%

echo.
echo ========================================
echo Execution Status
echo ========================================

if %SCRIPT_EXIT_CODE% equ 0 (
    echo [SUCCESS] Script executed successfully
) else (
    echo [ERROR] Script failed with error code %SCRIPT_EXIT_CODE%
)

echo.
echo ========================================
echo Cleaning up...
echo ========================================

call deactivate 2>nul
if %ERRORLEVEL% equ 0 (
    echo [INFO] Environment deactivated successfully
)

echo.
echo ========================================
echo Press any key to exit...
pause >nul
exit /b %SCRIPT_EXIT_CODE%