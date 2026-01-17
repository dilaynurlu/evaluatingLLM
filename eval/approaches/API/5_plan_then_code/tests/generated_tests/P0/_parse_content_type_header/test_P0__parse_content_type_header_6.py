from requests.utils import _parse_content_type_header

def test_parse_content_type_empty_segments():
    """Test handling of empty segments caused by extra semicolons."""
    header = "text/plain;;; charset=us-ascii;"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/plain"
    assert params == {"charset": "us-ascii"}