from requests.utils import unquote_header_value

def test_unquote_header_value_empty_quoted():
    """Test unquoting of an empty quoted string."""
    header_value = '""'
    result = unquote_header_value(header_value)
    assert result == ""