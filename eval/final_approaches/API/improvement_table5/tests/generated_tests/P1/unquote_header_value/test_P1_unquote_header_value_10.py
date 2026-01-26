from requests.utils import unquote_header_value

def test_unquote_none_value():
    """Test that None is handled safely and returns None."""
    assert unquote_header_value(None) is None