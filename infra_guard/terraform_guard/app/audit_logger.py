import os
from datetime import datetime
import getpass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.abspath(os.path.join(BASE_DIR, "../audit_logs"))
LOG_FILE = os.path.join(LOG_DIR, "audit.log")

os.makedirs(LOG_DIR, exist_ok=True)


def log_event(event, details=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # current OS user
    user = getpass.getuser()

    line = f"[{timestamp}] {user} {event}"

    if details:
        line += f" | {details}"

    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")
