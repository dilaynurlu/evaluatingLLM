from requests.utils import unquote_header_value

def test_unquote_empty_string():
    """Test that an empty string is handled safely."""
    assert unquote_header_value("") == ""