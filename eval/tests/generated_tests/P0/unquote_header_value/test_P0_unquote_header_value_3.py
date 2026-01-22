from requests.utils import unquote_header_value

def test_unquote_header_value_escaped_backslash():
    """Test unquoting a string containing an escaped backslash."""
    # Input represents: "foo\\bar"
    # The function should replace \\ with \
    value = r'"foo\\bar"'
    assert unquote_header_value(value) == r'foo\bar'