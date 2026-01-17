import pytest
from requests.utils import _parse_content_type_header

def test_parse_simple_content_type_no_params():
    """
    Test parsing a simple content-type header string containing only the MIME type
    without any parameters.
    """
    header = "application/json"
    result = _parse_content_type_header(header)
    
    assert result == ("application/json", {})