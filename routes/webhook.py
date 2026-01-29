"""GitHub webhook endpoint (TASK COMPLIANT)."""

import hashlib
import hmac
from flask import Blueprint, request, jsonify, current_app

from services.github_service import parse_webhook_payload
from models.event_model import EventModel

webhook_bp = Blueprint("webhook", __name__)


def verify_signature(payload_body, signature_header, secret):
    """
    Verify GitHub webhook signature (optional security).

    Args:
        payload_body: Raw request body (bytes)
        signature_header: X-Hub-Signature-256 header
        secret: Shared webhook secret

    Returns:
        bool: True if valid, False otherwise
    """
    if not signature_header or not secret:
        return False

    mac = hmac.new(
        secret.encode("utf-8"),
        msg=payload_body,
        digestmod=hashlib.sha256
    )
    expected_signature = "sha256=" + mac.hexdigest()

    return hmac.compare_digest(expected_signature, signature_header)


@webhook_bp.route("/webhook", methods=["POST"])
def receive_webhook():
    try:
        event_type = request.headers.get("X-GitHub-Event")
        signature = request.headers.get("X-Hub-Signature-256")
        payload = request.get_json()

        # ✅ HANDLE PING FIRST
        if event_type == "ping":
            return jsonify({"status": "pong"}), 200

        webhook_secret = current_app.config.get("GITHUB_WEBHOOK_SECRET")
        if webhook_secret:
            if not verify_signature(request.data, signature, webhook_secret):
                return jsonify({"error": "Invalid signature"}), 401

        event_data = parse_webhook_payload(event_type, payload)

        if not event_data:
            return jsonify({"status": "ignored"}), 200

        EventModel.create_event(event_data)

        return jsonify({"status": "success"}), 200

    except Exception as e:
        current_app.logger.error(f"Webhook error: {e}")
        return jsonify({"error": "Internal server error"}), 500


# Add GET /webhook for health/debugging
@webhook_bp.route("/webhook", methods=["GET"])
def webhook_health():
    return jsonify({"status": "Webhook endpoint is up"}), 200

