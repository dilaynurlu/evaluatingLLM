import pytest
from requests.utils import _parse_content_type_header

def test__parse_content_type_header_quotes():
    """Test parsing parameters with quotes."""
    header = 'text/html; charset="utf-8"'
    content_type, params = _parse_content_type_header(header)
    assert content_type == "text/html"
    assert params == {"charset": "utf-8"}
