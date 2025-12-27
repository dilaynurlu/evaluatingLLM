import pytest
from requests.utils import unquote_header_value

def test_unquote_no_quotes_input():
    """
    Test that an input string without surrounding quotes is returned unchanged.
    """
    input_value = 'no_quotes_here'
    expected_value = 'no_quotes_here'
    
    result = unquote_header_value(input_value)
    
    assert result == expected_value