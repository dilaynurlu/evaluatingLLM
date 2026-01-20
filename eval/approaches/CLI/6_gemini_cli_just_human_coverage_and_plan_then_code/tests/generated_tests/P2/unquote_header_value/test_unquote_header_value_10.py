import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_filename_with_escaped_quote():
    # "filename=\"foo.txt\"" -> filename="foo.txt"
    val = r'"filename=\"foo.txt\""'
    assert unquote_header_value(val, is_filename=True) == 'filename="foo.txt"'
