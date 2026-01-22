from requests.utils import unquote_header_value

def test_unquote_header_value_no_quotes():
    """Test that a string without surrounding quotes is returned unchanged."""
    value = 'no_quotes_here'
    assert unquote_header_value(value) == 'no_quotes_here'