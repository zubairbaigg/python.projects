#!/usr/bin/env python3
"""
process_payload.py

Parses a JSON payload, extracts 'name', 'email', and 'message',
then POSTs a formatted summary to the URL defined in the
WEBHOOK_URL environment variable.
"""

import json
import os
import sys
from datetime import datetime

import requests


REQUIRED_FIELDS = ("name", "email", "message")


def extract_fields(payload: str) -> dict:
    """
    Parse a JSON string and extract the required fields.

    Args:
        payload: A JSON-encoded string.

    Returns:
        A dict containing the extracted field values.

    Raises:
        json.JSONDecodeError: If the payload is not valid JSON.
        KeyError: If one or more required fields are missing.
    """
    try:
        data = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise json.JSONDecodeError(
            f"Invalid JSON payload: {exc.msg}", exc.doc, exc.pos
        ) from exc

    missing = [field for field in REQUIRED_FIELDS if field not in data]
    if missing:
        raise KeyError(
            f"Missing required field(s): {', '.join(missing)}"
        )

    return {field: data[field] for field in REQUIRED_FIELDS}


def build_summary(fields: dict) -> dict:
    """Build the summary dict that will be sent to the webhook."""
    return {
        "name": fields["name"],
        "email": fields["email"],
        "message": fields["message"],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def send_summary(summary: dict, webhook_url: str) -> None:
    """
    POST the summary as JSON to the given webhook URL.

    Raises:
        requests.RequestException: On any network or HTTP error.
    """
    response = requests.post(webhook_url, json=summary, timeout=10)
    response.raise_for_status()
    print(f"[OK] Summary sent to webhook (HTTP {response.status_code}).")


def process(payload: str) -> None:
    """End-to-end processing: extract fields and POST the summary."""
    webhook_url = os.environ.get("WEBHOOK_URL")
    if not webhook_url:
        print("[Error] WEBHOOK_URL environment variable is not set.", file=sys.stderr)
        sys.exit(1)

    try:
        fields = extract_fields(payload)
        summary = build_summary(fields)
        send_summary(summary, webhook_url)
    except json.JSONDecodeError as exc:
        print(f"[Error] {exc}", file=sys.stderr)
        sys.exit(1)
    except KeyError as exc:
        print(f"[Error] {exc}", file=sys.stderr)
        sys.exit(1)
    except requests.RequestException as exc:
        print(f"[Error] Webhook request failed: {exc}", file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# Example payloads — edit or replace with real input as needed
# ---------------------------------------------------------------------------

EXAMPLES = [
    # ✅ Valid payload
    '{"name": "Alice Smith", "email": "alice@example.com", "message": "Hello, world!"}',

    # ❌ Missing 'email' field
    '{"name": "Bob Jones", "message": "No email provided here."}',

    # ❌ Malformed JSON
    '{"name": "Carol", "email": "carol@example.com", "message": }',
]


if __name__ == "__main__":
    # If a payload is passed as a command-line argument, use that;
    # otherwise run through the built-in examples.
    if len(sys.argv) > 1:
        process(sys.argv[1])
    else:
        for i, example in enumerate(EXAMPLES, start=1):
            print(f"\n{'═' * 40}")
            print(f"  Example {i}")
            print(f"  Input: {example}")
            print(f"{'═' * 40}")
            process(example)
            print()  # blank line between examples
