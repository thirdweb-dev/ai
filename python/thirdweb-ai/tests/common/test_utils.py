import pytest

from thirdweb_ai.common.utils import normalize_chain_id


class TestNormalizeChainId:
    def test_none_input(self):
        assert normalize_chain_id(None) is None

    def test_integer_input(self):
        assert normalize_chain_id(1) == 1
        assert normalize_chain_id(137) == 137

    def test_string_numeric_input(self):
        assert normalize_chain_id("1") == 1
        assert normalize_chain_id("137") == 137
        assert normalize_chain_id("'137'") == 137
        assert normalize_chain_id('"137"') == 137

    def test_string_with_text(self):
        assert normalize_chain_id("ethereum-1") == 1
        assert normalize_chain_id("polygon-137") == 137
        assert normalize_chain_id("Chain ID: 56") == 56

    def test_list_input(self):
        assert normalize_chain_id([1, "2", "ethereum-3"]) == [1, 2, 3]
        assert normalize_chain_id(["1", 2, "polygon-137"]) == [1, 2, 137]

    def test_no_digits(self):
        with pytest.raises(ValueError, match="does not contain any digits"):
            normalize_chain_id("ethereum")

        with pytest.raises(ValueError, match="does not contain any digits"):
            normalize_chain_id("polygon")

        with pytest.raises(ValueError, match="does not contain any digits"):
            normalize_chain_id(["ethereum", "polygon"])
