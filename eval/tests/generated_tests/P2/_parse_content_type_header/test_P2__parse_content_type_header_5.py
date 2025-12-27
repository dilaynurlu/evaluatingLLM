import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_header_no_equals_flag():
    """
    Test parsing parameters that do not contain an equals sign.
    These should be treated as boolean flags with the value set to True.
    """
    header = "application/octet-stream; some_flag"
    expected_content_type = "application/octet-stream"
    expected_params = {"some_flag": True}
    
    result_type, result_params = _parse_content_type_header(header)
    
    assert result_type == expected_content_type
    assert result_params == expected_params