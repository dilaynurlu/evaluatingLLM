import pytest
from requests.utils import _parse_content_type_header

def test__parse_content_type_header_multiple_params():
    """Test parsing multiple parameters."""
    header = "multipart/form-data; boundary=something; charset=utf-8"
    content_type, params = _parse_content_type_header(header)
    assert content_type == "multipart/form-data"
    assert params == {"boundary": "something", "charset": "utf-8"}
