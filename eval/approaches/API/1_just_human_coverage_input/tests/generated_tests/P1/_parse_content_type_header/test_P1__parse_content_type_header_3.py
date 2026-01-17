from requests.utils import _parse_content_type_header

def test_parse_content_type_quoted_values():
    """
    Test parsing parameters with double-quoted values.
    Verifies that quotes are stripped from the value.
    """
    header = 'text/html; charset="utf-8"'
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/html"
    assert params == {"charset": "utf-8"}