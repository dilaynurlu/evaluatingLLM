from requests.utils import _parse_content_type_header

def test_parse_content_type_empty_segments():
    """
    Test handling of empty segments (consecutive semicolons) in the header.
    These should be ignored without causing errors or empty keys.
    """
    header = "text/css; ; charset=utf-8; ; ; version=1"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/css"
    assert params == {
        "charset": "utf-8",
        "version": "1"
    }