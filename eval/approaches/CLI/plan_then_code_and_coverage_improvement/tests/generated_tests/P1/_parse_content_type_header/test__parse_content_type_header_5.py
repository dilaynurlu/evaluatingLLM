import pytest
from requests.utils import _parse_content_type_header

def test__parse_content_type_header_empty_params():
    """Test parsing with trailing semicolon/empty params."""
    header = "text/html; ;"
    content_type, params = _parse_content_type_header(header)
    assert content_type == "text/html"
    assert params == {}
