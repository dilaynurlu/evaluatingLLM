from requests.utils import _parse_content_type_header

def test_parse_content_type_header_empty():
    """
    Test parsing an empty string header.
    Should return an empty content type and empty params dictionary.
    """
    header = ""
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == ""
    assert params == {}