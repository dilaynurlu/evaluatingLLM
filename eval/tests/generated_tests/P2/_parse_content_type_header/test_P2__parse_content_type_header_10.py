import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_header_empty_value():
    """
    Test parsing a parameter with a key but an empty value (key=).
    It should result in an empty string value.
    """
    header = "text/html; charset="
    expected_content_type = "text/html"
    expected_params = {"charset": ""}
    
    result_type, result_params = _parse_content_type_header(header)
    
    assert result_type == expected_content_type
    assert result_params == expected_params