import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_escaped_slash():
    value = r'"foo\\bar"'
    assert unquote_header_value(value) == r"foo\bar"

