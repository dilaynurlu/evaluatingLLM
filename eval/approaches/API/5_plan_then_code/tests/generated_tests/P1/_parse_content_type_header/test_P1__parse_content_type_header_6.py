from requests.utils import _parse_content_type_header

def test_parse_content_type_ignore_empty_params():
    """Test that empty segments (caused by consecutive or trailing semicolons) are ignored."""
    header = "text/plain;; charset=us-ascii;"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/plain"
    assert params == {"charset": "us-ascii"}