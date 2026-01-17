import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_filename_unc():
    # Input represents "\\server\share"" (quoted string containing UNC path)
    # Inner value: \\server\share
    value = r'"\\server\share"'
    # Should preserve leading double backslash
    assert unquote_header_value(value, is_filename=True) == r"\\server\share"
