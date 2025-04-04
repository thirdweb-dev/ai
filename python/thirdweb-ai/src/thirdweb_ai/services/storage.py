import hashlib
import json
import mimetypes
import os
from dataclasses import asdict, is_dataclass
from io import BytesIO
from pathlib import Path
from typing import Annotated, Any

from pydantic import BaseModel

from thirdweb_ai.services.service import Service
from thirdweb_ai.tools.tool import tool


def read_file_chunks(file_path: str | Path, chunk_size: int = 8192):
    """Read file in chunks to avoid loading entire file into memory."""
    path_obj = Path(file_path) if isinstance(file_path, str) else file_path
    with path_obj.open("rb") as f:
        while chunk := f.read(chunk_size):
            yield chunk


class Storage(Service):
    def __init__(self, secret_key: str):
        super().__init__(base_url="https://storage.thirdweb.com", secret_key=secret_key)
        self.gateway_url = self._get_gateway_url()
        self.gateway_hostname = "ipfscdn.io"

    def _get_gateway_url(self) -> str:
        return hashlib.sha256(self.secret_key.encode()).hexdigest()[:32]

    @tool(description="Fetch content from IPFS by hash. Retrieves data stored on IPFS using the thirdweb gateway.")
    def fetch_ipfs_content(
        self,
        ipfs_hash: Annotated[
            str, "The IPFS hash/URI to fetch content from (e.g., 'ipfs://QmXyZ...'). Must start with 'ipfs://'."
        ],
    ) -> dict[str, Any]:
        if not ipfs_hash.startswith("ipfs://"):
            return {"error": "Invalid IPFS hash"}

        ipfs_hash = ipfs_hash.removeprefix("ipfs://")
        path = f"https://{self.gateway_url}.{self.gateway_hostname}/ipfs/{ipfs_hash}"
        return self._get_file(path)

    def _get_file(self, path: str, params: dict[str, Any] | None = None, headers: dict[str, Any] | None = None):
        _headers = self._make_headers()
        if headers:
            _headers.update(headers)
        response = self.client.get(path, params=params, headers=_headers)
        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "")

        # Handle JSON responses
        if "application/json" in content_type:
            return response.json()

        # Handle binary files (images, pdfs, etc)
        if content_type.startswith(("image/", "application/pdf", "application/octet-stream")):
            return {"content": response.content, "content_type": content_type}

        # Handle text content (html, plain text, etc)
        if content_type.startswith(("text/", "application/xml")):
            return {"content": response.text, "content_type": content_type}

        # Default fallback - try json first, then return content with type
        try:
            return response.json()
        except ValueError:
            return {"content": response.content, "content_type": content_type}

    def _post_file(self, url: str, files: dict[str, Any]) -> dict[str, Any]:
        """Post files to a URL with proper authorization headers."""
        headers = self._make_headers()
        headers.pop("Content-Type", None)

        response = self.client.post(url, files=files, headers=headers)
        response.raise_for_status()
        return response.json()

    def _is_json_serializable(self, data: Any) -> bool:
        """Check if data is JSON serializable (dict, dataclass, or BaseModel)."""
        return isinstance(data, dict) or is_dataclass(data) or isinstance(data, BaseModel)

    def _convert_to_json(self, data: Any) -> str:
        """Convert data to JSON string."""
        if isinstance(data, dict):
            return json.dumps(data)
        if is_dataclass(data):
            # Handle dataclass properly
            if isinstance(data, type):
                raise ValueError(f"Expected dataclass instance, got dataclass type: {data}")
            return json.dumps(asdict(data))
        if isinstance(data, BaseModel):
            return data.model_dump_json()
        raise ValueError(f"Cannot convert {type(data)} to JSON")

    def _is_valid_path(self, path: str) -> bool:
        """Check if the string is a valid file or directory path."""
        return Path(path).exists()

    def _prepare_directory_files(self, directory_path: Path, chunk_size: int = 8192) -> list[tuple[str, BytesIO, str]]:
        """
        Prepare files from a directory for upload, preserving directory structure.
        Returns a list of tuples (relative_path, file_buffer, content_type).
        """
        files_data = []

        for root, _, files in os.walk(directory_path):
            for file in files:
                file_path = Path(root) / file
                # Preserve the directory structure in the relative path
                relative_path = str(file_path.relative_to(directory_path))
                content_type = mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"

                # Create a buffer and read the file in chunks
                buffer = BytesIO()
                for chunk in read_file_chunks(file_path, chunk_size):
                    buffer.write(chunk)
                buffer.seek(0)  # Reset buffer position

                files_data.append((relative_path, buffer, content_type))

        return files_data

    @tool(
        description="Upload a file, directory, or JSON data to IPFS. Stores any type on decentralized storage and returns an IPFS URI."
    )
    def upload_to_ipfs(
        self,
        data: Annotated[
            Any, "Data to upload: can be a file path, directory path, dict, dataclass, or BaseModel instance."
        ],
    ) -> str:
        """
        Upload data to IPFS and return the IPFS hash.

        Supports:
        - File paths (streams content)
        - Directory paths (preserves directory structure)
        - Dict objects (converted to JSON)
        - Dataclass instances (converted to JSON)
        - Pydantic BaseModel instances (converted to JSON)

        Always uses streaming for file uploads to handle large files efficiently.
        """
        storage_url = f"{self.base_url}/ipfs/upload"

        # Handle JSON-serializable data types
        if self._is_json_serializable(data):
            json_content = self._convert_to_json(data)
            files = {"file": ("data.json", BytesIO(json_content.encode()), "application/json")}
            body = self._post_file(storage_url, files)
            return f"ipfs://{body['IpfsHash']}"

        # Handle string paths to files or directories
        if isinstance(data, str) and self._is_valid_path(data):
            path = Path(data)

            # Single file upload with streaming
            if path.is_file():
                content_type = mimetypes.guess_type(str(path))[0] or "application/octet-stream"

                # Create a buffer to hold chunks for streaming upload
                buffer = BytesIO()
                for chunk in read_file_chunks(path):
                    buffer.write(chunk)

                buffer.seek(0)  # Reset buffer position
                files = {"file": (path.name, buffer, content_type)}
                body = self._post_file(storage_url, files)
                return f"ipfs://{body['IpfsHash']}"

            # Directory upload - preserve directory structure
            if path.is_dir():
                # Prepare all files from the directory with preserved structure
                files_data = self._prepare_directory_files(path)

                if not files_data:
                    raise ValueError(f"Directory is empty: {data}")

                files_dict = {
                    f"file{i}": (relative_path, buffer, content_type)
                    for i, (relative_path, buffer, content_type) in enumerate(files_data)
                }
                body = self._post_file(storage_url, files_dict)
                return f"ipfs://{body['IpfsHash']}"

            raise ValueError(f"Path exists but is neither a file nor a directory: {data}")

        try:
            content_type = mimetypes.guess_type(data)[0] or "application/octet-stream"
            files = {"file": ("data.txt", BytesIO(data.encode()), content_type)}
            body = self._post_file(storage_url, files)
            return f"ipfs://{body['IpfsHash']}"
        except TypeError as e:
            raise TypeError(
                f"Unsupported data type: {type(data)}. Must be a valid file/directory path, dict, dataclass, or BaseModel."
            ) from e
