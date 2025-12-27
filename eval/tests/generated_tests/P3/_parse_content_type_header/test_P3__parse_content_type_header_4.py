from requests.utils import _parse_content_type_header

def test_parse_content_type_header_whitespace_around_equals():
    # Refined: Covers excessive whitespace handling
    header = "text/plain ;  charset  =  utf-8 "
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/plain"
    assert params == {"charset": "utf-8"}