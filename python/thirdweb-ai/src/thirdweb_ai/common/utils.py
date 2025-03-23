def normalize_chain_id(
    chain_id: int | str | list[int | str] | None,
) -> int | list[int] | None:
    """Normalize chain IDs to integers."""
    if chain_id is None:
        return None

    if isinstance(chain_id, list):
        return [int(str(c).strip("\"'")) for c in chain_id]

    chain_id_str = str(chain_id).strip("\"'")
    return int(chain_id_str)
