import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_escaped_chars():
    """
    Test unquoting of a string containing escaped quotes and backslashes.
    \" should become "
    \\ should become \
    """
    # Input represents: "foo\"bar\\baz"
    # Expected: foo"bar\baz
    header_value = r'"foo\"bar\\baz"'
    result = unquote_header_value(header_value)
    assert result == r'foo"bar\baz'