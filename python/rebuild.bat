@echo off
rem MonitorCheck rebuild script - PyInstaller build
set APPVER=3.1
cd /d %~dp0

rem Prefer pyinstaller from PATH, fall back to the local venv used during development
set "PYI=pyinstaller"
where pyinstaller >nul 2>nul
if errorlevel 1 (
  if exist "%USERPROFILE%\.workbuddy\binaries\python\envs\py312\Scripts\pyinstaller.exe" (
    set "PYI=%USERPROFILE%\.workbuddy\binaries\python\envs\py312\Scripts\pyinstaller.exe"
  ) else (
    echo [ERROR] pyinstaller not found. Run: pip install pyinstaller
    exit /b 1
  )
)

rem --exclude-module PIL: openpyxl conditionally imports Pillow, without it the exe grows ~7MB
"%PYI%" --onefile --noconsole --clean --icon icon.ico --version-file version_info.txt --exclude-module PIL --exclude-module numpy --exclude-module pandas --name MonitorCheckPy monitor_check.py
if errorlevel 1 (
  echo BUILD FAILED
  exit /b 1
)
copy /y dist\MonitorCheckPy.exe ..\MonitorCheck_v%APPVER%.exe
echo DONE: ..\MonitorCheck_v%APPVER%.exe updated
