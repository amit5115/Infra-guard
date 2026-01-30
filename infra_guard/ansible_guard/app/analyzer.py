import yaml
import os

DANGEROUS_MODULES = ["shell", "command", "raw"]

def analyze_playbook(playbook_path):
    risks = []

    with open(playbook_path) as f:
        plays = yaml.safe_load(f)

    for play in plays:
        for task in play.get("tasks", []):
            name = task.get("name", "unnamed task")

            if "shell" in task:
                risks.append({
                    "task": name,
                    "reason": "Uses shell module (command execution)",
                    "risk": "HIGH"
                })

            if task.get("become") is True:
                risks.append({
                    "task": name,
                    "reason": "Privilege escalation enabled",
                    "risk": "HIGH"
                })

            if task.get("ignore_errors") is True:
                risks.append({
                    "task": name,
                    "reason": "Errors are ignored",
                    "risk": "MEDIUM"
                })

    return risks
