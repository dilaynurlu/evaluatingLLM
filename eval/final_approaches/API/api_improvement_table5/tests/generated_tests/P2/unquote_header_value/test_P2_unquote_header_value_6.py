import pytest
from requests.utils import unquote_header_value

def test_unquote_filename_normal_processing():
    """
    Test that when is_filename=True, a value that does NOT start with a UNC path
    is unquoted and unescaped normally.
    """
    # Input represents: "C:\\Folder\\File.txt" (standard IE upload behavior mentioned in comments)
    input_value = r'"C:\\Folder\\File.txt"'
    
    result = unquote_header_value(input_value, is_filename=True)
    
    # Logic:
    # 1. Strips quotes -> C:\\Folder\\File.txt
    # 2. Checks is_filename (True) but starts with C: (not \\)
    # 3. Performs replace: \\ -> \
    # Returns: C:\Folder\File.txt
    assert result == r"C:\Folder\File.txt"