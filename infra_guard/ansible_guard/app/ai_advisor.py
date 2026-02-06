import json

import re

from .common_llm import call_llm


# ---------------------------------------------------

# SAFE JSON PARSER (MOST IMPORTANT FIX)

# ---------------------------------------------------

def safe_json_parse(text):

    """

    LLM responses are NOT reliable JSON.

    This function prevents crashes.

    """

    # 1️⃣ Try direct JSON

    try:

        return json.loads(text)

    except Exception:

        pass

    # 2️⃣ Try extracting JSON block

    match = re.search(r"\{[\s\S]*\}", text)

    if match:

        try:

            return json.loads(match.group())

        except Exception:

            pass

    # 3️⃣ Final fallback (NO CRASH)

    return {

        "summary": "Unable to safely parse AI response",

        "issues": [],

        "risk_level": "UNKNOWN",

        "recommendation": "Review Ansible tasks manually"

    }


# ---------------------------------------------------

# MAIN AI FUNCTION

# ---------------------------------------------------

def explain_ansible_risk(tasks):

    """

    tasks: parsed ansible tasks list

    MUST return DICT (safe)

    """

    prompt = f"""

You are a security-focused DevOps engineer.

STRICT RULES:

- Output ONLY valid JSON

- NO markdown

- NO explanation outside JSON

- NO tables

- NO bullets

Return EXACTLY in this format:

{{

  "summary": "short summary",

  "issues": [

    {{

      "task": "task name",

      "risk": "LOW | MEDIUM | HIGH",

      "reason": "why risky"

    }}

  ],

  "risk_level": "LOW | MEDIUM | HIGH",

  "recommendation": "what should be done"

}}

Ansible tasks:

{json.dumps(tasks, indent=2)}

"""

    messages = [

        {"role": "user", "content": prompt}

    ]

    try:

        response = call_llm(messages)   # 🔥 LLM CALL

        return safe_json_parse(response)

    except Exception as e:

        return {

            "summary": "AI execution failed",

            "issues": [],

            "risk_level": "UNKNOWN",

            "recommendation": "Review Ansible tasks manually"

        }
 