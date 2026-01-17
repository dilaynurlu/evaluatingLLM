from requests.utils import _parse_content_type_header

def test_parse_content_type_header_irregular_whitespace():
    """
    Test parsing a Content-Type header with irregular whitespace around the semicolon and equals sign.
    Whitespace should be stripped correctly.
    """
    header = "text/html ;  charset =  utf-8 "
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/html"
    assert params == {'charset': 'utf-8'}