import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_local_filename_unescapes():
    """
    Test that a local filename path (e.g. C:\...) is unescaped even if is_filename is True,
    because it does not start with a UNC prefix (\\).
    """
    # Input represents quoted string "C:\\foo\\bar.txt"
    # Content: C:\\foo\\bar.txt
    # is_filename=True, but does not start with \\.
    # Replacements occur: \\ -> \
    # Result: C:\foo\bar.txt
    value = r'"C:\\foo\\bar.txt"'
    expected = r"C:\foo\bar.txt"
    
    assert unquote_header_value(value, is_filename=True) == expected