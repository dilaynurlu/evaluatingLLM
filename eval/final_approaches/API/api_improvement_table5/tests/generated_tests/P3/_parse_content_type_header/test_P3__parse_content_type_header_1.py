import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_simple():
    """
    Test parsing a header with only a content type and no parameters.
    Refined to include surrounding whitespace and control characters 
    to ensure they are handled (stripped) correctly.
    """
    header = "  application/json \r\n"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "application/json"
    assert params == {}