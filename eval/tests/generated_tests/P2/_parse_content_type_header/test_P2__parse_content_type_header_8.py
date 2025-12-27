import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_header_value_containing_equals():
    """
    Test parsing a parameter value that contains an equals sign.
    The parser should split only on the first equals sign found.
    """
    header = "application/x-www-form-urlencoded; key=value=with=equals"
    expected_content_type = "application/x-www-form-urlencoded"
    expected_params = {"key": "value=with=equals"}
    
    result_type, result_params = _parse_content_type_header(header)
    
    assert result_type == expected_content_type
    assert result_params == expected_params