from requests.utils import unquote_header_value

def test_unquote_header_value_none_empty():
    """Test None and empty string inputs."""
    assert unquote_header_value(None) is None
    assert unquote_header_value('') == ''
    assert unquote_header_value('""') == ''
