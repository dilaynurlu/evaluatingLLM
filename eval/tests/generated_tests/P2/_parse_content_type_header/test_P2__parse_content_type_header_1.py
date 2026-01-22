from requests.utils import _parse_content_type_header

def test_parse_content_type_simple_no_params():
    """
    Test parsing a content type header that has no parameters.
    """
    header = "application/xml"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "application/xml"
    assert params == {}