from requests.utils import _parse_content_type_header

def test_parse_content_type_header_quoted_parameter():
    """
    Test parsing a Content-Type header where the parameter value is enclosed in double quotes.
    The quotes should be stripped from the parsed value.
    """
    header = 'application/xml; charset="utf-16"'
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "application/xml"
    assert params == {'charset': 'utf-16'}