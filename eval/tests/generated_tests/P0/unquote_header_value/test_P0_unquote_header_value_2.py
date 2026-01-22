from requests.utils import unquote_header_value

def test_unquote_header_value_escaped_quote():
    """Test unquoting a string containing an escaped quote."""
    # Input represents: "foo\"bar"
    # The function should replace \" with "
    value = r'"foo\"bar"'
    assert unquote_header_value(value) == 'foo"bar'