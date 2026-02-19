import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_unescape_chars():
    """
    Test that escaped characters (quotes and backslashes) inside the quoted string
    are unescaped correctly when is_filename is False (default).
    """
    # Input: "foo\"bar" -> Expected: foo"bar
    assert unquote_header_value(r'"foo\"bar"') == 'foo"bar'
    
    # Input: "foo\\bar" -> Expected: foo\bar
    # Note: The function replaces \\ with \
    assert unquote_header_value(r'"foo\\bar"') == r"foo\bar"
    
    # Input: "foo\"\\bar" -> Expected: foo"\bar
    assert unquote_header_value(r'"foo\"\\bar"') == 'foo"\\bar'