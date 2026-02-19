from requests.utils import unquote_header_value

def test_unquote_header_value_empty():
    """Test handling of an empty string."""
    assert unquote_header_value('') == ''