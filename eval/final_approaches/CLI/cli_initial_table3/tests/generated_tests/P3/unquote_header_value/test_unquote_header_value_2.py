import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_2():
    # filename with backslashes (IE fix check)
    value = r'"C:\\path\\to\\file.txt"'
    # is_filename defaults to False, so it should unescape backslashes
    # wait, the function says:
    # if not is_filename or value[:2] != "\\\\":
    #    return value.replace("\\", "\").replace('\"', '"')
    # So it replaces \\ with \ and \" with "
    
    assert unquote_header_value(value, is_filename=True) == r"C:\path\to\file.txt"

