import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_single_quotes():
    """Test that single quotes are stripped from parameters just like double quotes."""
    header = "application/xml; schema='http://example.com'"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "application/xml"
    assert params == {"schema": "http://example.com"}