import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_header_with_charset():
    # Scenario: Header with charset param
    header = "text/html; charset=utf-8"
    ctype, params = _parse_content_type_header(header)
    assert ctype == "text/html"
    assert params == {"charset": "utf-8"}
