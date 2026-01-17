from requests.utils import _parse_content_type_header

def test_parse_content_type_header_empty_segments():
    """
    Test parsing a header with multiple consecutive semicolons (empty segments).
    Empty segments should be ignored to prevent errors.
    """
    header = "multipart/form-data; ; boundary=abc; ; "
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "multipart/form-data"
    assert params == {"boundary": "abc"}