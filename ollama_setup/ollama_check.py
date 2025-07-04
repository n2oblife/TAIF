import requests

OLLAMA_URL = "http://127.0.0.1:11434"

try:
    # Check Ollama server status
    response = requests.get(f"{OLLAMA_URL}/api/tags")
    response.raise_for_status()
    models = response.json().get("models", [])
    print("Ollama is running!")
    print("Available models:")
    for model in models:
        print(f"- {model.get('name', 'unknown')}")
except Exception as e:
    print("Could not connect to Ollama at http://127.0.0.1:11434")
    print(f"Error: {e}") 