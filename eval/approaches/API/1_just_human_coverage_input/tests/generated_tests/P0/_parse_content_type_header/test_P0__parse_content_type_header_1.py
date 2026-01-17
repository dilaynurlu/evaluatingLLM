from requests.utils import _parse_content_type_header

def test_parse_content_type_header_simple_no_params():
    """
    Test parsing a simple Content-Type header with no parameters.
    """
    header = "application/json"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "application/json"
    assert params == {}