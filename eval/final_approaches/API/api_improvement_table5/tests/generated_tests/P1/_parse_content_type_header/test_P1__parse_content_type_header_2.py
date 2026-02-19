import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_with_charset_param():
    """Test parsing a content type header with a single charset parameter."""
    header = "text/html; charset=utf-8"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/html"
    assert params == {"charset": "utf-8"}