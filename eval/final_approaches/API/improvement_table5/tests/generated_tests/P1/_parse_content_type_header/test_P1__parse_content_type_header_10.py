import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_empty_quoted_value():
    """Test parsing a parameter where the value is an empty quoted string."""
    header = 'text/plain; key=""'
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/plain"
    assert params == {"key": ""}