# cost_guard.py
MAX_MONTHLY_COST = 50  # USD (change later)

def is_cost_allowed(costs):
    # flatten if nested
    if costs and isinstance(costs[0], list):
        costs = costs[0]

    total = sum(c["delta"] for c in costs)
    return total <= 100, total
