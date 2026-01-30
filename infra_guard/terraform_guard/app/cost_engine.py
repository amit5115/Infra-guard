# from plan_utils import load_plan
from .plan_utils import load_plan


# -------------------------------
# Approx monthly pricing (USD)
# Conservative / safe defaults
# -------------------------------
GCP_PRICING = {
    # VM pricing (approx)
    "google_compute_instance": {
        "e2-micro": 6,
        "e2-small": 14,
        "e2-medium": 28,
        "e2-standard-4": 135,
    },

    # GCS pricing: ~$0.02 per GB-month
    "google_storage_bucket": {
        "per_gb": 0.02,
        "default_gb": 50,   # assume 50GB if size unknown
    },

    # GKE Zonal cluster
    "google_container_cluster": {
        "control_plane": 73,
        "node_e2_medium": 28,
    }
}

# -------------------------------
# Cost helpers
# -------------------------------
def estimate_vm_cost(machine_type):
    if not machine_type:
        return 0
    return GCP_PRICING["google_compute_instance"].get(machine_type, 0)


def estimate_bucket_cost(_):
    size_gb = GCP_PRICING["google_storage_bucket"]["default_gb"]
    return size_gb * GCP_PRICING["google_storage_bucket"]["per_gb"]


def estimate_gke_cost(_):
    return (
        GCP_PRICING["google_container_cluster"]["control_plane"]
        + GCP_PRICING["google_container_cluster"]["node_e2_medium"]
    )


# -------------------------------
# Main cost engine
# -------------------------------
def calculate_cost_impact():
    plan = load_plan()
    results = []
    total_delta = 0

    for r in plan.get("resource_changes", []):
        r_type = r.get("type")
        change = r.get("change", {})
        actions = change.get("actions", [])

        before = change.get("before") or {}
        after = change.get("after") or {}

        before_cost = 0
        after_cost = 0
        before_label = "None"
        after_label = "None"

        # -------- VM --------
        if r_type == "google_compute_instance":
            before_label = before.get("machine_type")
            after_label = after.get("machine_type")

            before_cost = estimate_vm_cost(before_label)
            after_cost = estimate_vm_cost(after_label)

        # -------- GCS Bucket --------
        elif r_type == "google_storage_bucket":
            before_label = "No Bucket"
            after_label = "GCS Bucket"

            after_cost = estimate_bucket_cost(after)

        # -------- GKE Cluster --------
        elif r_type == "google_container_cluster":
            before_label = "No Cluster"
            after_label = "Zonal GKE Cluster"

            after_cost = estimate_gke_cost(after)

        else:
            continue  # IAM / SA / bindings

        delta = after_cost - before_cost
        total_delta += delta

        results.append({
            "resource": r.get("address"),
            "action": actions,
            "before": before_label,
            "after": after_label,
            "before_cost": before_cost,
            "after_cost": after_cost,
            "delta": delta,
        })

    return results, total_delta
