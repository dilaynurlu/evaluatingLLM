from requests.utils import unquote_header_value

def test_unquote_header_value_none():
    """Test handling of None input."""
    assert unquote_header_value(None) is None