@echo off
REM Find the PID using port 11434 and kill it
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :11434') do set PID=%%a
if not defined PID (
    echo No process found using port 11434.
    exit /b 1
)
echo Stopping process with PID %PID% using port 11434...
taskkill /PID %PID% /F 