import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_whitespace_and_empty_segments():
    """
    Test robustness against extra whitespace and empty semicolon segments.
    The parser should ignore empty segments and strip whitespace from keys/values.
    """
    # Note: " ; " creates an empty param string which the loop skips
    header = " text/html ;  ; charset= us-ascii "
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/html"
    # Spaces around 'us-ascii' should be stripped
    assert params == {"charset": "us-ascii"}