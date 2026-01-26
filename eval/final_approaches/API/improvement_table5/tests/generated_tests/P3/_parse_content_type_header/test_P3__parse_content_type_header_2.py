import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_with_params():
    """
    Test parsing a header with standard key=value parameters.
    Refined to test duplicate parameters (HTTP Parameter Pollution).
    The function should retain the last occurrence of a duplicate key.
    """
    header = "text/html; charset=utf-8; v=1; charset=iso-8859-1"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/html"
    # Expect the last 'charset' value to overwrite previous ones
    assert params == {"charset": "iso-8859-1", "v": "1"}