from requests.utils import unquote_header_value

def test_unquote_header_value_no_quotes():
    """Test that a string without surrounding quotes is returned unchanged."""
    header_value = 'simple_value'
    result = unquote_header_value(header_value)
    assert result == "simple_value"