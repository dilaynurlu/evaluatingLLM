from requests.utils import unquote_header_value

def test_unquote_header_value_basic():
    """Test unquoting a simple quoted string."""
    value = '"simple_value"'
    # The function should strip the surrounding quotes.
    assert unquote_header_value(value) == 'simple_value'