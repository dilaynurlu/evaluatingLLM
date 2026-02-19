from requests.utils import unquote_header_value

def test_unquote_header_value_basic_quoted():
    """Test unquoting of a simple double-quoted string."""
    header_value = '"simple_value"'
    result = unquote_header_value(header_value)
    assert result == "simple_value"