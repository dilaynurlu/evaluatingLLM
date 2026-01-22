from requests.utils import _parse_content_type_header

def test__parse_content_type_header_5():
    # Malformed header (no semicolon)
    ct, params = _parse_content_type_header("text/plain")
    assert ct == "text/plain"
    assert params == {}
    
    # Empty
    #ct, params = _parse_content_type_header("")
    #assert ct == ""
