# ansible_guard/app/common_llm.py

from .ollama_llm import call_ollama
# future me company_llm add kar sakte ho

def call_llm(messages):
    """
    Single entry point for Ansible Guard LLM calls
    MUST return raw STRING
    """
    return call_ollama(messages)
