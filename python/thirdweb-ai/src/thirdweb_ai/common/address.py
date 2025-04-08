import re

from web3 import Web3


def validate_address(address: str) -> str:
    if not address.startswith("0x") or len(address) != 42:
        raise ValueError(f"Invalid blockchain address format: {address}")

    if not Web3.is_checksum_address(address):
        try:
            return Web3.to_checksum_address(address)
        except ValueError as e:
            raise ValueError(f"Invalid blockchain address: {address}") from e

    return address


def validate_transaction_hash(tx_hash: str) -> str:
    pattern = re.compile(r"^0x[a-fA-F0-9]{64}$")
    if bool(re.fullmatch(pattern, tx_hash)):
        return tx_hash
    raise ValueError(f"Invalid transaction hash: {tx_hash}")


def validate_block_identifier(block_id: str) -> str:
    if block_id.startswith("0x"):
        pattern = re.compile(r"^0x[a-fA-F0-9]{64}$")
        if bool(re.fullmatch(pattern, block_id)):
            return block_id
    elif block_id.isdigit():
        return block_id

    raise ValueError(f"Invalid block identifier: {block_id}")


def validate_signature(signature: str) -> str:
    # Function selector (4 bytes)
    if signature.startswith("0x") and len(signature) == 10:
        pattern = re.compile(r"^0x[a-fA-F0-9]{8}$")
        if bool(re.fullmatch(pattern, signature)):
            return signature
    # Event topic (32 bytes)
    elif signature.startswith("0x") and len(signature) == 66:
        pattern = re.compile(r"^0x[a-fA-F0-9]{64}$")
        if bool(re.fullmatch(pattern, signature)):
            return signature
    # Plain text signature (e.g. "transfer(address,uint256)")
    elif "(" in signature and ")" in signature:
        return signature

    raise ValueError(f"Invalid function or event signature: {signature}")
