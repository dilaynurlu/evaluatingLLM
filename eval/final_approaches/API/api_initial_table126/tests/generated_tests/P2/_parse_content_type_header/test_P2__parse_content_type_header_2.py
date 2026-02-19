from requests.utils import _parse_content_type_header

def test_parse_content_type_with_charset():
    """
    Test parsing a content type header with a single charset parameter.
    """
    header = "text/html; charset=UTF-8"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/html"
    # Keys should be normalized to lower-case, values preserved
    assert params == {"charset": "UTF-8"}