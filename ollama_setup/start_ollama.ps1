# PowerShell script to start Ollama server
# Usage: Run this script from the project root

Write-Host "Starting Ollama server..."

# Check if Ollama is installed
if (-not (Get-Command "ollama" -ErrorAction SilentlyContinue)) {
    Write-Host "Ollama is not installed. Please install Ollama from https://ollama.com/download before running this script."
    exit 1
}

# Start Ollama server
ollama serve 