import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_empty_string():
    """
    Test that passing an empty string returns an empty string.
    """
    result = unquote_header_value("")
    assert result == ""