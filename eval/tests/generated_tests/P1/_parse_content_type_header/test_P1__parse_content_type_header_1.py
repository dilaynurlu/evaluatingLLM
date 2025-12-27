import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_basic_no_params():
    """
    Test that a simple Content-Type header without parameters is parsed correctly.
    It should return the content type string and an empty dictionary.
    """
    header = "application/json"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "application/json"
    assert params == {}