import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_filename_unc_preserve():
    """
    Test unquoting a filename that is a UNC path (starts with \\).
    Should preserve the double backslash at the start and NOT unescape backslashes,
    to avoid corrupting the UNC path structure.
    """
    # Input represents: "\\server\share\file.txt"
    # Stripped: \\server\share\file.txt
    # Should NOT replace \\ with \
    input_val = r'"\\server\share\file.txt"'
    expected = r'\\server\share\file.txt'
    
    # is_filename=True triggers the UNC check
    result = unquote_header_value(input_val, is_filename=True)
    assert result == expected