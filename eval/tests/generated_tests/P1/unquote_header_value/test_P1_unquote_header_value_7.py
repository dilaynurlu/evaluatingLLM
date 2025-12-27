import pytest
from requests.utils import unquote_header_value

def test_unquote_filename_normal_behavior():
    """
    Test that is_filename=True behaves like normal unquoting for non-UNC paths.
    It should still strip quotes and handle normal escapes.
    """
    # Input: "file.txt"
    input_value = '"file.txt"'
    expected_value = 'file.txt'
    
    result = unquote_header_value(input_value, is_filename=True)
    
    assert result == expected_value