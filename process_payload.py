#!/usr/bin/env python3
"""
process_payload.py

Parses a JSON payload and prints a formatted summary of the
'name', 'email', and 'message' fields. Handles missing or
malformed input gracefully.
"""

import json
import sys
from datetime import datetime


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


def print_summary(fields: dict) -> None:
    """Print a formatted summary of the extracted fields."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    separator = "─" * 40
    print(separator)
    print("         📋  Message Summary")
    print(separator)
    print(f"  Name   : {fields['name']}")
    print(f"  Email  : {fields['email']}")
    print(f"  Message: {fields['message']}")
    print(f"  Time   : {timestamp}")
    print(separator)


def process(payload: str) -> None:
    """End-to-end processing: extract fields and print the summary."""
    try:
        fields = extract_fields(payload)
        print_summary(fields)
    except json.JSONDecodeError as exc:
        print(f"[Error] {exc}", file=sys.stderr)
        sys.exit(1)
    except KeyError as exc:
        print(f"[Error] {exc}", file=sys.stderr)
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
