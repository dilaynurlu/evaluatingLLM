import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_unc_path():
    value = r'"\\server\share\file.txt"'
    # starts with \, so should return without unescaping backslashes?
    
    assert unquote_header_value(value, is_filename=True) == r'\\server\share\file.txt'