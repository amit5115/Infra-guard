# import json

# PLAN_PATH = "../plans/plan.json"


# def get_destructive_resources():
#     with open(PLAN_PATH) as f:
#         plan = json.load(f)

#     destructive = []

#     for resource in plan.get("resource_changes", []):
#         actions = resource.get("change", {}).get("actions", [])

#         if "delete" in actions or "replace" in actions:
#             destructive.append({
#                 "address": resource.get("address"),
#                 "actions": actions
#             })

#     return destructive


# def get_all_resource_changes():
#     with open(PLAN_PATH) as f:
#         plan = json.load(f)

#     changes = []

#     for resource in plan.get("resource_changes", []):
#         actions = resource.get("change", {}).get("actions", [])

#         # Ignore no-op
#         if actions == ["no-op"]:
#             continue

#         changes.append({
#             "address": resource.get("address"),
#             "actions": actions
#         })

#     return changes


import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLAN_PATH = os.path.abspath(os.path.join(BASE_DIR, "../plans/plan.json"))


def get_all_resource_changes():
    if not os.path.exists(PLAN_PATH):
        raise FileNotFoundError("Terraform plan.json not found. Run plan first.")

    with open(PLAN_PATH) as f:
        plan = json.load(f)

    changes = []

    for r in plan.get("resource_changes", []):
        changes.append({
            "address": r.get("address"),
            "type": r.get("type"),
            "actions": r.get("change", {}).get("actions", []),
        })

    return changes


def get_destructive_resources():
    destructive = []

    if not os.path.exists(PLAN_PATH):
        return destructive

    with open(PLAN_PATH) as f:
        plan = json.load(f)

    for r in plan.get("resource_changes", []):
        actions = r.get("change", {}).get("actions", [])
        if "delete" in actions or actions == ["create", "delete"]:
            destructive.append(r.get("address"))

    return destructive
