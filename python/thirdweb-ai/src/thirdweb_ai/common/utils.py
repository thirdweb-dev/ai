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


def decode_abi_data(encoded_data: str) -> bytes:
    encoded_data = encoded_data.removeprefix("0x")
    return bytes.fromhex(encoded_data)


def clean_resolve(out: dict[str, Any]):
    if "transactions" in out["data"]:
        for transaction in out["data"]["transactions"]:
            if "data" in transaction:
                transaction["data"] = decode_abi_data(transaction["data"])
            if "logs_bloom" in transaction:
                transaction.pop("logs_bloom")
    return out
