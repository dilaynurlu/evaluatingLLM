from requests.utils import _parse_content_type_header

def test_parse_content_type_header_simple_no_params():
    """
    Test parsing a simple content-type header with no parameters.
    """
    header = "application/json"
    expected_content_type = "application/json"
    expected_params = {}
    
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == expected_content_type
    assert params == expected_params