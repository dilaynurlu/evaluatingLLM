import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_multiple_params_empty_segments():
    """Test parsing multiple parameters while ignoring empty segments (;;)."""
    header = "multipart/form-data; boundary=something;; charset=utf-8"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "multipart/form-data"
    assert params == {"boundary": "something", "charset": "utf-8"}