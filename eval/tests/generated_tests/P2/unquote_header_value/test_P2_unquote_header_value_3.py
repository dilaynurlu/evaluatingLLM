import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_mixed_escapes():
    """
    Test unquoting of a string containing escaped backslashes and escaped quotes.
    The function replaces '\\\\' with '\\' first, then '\\"' with '"'.
    Input: "foo\\"bar\"baz"
    Inside quotes: foo\\"bar\"baz
    Replace \\\\ -> \\: foo\"bar\"baz
    Replace \" -> ": foo"bar"baz
    """
    # Input representation: "foo\\"bar\"baz"
    # In Python raw string for the argument: r'"foo\\"bar\"baz"'
    value = r'"foo\\"bar\"baz"'
    expected = 'foo"bar"baz'
    
    assert unquote_header_value(value) == expected