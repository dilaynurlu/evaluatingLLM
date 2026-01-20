import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_header_param_without_value():
    header = "text/html; flag"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/html"
    assert params == {"flag": True}
