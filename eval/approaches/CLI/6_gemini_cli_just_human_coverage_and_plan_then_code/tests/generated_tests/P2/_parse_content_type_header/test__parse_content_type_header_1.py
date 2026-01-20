import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_header_simple():
    # Scenario: Simple header without params
    header = "text/html"
    ctype, params = _parse_content_type_header(header)
    assert ctype == "text/html"
    assert params == {}
