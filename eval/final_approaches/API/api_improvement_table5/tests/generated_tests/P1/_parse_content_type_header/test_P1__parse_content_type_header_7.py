import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_value_with_equals():
    """Test that values containing equals signs are parsed correctly (split only on first =)."""
    header = "text/x-lua; option=a=b"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/x-lua"
    assert params == {"option": "a=b"}