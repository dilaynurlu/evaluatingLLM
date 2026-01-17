from requests.utils import _parse_content_type_header

def test_parse_content_type_header_single_quoted_parameter():
    """
    Test parsing a Content-Type header where the parameter value is enclosed in single quotes.
    The quotes should be stripped from the parsed value.
    """
    header = "text/plain; charset='iso-8859-1'"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/plain"
    assert params == {'charset': 'iso-8859-1'}