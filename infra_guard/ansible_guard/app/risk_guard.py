def is_apply_allowed(ai_analysis):
    """
    Decide whether Ansible apply should proceed based on risk level
    """
    risk = ai_analysis.get("risk_level", "LOW").upper()

    if risk == "HIGH":
        return False, "HIGH risk detected. Apply is BLOCKED."

    if risk == "MEDIUM":
        return True, "MEDIUM risk detected. Manual confirmation required."

    return True, "LOW risk. Safe to apply."
