import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_header_simple_mime_type():
    header = "application/xml"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "application/xml"
    assert params == {}