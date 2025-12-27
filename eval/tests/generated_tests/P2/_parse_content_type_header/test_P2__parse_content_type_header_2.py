import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_header_with_charset_whitespace():
    """
    Test parsing a content type header with a charset parameter and whitespace.
    Whitespace around the semicolon and equals sign should be stripped.
    """
    header = "text/html ;  charset =  utf-8 "
    expected_content_type = "text/html"
    expected_params = {"charset": "utf-8"}
    
    result_type, result_params = _parse_content_type_header(header)
    
    assert result_type == expected_content_type
    assert result_params == expected_params