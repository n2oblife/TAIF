@echo off

where ollama >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Ollama is not installed. Please install Ollama from https://ollama.com/download before running this script.
    exit /b 1
)

echo Starting Ollama server...
ollama serve 