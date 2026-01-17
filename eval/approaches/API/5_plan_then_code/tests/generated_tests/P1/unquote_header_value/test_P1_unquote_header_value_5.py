import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_mismatched_quotes():
    """
    Test that strings without matching start and end quotes are returned as-is.
    """
    # Only start quote
    header_value = '"mismatched'
    result = unquote_header_value(header_value)
    assert result == '"mismatched'