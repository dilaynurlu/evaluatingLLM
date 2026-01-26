import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_escaped_quotes():
    """Test unquoting string with escaped quotes."""
    value = '"foo\"bar"'
    # Inner: foo"bar -> replace " with " -> foo"bar
    assert unquote_header_value(value) == 'foo"bar'

