from requests.utils import _parse_content_type_header

def test_parse_content_type_header_quoted_parameter():
    """
    Test parsing a content-type header where the parameter value is enclosed in double quotes.
    The function should strip the quotes.
    """
    header = 'text/html; charset="utf-8"'
    expected_content_type = "text/html"
    expected_params = {"charset": "utf-8"}
    
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == expected_content_type
    assert params == expected_params