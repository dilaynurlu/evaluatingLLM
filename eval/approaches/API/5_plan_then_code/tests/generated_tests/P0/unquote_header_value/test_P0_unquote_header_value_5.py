import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_filename_normal_unescape():
    """
    Test unquoting a normal filename (not UNC).
    Should unescape backslashes (convert \\ to \).
    """
    # Input represents: "C:\\path\\to\\file.txt"
    # Stripped: C:\\path\\to\\file.txt
    # Should replace \\ with \ -> C:\path\to\file.txt
    input_val = r'"C:\\path\\to\\file.txt"'
    expected = r'C:\path\to\file.txt'
    
    result = unquote_header_value(input_val, is_filename=True)
    assert result == expected