import json
from typing import Optional

def load_risk_rules():
    with open("knowledge/risk_rules.json") as f:
        return json.load(f)

def score_risk(source: Optional[str], target: Optional[str], service: Optional[str]) -> dict:
    rules = load_risk_rules()
    risk_level = "low"
    reasons = []
    if source and target:
        for rule in rules:
            if rule.get("source") == source and rule.get("target") == target:
                risk_level = rule.get("level", "low")
                reasons = rule.get("reasons", [])
                break
    return {"level": risk_level, "factors": reasons}
