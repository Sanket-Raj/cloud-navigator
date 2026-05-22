import json
from typing import Optional

def load_service_mappings():
    with open("knowledge/service_mappings.json") as f:
        return json.load(f)

SERVICE_MAP = load_service_mappings()

def generate_runbook(source: str, target: str, service: Optional[str] = None) -> dict:
    steps = []
    if service and service in SERVICE_MAP:
        mapping = SERVICE_MAP[service]
        target_service = mapping.get(target)
        if target_service:
            steps.append(f"Map {source} {service} to {target} {target_service['service']}")
            steps.append(f"Provision {target} resources using Terraform stub")
            steps.append(f"Migrate data from {service} to {target_service['service']}")
    else:
        steps.append(f"Analyze full {source} environment")
        steps.append(f"Design target architecture on {target}")
        steps.append("Set up networking and identity")
        steps.append("Migrate workloads in waves")
    steps.append("Run validation tests")
    steps.append("Cutover traffic")
    return {"source": source, "target": target, "steps": steps}
