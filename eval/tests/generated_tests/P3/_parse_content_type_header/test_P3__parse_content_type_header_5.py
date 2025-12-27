from requests.utils import _parse_content_type_header

def test_parse_content_type_header_missing_value():
    # Refined: Covers flags and mixed parameter types
    header = "text/html; myflag; charset=utf-8"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/html"
    assert params["myflag"] is True
    assert params["charset"] == "utf-8"