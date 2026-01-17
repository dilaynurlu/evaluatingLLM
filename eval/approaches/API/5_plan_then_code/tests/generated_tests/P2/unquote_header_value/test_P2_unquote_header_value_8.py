import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_none():
    """
    Test that passing None returns None immediately.
    """
    result = unquote_header_value(None)
    assert result is None