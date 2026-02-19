import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_flag_param_no_value():
    """Test that parameters without an equals sign are treated as flags with value True."""
    header = "text/html; secure; httponly"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/html"
    assert params == {"secure": True, "httponly": True}