import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_duplicate_parameters():
    """
    Test parsing a content-type header with duplicate parameter keys (HTTP Parameter Pollution).
    Verifies that the parser handles duplicates deterministically. 
    In requests, the last value for a given key typically overwrites previous ones.
    """
    header = "text/html; charset=utf-8; charset=iso-8859-1"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/html"
    # Asserting that the last occurrence wins
    assert params == {"charset": "iso-8859-1"}