import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_non_filename_unc_fix():
    """
    Test that if is_filename is False (default), a value starting with double backslash
    is processed (unescaped), converting the leading double backslash to a single one.
    This simulates the fix for IE uploads.
    """
    # Input: "\\server\share" (surrounded by quotes)
    # The function sees starts with \\ but is_filename=False.
    # It proceeds to replace '\\\\' with '\\'.
    # \\\\ in the input string (Python literal r"\\") becomes \.
    # So \\server... becomes \server...
    value = r'"\\server\share"'
    expected = r"\server\share"
    
    assert unquote_header_value(value, is_filename=False) == expected