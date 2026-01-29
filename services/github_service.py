"""GitHub webhook payload parsing logic (TASK COMPLIANT)."""

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
        return {
            "request_id": payload["head_commit"]["id"],
            "author": payload["pusher"]["name"],
            "action": "PUSH",
            "from_branch": None,
            "to_branch": payload["ref"].replace("refs/heads/", ""),
            "timestamp": payload["head_commit"]["timestamp"]
        }

    # -------------------------
    # PULL REQUEST / MERGE EVENT
    # -------------------------
    if event_type == "pull_request":
        pr = payload["pull_request"]

        # MERGE (bonus)
        if pr.get("merged"):
            action = "MERGE"
        else:
            action = "PULL_REQUEST"

        return {
            "request_id": str(pr["id"]),
            "author": pr["user"]["login"],
            "action": action,
            "from_branch": pr["head"]["ref"],
            "to_branch": pr["base"]["ref"],
            "timestamp": pr["created_at"]
        }

    # -------------------------
    # IGNORE ALL OTHER EVENTS
    # -------------------------
    return None
