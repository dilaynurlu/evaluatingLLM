from requests.utils import unquote_header_value

def test_unquote_header_value_none():
    """Test that None input returns None."""
    assert unquote_header_value(None) is None