import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_simple_quoted():
    """
    Test that a simple string surrounded by double quotes is correctly unquoted.
    """
    input_value = '"SimpleTest"'
    expected_value = 'SimpleTest'
    
    result = unquote_header_value(input_value)
    
    assert result == expected_value