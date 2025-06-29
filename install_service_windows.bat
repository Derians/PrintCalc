@echo off
setlocal EnableDelayedExpansion
cd /d "%~dp0"
echo Installing PrintCalcService Windows service

:: Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Please run this script as Administrator
    pause
    exit /b 1
)

:: Check for Python 3
python --version 2>nul | findstr /B /C:"Python 3" >nul
if %errorLevel% neq 0 (
    echo Python 3 not found. Please install Python 3.7 or higher.
    pause
    exit /b 1
)

:: Check Python version
python -c "import sys; exit(1 if sys.version_info < (3,7) else 0)" >nul 2>&1
if %errorLevel% neq 0 (
    echo Python version is not supported. Please install Python 3.7 or higher.
    pause
    exit /b 1
)

:: Check for pip
python -m pip --version >nul 2>&1
if %errorLevel% neq 0 (
    echo pip not found. Please install pip for Python 3.
    pause
    exit /b 1
)

:: Create virtual environment if it does not exist
if not exist venv\Scripts\python.exe (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Installing dependencies from requirements.txt...
    pip install -r requirements.txt
)

:: Install/update required packages if venv exists
if exist venv\Scripts\python.exe (
    call venv\Scripts\activate.bat
    echo Updating dependencies from requirements.txt...
    pip install -r requirements.txt
)

:: Get full paths
set "SCRIPT_DIR=%~dp0"
set "RUNNER_PATH=%SCRIPT_DIR%service_runner.bat"

:: Create service runner if it doesn't exist
echo @echo off > "%RUNNER_PATH%"
echo cd /d "%%~dp0" >> "%RUNNER_PATH%"
echo call "%%~dp0venv\Scripts\activate.bat" >> "%RUNNER_PATH%"
echo "%%~dp0venv\Scripts\python.exe" "%%~dp0wsgi.py" >> "%RUNNER_PATH%"

:: Remove existing service if it exists
echo Checking for existing service...
sc query PrintCalcService >nul 2>&1
if %errorLevel% equ 0 (
    echo Stopping service...
    sc stop PrintCalcService >nul 2>&1
    timeout /t 5 /nobreak >nul
    
    echo Removing service...
    sc delete PrintCalcService >nul 2>&1
    
    echo Waiting for service removal to complete...
    timeout /t 10 /nobreak >nul
)

:: Verify service is completely removed
:check_service
sc query PrintCalcService >nul 2>&1
if %errorLevel% neq 1060 (
    echo Waiting for service removal...
    timeout /t 5 /nobreak >nul
    goto check_service
)

:: Create and start the service
echo Installing service...
sc create PrintCalcService binPath= "cmd.exe /c \"%RUNNER_PATH%\"" start= auto DisplayName= "PrintCalc Service"
if %errorLevel% neq 0 goto error

sc description PrintCalcService "Web service for 3D printing cost calculation"
sc config PrintCalcService type= own obj= "NT AUTHORITY\LocalService"
sc config PrintCalcService depend= Tcpip/Afd

echo.
echo Waiting before starting service...
timeout /t 5 /nobreak >nul

echo Starting service...
sc start PrintCalcService
if %errorLevel% neq 0 goto error

echo.
echo Installation complete! Service should be running.
echo To verify service status, run: sc query PrintCalcService
goto end

:error
echo.
echo Error occurred during installation!
echo Please try running service_runner.bat directly to check for errors.
echo Also check Event Viewer for more details.

:end
endlocal
pause