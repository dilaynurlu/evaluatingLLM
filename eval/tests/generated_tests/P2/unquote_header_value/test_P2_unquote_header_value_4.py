import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_filename_unc_preservation():
    """
    Test that if is_filename is True and the value starts with a UNC path (double backslash),
    it is returned without any unescaping (preserving the double backslash and any other escapes).
    """
    # Input: "\\server\share\file.txt" (surrounded by quotes)
    # The function sees it starts with \\ and is_filename=True, so it returns the stripped content immediately.
    value = r'"\\server\share\file.txt"'
    expected = r"\\server\share\file.txt"
    
    assert unquote_header_value(value, is_filename=True) == expected