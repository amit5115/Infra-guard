import requests

PROXY_ENDPOINT = "https://ai-framework1:8085"
API_KEY = "f7607702011b43e19417a91c1dd07489"
LLM_MODEL = "gpt-4.1"

HEADERS = {
    "Content-Type": "application/json",
    "API-Key": API_KEY,
    "X-Effective-Caller": "amitk30@amdocs.com"
}

def call_company_llm(messages):
    payload = {
        "llm_model": LLM_MODEL,
        "messages": messages
    }

    response = requests.post(
        f"{PROXY_ENDPOINT}/api/v1/call_llm",
        headers=HEADERS,
        json=payload,
        verify=False,
        timeout=30
    )

    if response.status_code != 200:
        raise Exception(f"LLM HTTP error: {response.text}")

    body = response.json()
    return body["message"]   # 👈 STRING
