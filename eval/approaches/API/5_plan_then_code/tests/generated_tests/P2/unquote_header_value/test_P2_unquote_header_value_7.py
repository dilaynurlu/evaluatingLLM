import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_mismatched_quotes():
    """
    Test that strings with mismatched quotes (e.g. starting with " but not ending with ")
    are returned as-is without modification.
    """
    input_value = '"Mismatched'
    expected_value = '"Mismatched'
    
    result = unquote_header_value(input_value)
    
    assert result == expected_value