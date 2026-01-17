from requests.utils import _parse_content_type_header

def test_parse_content_type_header_no_params():
    """
    Test parsing a Content-Type header that has no parameters.
    """
    header = "text/plain"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/plain"
    assert params == {}