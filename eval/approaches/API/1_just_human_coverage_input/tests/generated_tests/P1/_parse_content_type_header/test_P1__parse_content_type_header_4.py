from requests.utils import _parse_content_type_header

def test_parse_content_type_whitespace_handling():
    """
    Test parsing a header with irregular whitespace around delimiters.
    Verifies that extra spaces are stripped from keys and values.
    """
    header = " application/xml ;  charset =  ISO-8859-1 "
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "application/xml"
    assert params == {"charset": "ISO-8859-1"}