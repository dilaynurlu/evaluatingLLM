from requests.utils import _parse_content_type_header

def test_parse_content_type_whitespace_normalization():
    """
    Test that surrounding whitespace is stripped from the content type
    and from keys/values in the parameters.
    """
    header = "  text/html  ;  charset  =  utf-8  "
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/html"
    assert params == {"charset": "utf-8"}