from requests.utils import _parse_content_type_header

def test__parse_content_type_header_simple():
    """
    Test parsing a simple content-type without parameters.
    """
    header = "application/json"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "application/json"
    assert params == {}
