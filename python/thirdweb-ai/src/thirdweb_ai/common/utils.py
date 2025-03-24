import re


def extract_digits(value: int | str) -> int:
    value_str = str(value).strip("\"'")
    digit_match = re.search(r"\d+", value_str)

    if not digit_match:
        raise ValueError(f"Chain ID '{value}' does not contain any digits")

    extracted_digits = digit_match.group()

    if not extracted_digits.isdigit():
        raise ValueError(
            f"Extracted value '{extracted_digits}' is not a valid digit string"
        )
    return int(extracted_digits)


def normalize_chain_id(
    chain_id: int | str | list[int | str] | None,
) -> int | list[int] | None:
    """Normalize chain IDs to integers."""

    if chain_id is None:
        return None

    if isinstance(chain_id, list):
        return [extract_digits(c) for c in chain_id]

    return extract_digits(chain_id)
