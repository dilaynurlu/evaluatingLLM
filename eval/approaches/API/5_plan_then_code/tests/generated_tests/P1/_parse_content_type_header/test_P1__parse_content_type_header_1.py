from requests.utils import _parse_content_type_header

def test_parse_simple_content_type():
    """Test parsing a header string with only a content type and no parameters."""
    header = "application/json"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "application/json"
    assert params == {}