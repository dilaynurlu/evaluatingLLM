import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_excessive_whitespace_and_quoting():
    # Validates stripping of mixed quotes (single/double) and whitespace around keys and values
    header = "application/xml;  ' key '  =  \" value \" "
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "application/xml"
    assert params == {"key": "value"}