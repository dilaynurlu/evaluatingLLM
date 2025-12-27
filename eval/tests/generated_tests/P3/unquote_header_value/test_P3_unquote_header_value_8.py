import pytest
from requests.utils import unquote_header_value

def test_unquote_filename_ie_style():
    """
    Test unquoting of IE-style filenames with double backslashes.
    The function handles fixing IE uploads like "C:\\foo\\bar.txt" by converting
    double backslashes to single backslashes if it is a filename but not a UNC path.
    """
    # Input: "C:\\path\\to\\file.txt"
    # This simulates a browser sending a full local path in the Content-Disposition filename
    header_value = r'"C:\\path\\to\\file.txt"'
    
    # Expected: C:\path\to\file.txt
    expected = r'C:\path\to\file.txt'
    
    result = unquote_header_value(header_value, is_filename=True)
    assert result == expected