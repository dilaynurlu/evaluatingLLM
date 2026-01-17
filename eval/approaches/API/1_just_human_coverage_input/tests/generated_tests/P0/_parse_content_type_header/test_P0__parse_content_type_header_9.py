from requests.utils import _parse_content_type_header

def test_parse_content_type_header_quoted_key():
    """
    Test parsing a Content-Type header where the parameter key is enclosed in quotes.
    The quotes should be stripped from the key.
    """
    header = 'text/html; "charset"=utf-8'
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/html"
    assert params == {'charset': 'utf-8'}