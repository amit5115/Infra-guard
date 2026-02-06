from .company_llm import call_company_llm
from .ollama_llm import call_ollama

LLM_PROVIDER = "ollama"  # or "company"

def call_llm(messages):
    if LLM_PROVIDER == "ollama":
        return call_ollama(messages)
    else:
        return call_company_llm(messages)
