from requests.utils import _parse_content_type_header

def test_parse_content_type_basic():
    """
    Test parsing a standard content-type header with one parameter.
    Verifies that the content type and parameter are correctly extracted.
    """
    header = "application/json; charset=utf-8"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "application/json"
    assert params == {"charset": "utf-8"}