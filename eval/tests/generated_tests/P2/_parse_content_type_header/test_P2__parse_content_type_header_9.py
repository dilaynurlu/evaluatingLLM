import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_header_key_stripping():
    """
    Test that quotes around parameter keys are stripped, similar to values.
    """
    header = 'text/csv; "header"=present'
    expected_content_type = "text/csv"
    expected_params = {"header": "present"}
    
    result_type, result_params = _parse_content_type_header(header)
    
    assert result_type == expected_content_type
    assert result_params == expected_params