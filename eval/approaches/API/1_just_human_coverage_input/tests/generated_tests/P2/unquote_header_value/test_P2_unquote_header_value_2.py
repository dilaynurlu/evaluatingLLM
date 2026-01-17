import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_escaped_backslash():
    """
    Test that escaped backslashes are unescaped when is_filename is False.
    Input: "foo\\bar" (quoted string containing foo\bar with escaped backslash)
    Expected: foo\bar
    """
    # Input represents quoted string "foo\\bar"
    # The content inside quotes is foo\\bar
    # unquote_header_value should strip quotes -> foo\\bar
    # Then replace \\ with \ -> foo\bar
    value = r'"foo\\bar"'
    expected = r"foo\bar"
    assert unquote_header_value(value) == expected