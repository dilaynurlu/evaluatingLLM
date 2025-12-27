import pytest
from requests.utils import unquote_header_value

def test_unquote_basic_quoted_string():
    """
    Test that a standard double-quoted string is correctly stripped of quotes.
    Scenario: Input is "simple_value".
    Expected: simple_value
    """
    input_value = '"simple_value"'
    expected_value = 'simple_value'
    
    result = unquote_header_value(input_value)
    
    assert result == expected_value