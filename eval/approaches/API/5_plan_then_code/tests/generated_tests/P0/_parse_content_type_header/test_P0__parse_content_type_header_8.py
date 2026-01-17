from requests.utils import _parse_content_type_header

def test_parse_content_type_duplicate_keys():
    """Test that duplicate keys in header overwrite previous values."""
    header = "text/html; level=1; level=2"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/html"
    assert params == {"level": "2"}