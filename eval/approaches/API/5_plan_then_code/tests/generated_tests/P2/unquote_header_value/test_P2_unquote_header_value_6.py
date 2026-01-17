import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_single_quotes_ignored():
    """
    Test that strings surrounded by single quotes are NOT unquoted.
    The function only looks for double quotes.
    """
    input_value = "'SingleQuoted'"
    expected_value = "'SingleQuoted'"
    
    result = unquote_header_value(input_value)
    
    assert result == expected_value