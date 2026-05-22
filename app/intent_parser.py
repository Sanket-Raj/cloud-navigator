import re

def parse_intent(text: str) -> dict:
    text_lower = text.lower()
    clouds = ["aws", "azure", "oci", "gcp"]
    detected_src = None
    detected_tgt = None
    found = []
    for cloud in clouds:
        if cloud in text_lower:
            found.append(cloud)
    if len(found) >= 2:
        detected_src, detected_tgt = found[0], found[1]
    elif len(found) == 1:
        detected_src = found[0]
    services = ["ec2", "s3", "rds", "lambda", "vm", "blob", "sql", "function"]
    detected_service = None
    for svc in services:
        if svc in text_lower:
            detected_service = svc
            break
    return {"source": detected_src, "target": detected_tgt, "service": detected_service}
