import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_whitespace_and_control_chars():
    """
    Test that excessive whitespace and control characters (tabs, newlines) 
    around separators are handled or stripped correctly.
    """
    header = "  text/html  ; \t charset  =  utf-8 \r\n ; version = 1.0 "
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/html"
    assert params["charset"] == "utf-8"
    assert params["version"] == "1.0"