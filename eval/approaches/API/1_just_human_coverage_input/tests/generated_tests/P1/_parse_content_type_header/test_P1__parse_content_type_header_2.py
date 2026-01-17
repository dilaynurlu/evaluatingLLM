from requests.utils import _parse_content_type_header

def test_parse_content_type_no_params():
    """
    Test parsing a content-type header with no parameters.
    Verifies that the params dictionary is empty.
    """
    header = "text/plain"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/plain"
    assert params == {}