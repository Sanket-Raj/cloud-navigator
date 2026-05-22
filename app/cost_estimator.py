import json
from typing import Optional

def load_cost_data():
    with open("knowledge/cost_data.json") as f:
        return json.load(f)

def estimate_cost(source: Optional[str], target: Optional[str], service: Optional[str]) -> dict:
    cost_db = load_cost_data()
    if not source or not target:
        return {"message": "Insufficient information for cost comparison"}
    source_cost = cost_db.get(source, {}).get("monthly", "N/A")
    target_cost = cost_db.get(target, {}).get("monthly", "N/A")
    comparison = {
        "source_cloud": source,
        "target_cloud": target,
        "source_estimated_monthly": source_cost,
        "target_estimated_monthly": target_cost,
        "savings": "N/A" if source_cost=="N/A" or target_cost=="N/A" else f"${source_cost - target_cost:.2f}"
    }
    return comparison
