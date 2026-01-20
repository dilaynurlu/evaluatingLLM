import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_escaped_quote():
    value = r'"foo\"bar"'
    assert unquote_header_value(value) == 'foo"bar'
