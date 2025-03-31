import hashlib
import mimetypes
from io import BytesIO
from pathlib import Path
from typing import Annotated, Any

from thirdweb_ai.services.service import Service
from thirdweb_ai.tools.tool import tool


class Storage(Service):
    def __init__(self, secret_key: str):
        super().__init__(base_url="https://storage.thirdweb.com/ipfs", secret_key=secret_key)
        self.gateway_url = self._get_gateway_url()

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
        path = f"https://{self.gateway_url}.ipfscdn.io/ipfs/{ipfs_hash}"
        return self._get(path)

    def _post_file(self, url: str, files: dict[str, Any]) -> dict[str, Any]:
        """Post files to a URL using the client with proper authorization headers."""
        headers = self._make_headers()
        # Remove the Content-Type as httpx will set it correctly for multipart/form-data
        headers.pop("Content-Type", None)

        response = self.client.post(url, files=files, headers=headers)
        response.raise_for_status()
        return response.json()

    @tool(description="Upload a file to IPFS. Stores any file type on decentralized storage and returns an IPFS URI.")
    def upload_ipfs_file(
        self,
        file_path: Annotated[str, "Path to the file to upload."],
    ) -> str:
        """Upload a file (e.g., image, JSON, or any binary data) to IPFS and return the IPFS hash."""
        storage_url = f"{self.base_url}/upload"

        with Path.open(Path(file_path), "rb") as f:
            file_bytes = f.read()

        content_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
        files = {"file": (file_path, BytesIO(file_bytes), content_type)}
        body = self._post_file(storage_url, files)
        return f"ipfs://{body['IpfsHash']}"
