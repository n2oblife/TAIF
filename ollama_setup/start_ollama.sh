#!/bin/bash

if ! command -v ollama &> /dev/null
then
    echo "Ollama is not installed. Please install Ollama from https://ollama.com/download before running this script."
    exit 1
fi

echo "Starting Ollama server..."
ollama serve 