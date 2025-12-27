from requests.utils import _parse_content_type_header

def test_parse_content_type_header_single_param_no_quotes():
    # Refined: Covers standard param and malformed types (Critique: Malformed MIME Types)
    
    # Case 1: Standard
    header = "text/html; charset=utf-8"
    content_type, params = _parse_content_type_header(header)
    assert content_type == "text/html"
    assert params == {"charset": "utf-8"}

    # Case 2: Missing subtype (e.g. "text" instead of "text/plain")
    header_malformed = "text; charset=utf-8"
    ct, p = _parse_content_type_header(header_malformed)
    assert ct == "text"
    assert p == {"charset": "utf-8"}