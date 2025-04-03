import re
from typing import Any


def extract_digits(value: int | str) -> int:
    value_str = str(value).strip("\"'")
    digit_match = re.search(r"\d+", value_str)

    if not digit_match:
        raise ValueError(f"Input '{value}' does not contain any digits")

    extracted_digits = digit_match.group()

    if not extracted_digits.isdigit():
        raise ValueError(f"Extracted value '{extracted_digits}' is not a valid digit string")
    return int(extracted_digits)


def normalize_chain_id(
    in_value: int | str | list[int | str] | None,
) -> int | list[int] | None:
    """Normalize str values integers."""

    if in_value is None:
        return None

    if isinstance(in_value, list):
        return [extract_digits(c) for c in in_value]

    return extract_digits(in_value)


def is_encoded(encoded_data: str) -> bool:
    encoded_data = encoded_data.removeprefix("0x")

    try:
        bytes.fromhex(encoded_data)
        return True
    except ValueError:
        return False


def clean_resolve(out: dict[str, Any]):
    if "transactions" in out["data"]:
        for transaction in out["data"]["transactions"]:
            if "data" in transaction and is_encoded(transaction["data"]):
                transaction.pop("data")
            if "logs_bloom" in transaction:
                transaction.pop("logs_bloom")
    return out
