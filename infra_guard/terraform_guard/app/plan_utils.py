import json
import os
import hashlib

# -------------------------
# Absolute paths (safe)
# -------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PLAN_PATH = os.path.abspath(os.path.join(BASE_DIR, "../plans/plan.json"))
TF_DIR = os.path.abspath(os.path.join(BASE_DIR, "../terraform"))


# -------------------------
# Plan helpers
# -------------------------
def plan_exists():
    return os.path.exists(PLAN_PATH)


def load_plan():
    if not plan_exists():
        raise FileNotFoundError("Terraform plan not found")

    with open(PLAN_PATH) as f:
        return json.load(f)


def plan_counts(plan):
    add = change = destroy = 0

    for r in plan.get("resource_changes", []):
        actions = r["change"]["actions"]

        if "create" in actions:
            add += 1

        if actions == ["update"]:
            change += 1

        if "delete" in actions:
            destroy += 1

    return add, change, destroy


# -------------------------
# HASH-BASED TF CHANGE DETECTION (FINAL)
# -------------------------
def calculate_tf_hash():
    """
    Calculates a SHA256 hash of all .tf files
    """
    hasher = hashlib.sha256()

    for root, _, files in os.walk(TF_DIR):
        for f in sorted(files):
            if f.endswith(".tf"):
                tf_path = os.path.join(root, f)
                with open(tf_path, "rb") as tf:
                    hasher.update(tf.read())

    return hasher.hexdigest()


def tf_files_changed():
    """
    Returns True if Terraform files changed since last plan
    """
    hash_file = PLAN_PATH + ".hash"
    current_hash = calculate_tf_hash()

    if not os.path.exists(hash_file):
        return True

    with open(hash_file) as f:
        old_hash = f.read()

    return current_hash != old_hash


def save_tf_hash():
    """
    Saves current TF hash AFTER successful terraform plan
    """
    hash_file = PLAN_PATH + ".hash"
    with open(hash_file, "w") as f:
        f.write(calculate_tf_hash())
