import subprocess
import os

def run_ansible(playbook, inventory=None, check=False):
    """
    Runs ansible-playbook with optional --check (dry-run)
    """

    cmd = ["ansible-playbook", playbook]

    if inventory:
        cmd.extend(["-i", inventory])

    if check:
        cmd.append("--check")

    subprocess.run(
        cmd,
        check=True
    )
