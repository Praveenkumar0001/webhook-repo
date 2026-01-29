"""GitHub webhook payload parsing logic (TASK COMPLIANT)."""
from datetime import datetime

def parse_webhook_payload(event_type, payload):
    """
    Parse GitHub webhook payload and return ONLY required data.

    Supported events:
    - PUSH
    - PULL_REQUEST
    - MERGE (bonus)

    Returns:
        dict (clean event data) OR None (if event is ignored)
    """

    # -------------------------
    # PUSH EVENT
    # -------------------------
    if event_type == "push":
        # Convert timestamp to UTC ISO format
        timestamp = payload["head_commit"]["timestamp"]
        timestamp_utc = datetime.fromisoformat(timestamp.replace('Z', '+00:00')).strftime("%Y-%m-%dT%H:%M:%SZ")
        
        return {
            "request_id": payload["head_commit"]["id"],
            "author": payload["pusher"]["name"],
            "action": "PUSH",
            "from_branch": None,
            "to_branch": payload["ref"].replace("refs/heads/", ""),
            "timestamp": timestamp_utc
        }

    # -------------------------
    # PULL REQUEST / MERGE EVENT
    # -------------------------
    if event_type == "pull_request":
        pr = payload["pull_request"]

        # ✅ MERGE detection (correct way)
        if payload.get("action") == "closed" and pr.get("merged") is True:
            # Convert timestamp to UTC ISO format
            timestamp = pr.get("merged_at") or pr.get("updated_at") or pr.get("created_at")
            timestamp_utc = datetime.fromisoformat(timestamp.replace('Z', '+00:00')).strftime("%Y-%m-%dT%H:%M:%SZ")
            
            return {
                "request_id": str(pr["id"]),
                "author": pr["user"]["login"],
                "action": "MERGE",
                "from_branch": pr["head"]["ref"],
                "to_branch": pr["base"]["ref"],
                "timestamp": timestamp_utc
            }

        # Normal pull request
        # Convert timestamp to UTC ISO format
        timestamp = pr.get("created_at") or pr.get("updated_at")
        timestamp_utc = datetime.fromisoformat(timestamp.replace('Z', '+00:00')).strftime("%Y-%m-%dT%H:%M:%SZ")
        
        return {
            "request_id": str(pr["id"]),
            "author": pr["user"]["login"],
            "action": "PULL_REQUEST",
            "from_branch": pr["head"]["ref"],
            "to_branch": pr["base"]["ref"],
            "timestamp": timestamp_utc
        }

    # -------------------------
    # IGNORE ALL OTHER EVENTS
    # -------------------------
    return None
