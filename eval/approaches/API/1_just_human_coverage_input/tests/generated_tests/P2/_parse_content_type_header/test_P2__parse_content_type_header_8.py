import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_header_ignores_empty_segments():
    # Empty segments caused by double semicolons or trailing semicolons should be ignored
    header = "application/json; ; charset=utf-8; "
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "application/json"
    assert params == {"charset": "utf-8"}