import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_none():
    """
    Test that None input is handled gracefully and returned as None.
    """
    result = unquote_header_value(None)
    assert result is None