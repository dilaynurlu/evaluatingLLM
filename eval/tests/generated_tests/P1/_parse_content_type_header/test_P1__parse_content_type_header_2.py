import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_with_single_param():
    """
    Test that a Content-Type header with a single unquoted parameter is parsed correctly.
    """
    header = "text/html; charset=utf-8"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/html"
    assert params == {"charset": "utf-8"}