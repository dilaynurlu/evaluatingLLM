from requests.utils import _parse_content_type_header

def test_parse_content_type_header_empty_segments():
    # Refined: Covers malformed structure with empty segments (Critique: Malformed inputs)
    header = "text/html;; ; charset=utf-8;"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/html"
    assert params == {"charset": "utf-8"}