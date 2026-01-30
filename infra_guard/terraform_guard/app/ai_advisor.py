# from openai import OpenAI

# client = OpenAI()

# def explain_risk(destructive_resources):
#     prompt = f"""
# You are a senior DevOps engineer.

# The following Terraform resources are going to be deleted or replaced:
# {destructive_resources}

# Explain in very simple words:
# 1. What will happen
# 2. Why this is risky
# 3. Should we apply or not
# """

#     try:
#         response = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[
#                 {"role": "user", "content": prompt}
#             ]
#         )
#         return response.choices[0].message.content

#     except Exception as e:
#         # FALLBACK (DEMO SAFE)
#         # return (
#         #     "⚠️ High Risk Change Detected\n\n"
#         #     "One or more resources will be deleted or replaced.\n"
#         #     "This may cause data loss or downtime.\n\n"
#         #     "Recommendation: DO NOT apply without approval."
#         # )
#         print("DEBUG AI ERROR:", e)
#         return "AI FAILED"


# from company_llm import call_company_llm
from .company_llm import call_company_llm
import json
import requests


def explain_all_changes(changes):
    prompt = f"""
You are a senior DevOps engineer.

Analyze the Terraform infrastructure changes below and respond in STRICT JSON ONLY.

Terraform changes:
{json.dumps(changes, indent=2)}

Return JSON exactly in this format:
{{
  "summary": "long summary",
  "changes": ["list of key changes"],
  "impact": "what will happen technically",
  "risk_level": "LOW | MEDIUM | HIGH",
  "recommendation": "what should be done"
}}

IMPORTANT:
- Do NOT add markdown
- Do NOT add explanations outside JSON
- Output must be valid JSON only
"""

    try:
        return call_company_llm([
            {"role": "user", "content": prompt}
        ])
    except Exception:
        return json.dumps({
            "summary": "Unable to analyze changes",
            "changes": [],
            "impact": "Unknown",
            "risk_level": "UNKNOWN",
            "recommendation": "Review Terraform plan manually"
        })
    
def explain_risk(destructive_resources):
    """
    Backward compatibility wrapper.
    Converts destructive-only input to generic change explanation.
    """
    changes = [
        {
            "address": r.get("address"),
            "actions": r.get("actions")
        }
        for r in destructive_resources
    ]

    return explain_all_changes(changes)

def explain_cost_impact(costs):
    prompt = f"""
You are an expert cloud cost analyst.

Analyze the following Terraform cost changes and return STRICT JSON in this format:

{{
  "summary": "give detailed summary of this change",
  "changes": [
    "long bullet 1",
    "long bullet 2"
  ],
  "impact": "operational and financial impact",
  "risk_level": "LOW | MEDIUM | HIGH",
  "recommendation": "clear actionable recommendation"
}}

Cost changes:
{costs}

Rules:
- Do NOT add markdown
- Do NOT add explanations outside JSON
- Be concise
"""

    messages = [
        {"role": "system", "content": "You are an expert cloud cost analyst."},
        {"role": "user", "content": prompt}
    ]

    response = call_company_llm(messages)
    return response   # ✅ STRING
