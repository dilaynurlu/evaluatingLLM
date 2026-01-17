import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_header_complex():
    header = " application/json ;  version = 1 ; FLAG ; charset='utf-8' "
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "application/json"
    assert params == {"version": "1", "flag": True, "charset": "utf-8"}
