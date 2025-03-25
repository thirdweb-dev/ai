from thirdweb_ai.common.utils import normalize_chain_id
from thirdweb_ai.services.insight import Insight


class DevInsight(Insight):
    """Subclass of Insight that uses the dev URL by default."""

    def __init__(self, chain_id: list[str | int] | str | int | None = None):
        self.base_url = "https://insight.thirdweb-dev.com"
        normalized = normalize_chain_id(chain_id)
        self.chain_ids = normalized if isinstance(normalized, list) else [normalized]


class TestInsight:
    """Tests for the Insight service using the dev environment."""

    def __init__(self):
        self.insight = DevInsight()

    def test_initialization(self):
        """Test initialization with various chain_id formats."""
        assert self.insight.chain_ids is None
