import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_header_single_quoted_values():
    """
    Test parsing parameters where values are enclosed in single quotes.
    The single quotes should be stripped from the parsed values.
    """
    header = "text/xml; encoding='latin1'"
    expected_content_type = "text/xml"
    expected_params = {"encoding": "latin1"}
    
    result_type, result_params = _parse_content_type_header(header)
    
    assert result_type == expected_content_type
    assert result_params == expected_params