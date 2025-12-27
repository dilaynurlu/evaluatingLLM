import pytest
from requests.utils import unquote_header_value

def test_unquote_unc_filename_preserved():
    """
    Test that UNC paths (starting with \\) are preserved when is_filename=True.
    This ensures that the double backslash at the start of a UNC path is not collapsed.
    """
    # Input represents: "\\server\share\file.txt" inside quotes.
    # The string inside quotes starts with \\.
    input_value = r'"\\server\share\file.txt"'
    
    # Expected: The quotes are stripped, but \\ remains \\ (not replaced by \).
    expected_value = r'\\server\share\file.txt'
    
    result = unquote_header_value(input_value, is_filename=True)
    
    assert result == expected_value