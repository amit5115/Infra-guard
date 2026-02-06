import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"


def call_ollama(messages):
    """
    MUST return STRING
    Terraform Guard parses JSON from string
    """

    # Terraform Guard hamesha last user message bhejta hai
    prompt = messages[-1]["content"]

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=60
        )
        response.raise_for_status()

        data = response.json()

        # 🔥 MOST IMPORTANT LINE
        return data.get("response", "").strip()

    except Exception as e:
        print("❌ Ollama error:", e)
        return json.dumps({
            "summary": "Unable to analyze changes",
            "changes": [],
            "impact": "Unknown",
            "risk_level": "UNKNOWN",
            "recommendation": "Review Terraform plan manually"
        })
