import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_empty_segments():
    # Validates that empty segments caused by consecutive semicolons are ignored
    header = "image/png;;; required=true"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "image/png"
    assert params == {"required": "true"}