# ansible_guard/app/ollama_llm.py

import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

def call_ollama(messages):
    """
    messages = [
        {"role": "system", "content": "..."},
        {"role": "user", "content": "..."}
    ]
    Returns STRING only
    """

    prompt = messages[-1]["content"]

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=60)
    response.raise_for_status()

    data = response.json()
    return data.get("response", "")
