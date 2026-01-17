from requests.utils import _parse_content_type_header

def test_parse_content_type_header_parameter_value_containing_equals():
    """
    Test parsing a Content-Type header where a parameter value contains an equals sign.
    The parser should split only on the first equals sign for the key-value pair.
    """
    header = 'text/x-dvi; names="foo=bar"'
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/x-dvi"
    # The quotes are stripped, but the internal equals sign remains
    assert params == {'names': 'foo=bar'}