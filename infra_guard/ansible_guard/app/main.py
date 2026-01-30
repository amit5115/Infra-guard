from .analyzer import analyze_playbook
from .ai_advisor import explain_ansible_risk
from .runner import run_ansible
from .risk_guard import is_apply_allowed
import sys
import os

from .ui import (
    header,
    success,
    warning,
    error,
    show_risks,
    show_ai_analysis,
)


def main():
    repo = input("Enter Ansible repo path: ").strip()
    # playbook = f"{repo}/playbooks/site.yml"
    # inventory = f"{repo}/inventories/prod.ini"
    playbook = os.path.join(repo, "playbooks", "site.yml")
    inventory = os.path.join(repo, "inventories", "prod.ini")

    while True:
        print("\n========= Ansible Guard =========")
        print("1. AI Analyze Playbook")
        print("2. Apply Ansible (safe)")
        print("3. Exit")

        choice = input("Select option: ").strip()

        # ===============================
        # 1️⃣ AI ANALYSIS
        # ===============================
        if choice == "1":
            header("Ansible AI Analysis")
            risks = analyze_playbook(playbook)

            if not risks:
                success("No risky tasks detected")
            else:
                warning("Risky tasks detected")
                show_risks(risks)

                ai = explain_ansible_risk(risks)
                show_ai_analysis(ai)

        # ===============================
        # 2️⃣ SAFE APPLY
        # ===============================
        elif choice == "2":
            header("Ansible Apply")

            # Always analyze before apply
            risks = analyze_playbook(playbook)

            if risks:
                ai = explain_ansible_risk(risks)
                allowed, message = is_apply_allowed(ai)

                if not allowed:
                    error(message)
                    continue

                warning(message)
                confirm = input("Proceed anyway? (yes/no): ").strip().lower()
                if confirm != "yes":
                    warning("Apply aborted by user.")
                    continue

            success("Running dry-run...")
            run_ansible(playbook, inventory, check=True)

            confirm = input("Proceed with real apply? (yes/no): ").strip().lower()
            if confirm == "yes":
                run_ansible(playbook, inventory, check=False)
                success("Ansible apply completed")

        # ===============================
        # 3️⃣ EXIT
        # ===============================
        elif choice == "3":
          success("Exiting Ansible Guard 👋")
          sys.exit(0)

        else:
            warning("Invalid option selected")


if __name__ == "__main__":
    main()
