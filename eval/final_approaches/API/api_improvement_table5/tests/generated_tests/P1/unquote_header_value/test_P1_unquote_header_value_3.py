from requests.utils import unquote_header_value

def test_unquote_escaped_backslash():
    """Test unquoting a string containing an escaped backslash."""
    # Input represents: "foo\\bar"
    # Expected behavior: strip outer quotes, then replace \\ with \
    input_val = r'"foo\\bar"'
    assert unquote_header_value(input_val) == r'foo\bar'