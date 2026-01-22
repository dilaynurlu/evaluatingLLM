import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_filename_standard():
    """
    Test that if is_filename=True but the value is NOT a UNC path (e.g. C:\path),
    standard unescaping logic (replace \\ with \) is applied.
    """
    # Windows path with escaped backslashes: "C:\\path\\file.txt"
    # Input wrapped in quotes: "C:\\path\\file.txt" (Literal string representation)
    
    # In python raw string: r'"C:\\path\\file.txt"' -> Content inside is C:\\path\\file.txt
    # This contains double backslashes which need to be unescaped to single backslashes.
    
    win_val = r'"C:\\path\\file.txt"'
    expected = r"C:\path\file.txt"
    
    assert unquote_header_value(win_val, is_filename=True) == expected