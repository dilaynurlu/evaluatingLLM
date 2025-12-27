import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_header_empty_segments():
    """
    Test parsing a header with multiple consecutive semicolons (empty segments).
    Empty segments should be ignored.
    """
    header = "application/javascript;;; charset=utf-8;;"
    expected_content_type = "application/javascript"
    expected_params = {"charset": "utf-8"}
    
    result_type, result_params = _parse_content_type_header(header)
    
    assert result_type == expected_content_type
    assert result_params == expected_params