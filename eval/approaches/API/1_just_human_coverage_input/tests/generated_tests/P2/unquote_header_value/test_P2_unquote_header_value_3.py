import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_unc_filename_preserves_backslashes():
    """
    Test that when is_filename is True and the value looks like a UNC path (starts with \\),
    backslashes are NOT unescaped (to preserve UNC path structure).
    """
    # Input represents quoted string "\\server\share"
    # Content: \\server\share
    # Since is_filename=True and it starts with \\, replacements are skipped.
    value = r'"\\server\share"'
    expected = r"\\server\share"
    
    assert unquote_header_value(value, is_filename=True) == expected