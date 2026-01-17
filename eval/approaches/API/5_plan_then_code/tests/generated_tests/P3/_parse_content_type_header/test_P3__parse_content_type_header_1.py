from requests.utils import _parse_content_type_header

def test_parse_content_type_header_basic():
    """
    Test parsing a standard Content-Type header with a type and a single parameter.
    """
    header = "application/json; charset=utf-8"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "application/json"
    assert params == {"charset": "utf-8"}