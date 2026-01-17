import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_header_handles_flag_parameters():
    # Parameters without equals sign are treated as boolean flags (True)
    header = "text/plain; verbose"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/plain"
    assert params == {"verbose": True}