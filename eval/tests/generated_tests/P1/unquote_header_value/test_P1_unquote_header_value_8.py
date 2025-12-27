import pytest
from requests.utils import unquote_header_value

def test_unquote_mismatched_quotes():
    """
    Test that strings with mismatched quotes are not unquoted.
    """
    # Case: Starts with quote but doesn't end with quote
    input_value = '"mismatched'
    expected_value = '"mismatched'
    
    result = unquote_header_value(input_value)
    
    assert result == expected_value