import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_filename_backslash():
    # IE uploads files with full path like "C:\foo\bar.txt"
    # But browsers might quote it: "C:\foo\bar.txt"
    # unquote_header_value handles replace("\\", "\").replace('\"', '"') if not is_filename or ...
    
    # Wait, unquote_header_value(value, is_filename=False)
    # if value[:2] != "\\" (UNC path)
    
    value = '"C:\\foo\\bar.txt"' # In python string "C:\foo\bar.txt"
    # expected: C:\foo\bar.txt
    
    assert unquote_header_value(value, is_filename=True) == r"C:\foo\bar.txt"
