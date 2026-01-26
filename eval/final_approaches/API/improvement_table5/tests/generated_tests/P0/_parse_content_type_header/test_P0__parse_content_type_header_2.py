from requests.utils import _parse_content_type_header

def test_content_type_with_multiple_params():
    header = "text/html; charset=utf-8; level=1"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/html"
    assert params == {"charset": "utf-8", "level": "1"}