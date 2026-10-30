@echo off
rem MonitorCheck rebuild script - PyInstaller build
set APPVER=3.1
cd /d %~dp0
rem --exclude-module PIL: openpyxl 会条件导入 PIL, 不排除会多打进约 7MB
"C:\Users\yuguo\.workbuddy\binaries\python\envs\py312\Scripts\pyinstaller.exe" --onefile --noconsole --clean --icon icon.ico --version-file version_info.txt --exclude-module PIL --exclude-module numpy --exclude-module pandas --name MonitorCheckPy monitor_check.py
if errorlevel 1 (
  echo BUILD FAILED
  exit /b 1
)
copy /y dist\MonitorCheckPy.exe ..\MonitorCheck_v%APPVER%.exe
echo DONE: ..\MonitorCheck_v%APPVER%.exe updated
