import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_empty_segments():
    """
    Test that empty segments (caused by double semicolons or trailing semicolons)
    are ignored correctly.
    """
    header = "text/css;; charset=utf-8;; ;"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/css"
    assert params == {"charset": "utf-8"}