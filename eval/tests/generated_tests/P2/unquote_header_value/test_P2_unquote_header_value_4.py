import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_filename_unc_preservation():
    """
    Test that if is_filename=True and the value looks like a UNC path (starts with \\),
    the backslashes are NOT unescaped, to prevent corruption of the UNC path.
    """
    # UNC path: \\server\share
    # Input wrapped in quotes: "\\server\share"
    # The function checks if it starts with \\ after unquoting.
    
    unc_val = r'"\\server\share"'
    expected = r"\\server\share"
    
    # Should just strip quotes, no replace
    assert unquote_header_value(unc_val, is_filename=True) == expected