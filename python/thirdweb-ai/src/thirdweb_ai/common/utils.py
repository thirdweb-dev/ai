import re
from datetime import datetime, timezone
from typing import Any


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
            if "data" in transaction and is_encoded(transaction["data"]):
                transaction.pop("data")
            if "logs_bloom" in transaction:
                transaction.pop("logs_bloom")
    return out


def clean_transactions(out: dict[str, Any]):
    """Clean and format transaction data for better LLM readability."""
    transactions = []
    transactions.extend(
        {
            "chain_id": transaction["chain_id"],
            "hash": transaction["hash"],
            "block_hash": transaction["block_hash"],
            "block_number": transaction["block_number"],
            "block_timestamp": datetime.fromtimestamp(transaction["block_timestamp"], tz=timezone.utc).strftime(
                "%Y-%m-%d %H:%M:%S UTC"
            ),
            "from_address": transaction["from_address"],
            "to_address": transaction["to_address"],
            "value": transaction["value"],
            "gas": transaction["gas"],
            "gas_price": transaction["gas_price"],
            "gas_used": transaction["gas_used"],
            "cumulative_gas_used": transaction["cumulative_gas_used"],
            "effective_gas_price": transaction["effective_gas_price"],
            "blob_gas_used": transaction["blob_gas_used"],
            "blob_gas_price": transaction["blob_gas_price"],
            "max_fee_per_gas": transaction["max_fee_per_gas"],
            "max_priority_fee_per_gas": transaction["max_priority_fee_per_gas"],
            "transaction_type": transaction["transaction_type"],
            "contract_address": transaction["contract_address"],
            "status": transaction["status"],
        }
        for transaction in out["data"]
    )
    out["data"] = transactions
    return out
