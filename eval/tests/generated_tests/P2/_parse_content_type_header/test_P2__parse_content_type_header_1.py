import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_header_simple_no_params():
    """
    Test parsing a simple content type header with no parameters.
    It should return the content type string and an empty dictionary.
    """
    header = "application/json"
    expected_content_type = "application/json"
    expected_params = {}
    
    result_type, result_params = _parse_content_type_header(header)
    
    assert result_type == expected_content_type
    assert result_params == expected_params