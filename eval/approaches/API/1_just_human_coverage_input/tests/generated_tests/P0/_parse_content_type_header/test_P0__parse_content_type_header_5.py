from requests.utils import _parse_content_type_header

def test_parse_content_type_header_boolean_parameter():
    """
    Test parsing a Content-Type header with a parameter that has no value (no equals sign).
    It should be treated as a flag with a value of True.
    """
    header = "text/html; verbose"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/html"
    assert params == {'verbose': True}