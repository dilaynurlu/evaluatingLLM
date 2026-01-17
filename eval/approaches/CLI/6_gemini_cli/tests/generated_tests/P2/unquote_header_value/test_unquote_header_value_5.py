import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_filename_escaped():
    # "foo\\bar" -> foo\bar
    val = r'"foo\\bar"'
    assert unquote_header_value(val, is_filename=True) == r"foo\bar"
