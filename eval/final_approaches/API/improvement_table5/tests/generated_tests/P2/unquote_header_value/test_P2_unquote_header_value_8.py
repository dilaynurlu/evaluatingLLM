import pytest
from requests.utils import unquote_header_value

def test_unquote_mismatched_quotes():
    """
    Test that a string with mismatched quotes (start but no end, or vice versa)
    is returned as-is without stripping.
    """
    input_value = '"mismatched'
    result = unquote_header_value(input_value)
    assert result == '"mismatched'