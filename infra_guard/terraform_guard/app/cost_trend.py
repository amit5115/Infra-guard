import json
import os

COST_TREND_FILE = "../plans/last_cost.json"

# -------------------------
# Core helpers (internal)
# -------------------------
def _read_last_cost():
    if not os.path.exists(COST_TREND_FILE):
        return None

    try:
        with open(COST_TREND_FILE, "r") as f:
            return json.load(f).get("total")
    except Exception:
        return None


def _write_current_cost(total):
    os.makedirs(os.path.dirname(COST_TREND_FILE), exist_ok=True)
    with open(COST_TREND_FILE, "w") as f:
        json.dump({"total": total}, f)


# -------------------------
# OLD API (used by main.py)
# DO NOT REMOVE
# -------------------------
def load_last_cost():
    return _read_last_cost()


def save_current_cost(total):
    _write_current_cost(total)


# -------------------------
# NEW API (future use)
# -------------------------
def get_latest_trend():
    return _read_last_cost()


def save_trend(total):
    _write_current_cost(total)
