import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_header_empty():
    # Scenario: Empty string or weird whitespace
    # If header is empty string, split returns ['']
    # content_type='', params=[]
    header = ""
    ctype, params = _parse_content_type_header(header)
    assert ctype == ""
    assert params == {}
