from requests.utils import _parse_content_type_header

def test_parse_content_type_with_parameters():
    """Test parsing a content type header with standard parameters."""
    header = "text/html; charset=utf-8; version=1.0"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/html"
    assert params == {"charset": "utf-8", "version": "1.0"}