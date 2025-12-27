import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_value_containing_equals():
    # Validates that splitting key/value pairs stops at the first equals sign
    header = "text/x-dvi; format=key=value"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/x-dvi"
    # The value should contain the second equals sign intact
    assert params == {"format": "key=value"}