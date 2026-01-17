import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_escaped_chars():
    """
    Test unquoting a string with escaped characters (quotes and backslashes).
    \" should become "
    \\ should become \
    """
    # Input represents: "foo\"bar\\baz"
    # Inside quotes: foo\"bar\\baz
    # Expected: foo"bar\baz
    input_val = r'"foo\"bar\\baz"'
    expected = r'foo"bar\baz'
    
    result = unquote_header_value(input_val, is_filename=False)
    assert result == expected