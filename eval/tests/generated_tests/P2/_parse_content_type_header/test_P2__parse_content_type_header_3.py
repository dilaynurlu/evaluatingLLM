import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_header_quoted_values():
    """
    Test parsing parameters where values are enclosed in double quotes.
    The quotes should be stripped from the parsed values.
    """
    header = 'multipart/form-data; boundary="simple_boundary"'
    expected_content_type = "multipart/form-data"
    expected_params = {"boundary": "simple_boundary"}
    
    result_type, result_params = _parse_content_type_header(header)
    
    assert result_type == expected_content_type
    assert result_params == expected_params