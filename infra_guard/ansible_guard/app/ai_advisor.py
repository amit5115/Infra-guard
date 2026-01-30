import json
from .company_llm import call_company_llm

def explain_ansible_risk(risks):
    prompt = f"""
You are a senior DevOps and SRE engineer.

Analyze the following Ansible risks and return STRICT JSON ONLY.

Return format:
{{
  "summary": "one line summary",
  "risk_level": "LOW | MEDIUM | HIGH",
  "impact": [
    "impact line 1",
    "impact line 2"
  ],
  "recommendation": "clear actionable recommendation"
}}

Ansible risks:
{risks}

Rules:
- Output ONLY valid JSON
- No markdown
- No extra text
"""

    messages = [
        {"role": "user", "content": prompt}
    ]

    response = call_company_llm(messages)

    data = json.loads(response)

    if isinstance(data, list) and len(data) > 0:
       data = data[0]

    return data

