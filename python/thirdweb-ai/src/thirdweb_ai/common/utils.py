import re
from typing import Any

TRANSACTION_KEYS_TO_KEEP = [
    "hash",
    "block_number",
    "block_timestamp",
    "from_address",
    "to_address",
    "value",
    "decodedData",
]
EVENT_KEYS_TO_KEEP = [
    "block_number",
    "block_timestamp",
    "address",
    "transaction_hash",
    "transaction_index",
    "log_index",
    "topics",
    "data",
    "decodedData",
]


def extract_digits(value: int | str) -> int:
    """Extract the integer value from a string or return the integer directly."""
    if isinstance(value, int):
        return value

    value_str = str(value).strip("\"'")
    digit_match = re.search(r"\d+", value_str)

    if not digit_match:
        raise ValueError(f"Input '{value}' does not contain any digits")

    extracted_digits = digit_match.group()

    if not extracted_digits.isdigit():
        raise ValueError(f"Extracted value '{extracted_digits}' is not a valid digit string")
    return int(extracted_digits)


def is_encoded(encoded_data: str) -> bool:
    """Check if a string is a valid hexadecimal value."""
    encoded_data = encoded_data.removeprefix("0x")

    try:
        bytes.fromhex(encoded_data)
        return True
    except ValueError:
        return False


def clean_resolve(out: dict[str, Any]):
    """Clean the response from the resolve function."""
    if "transactions" in out["data"]:
        for transaction in out["data"]["transactions"]:
            for key in list(transaction.keys()):
                if key not in TRANSACTION_KEYS_TO_KEEP:
                    transaction.pop(key, None)
    if "events" in out["data"]:
        for event in out["data"]["events"]:
            for key in list(event.keys()):
                if key not in EVENT_KEYS_TO_KEEP:
                    event.pop(key, None)
    return out


def filter_response_keys(items: list[dict[str, Any]], keys_to_keep: list[str] | None) -> list[dict[str, Any]]:
    """Filter the response items to only include the specified keys"""
    if not keys_to_keep:
        return items

    for item in items:
        keys_to_remove = [key for key in item if key not in keys_to_keep]
        for key in keys_to_remove:
            item.pop(key, None)
    return items
