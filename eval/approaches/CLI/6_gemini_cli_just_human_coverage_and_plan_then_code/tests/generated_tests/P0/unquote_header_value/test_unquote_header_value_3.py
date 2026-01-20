
import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_escaped_quotes():
    # Input: "foo\"bar"
    value = r'"foo\"bar"'
    assert unquote_header_value(value) == 'foo"bar'

